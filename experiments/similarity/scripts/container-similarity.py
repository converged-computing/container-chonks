#!/usr/bin/env python3

import argparse
import json
import os
import re
import shutil
import sys
import hashlib

from datetime import datetime
import numpy
import matplotlib.pylab as plt
import pandas
import seaborn as sns
import requests

here = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(here)

timestamp_format = "%Y-%m-%dT%H:%M:%SZ"

# Container URI set that are intentionally more similar
ensemble_containers = [
    # Google
    "ghcr.io/converged-computing/ensemble-amg2023",
    "ghcr.io/converged-computing/ensemble-lammps",
    "ghcr.io/converged-computing/ensemble-kripke",
    "ghcr.io/converged-computing/ensemble-laghos",
    "ghcr.io/converged-computing/ensemble-minife",
    "ghcr.io/converged-computing/ensemble-mixbench",
    "ghcr.io/converged-computing/ensemble-mt-gemm",
    "ghcr.io/converged-computing/ensemble-osu",
    "ghcr.io/converged-computing/ensemble-quicksilver",
    "ghcr.io/converged-computing/ensemble-stream",
]

# "Matching" containers from the performance study that are different
study_containers = [
    "ghcr.io/converged-computing/metric-amg2023:spack-slim",
    "ghcr.io/converged-computing/metric-lammps-cpu:zen4",
    "ghcr.io/converged-computing/metric-kripke-cpu:zen4",
    "ghcr.io/converged-computing/metric-laghos:cpu-zen4",
    "ghcr.io/converged-computing/metric-minife:cpu-zen4",
    "ghcr.io/converged-computing/metric-mixbench:cpu",
    "ghcr.io/converged-computing/mt-gemm:cpu-zen4",
    "ghcr.io/converged-computing/metric-osu-cpu:zen4",
    "ghcr.io/converged-computing/metric-quicksilver-cpu:zen4",
    "ghcr.io/converged-computing/metric-stream:cpu-zen4",
]

spack_containers = [
    "ghcr.io/converged-computing/ensemble-amg2023:spack",
    "ghcr.io/converged-computing/ensemble-lammps:spack",
    "ghcr.io/converged-computing/ensemble-stream:spack",
    "ghcr.io/converged-computing/ensemble-laghos:spack",
    "ghcr.io/converged-computing/ensemble-minife:spack",
    "ghcr.io/converged-computing/ensemble-quicksilver:spack",
    "ghcr.io/converged-computing/ensemble-osu:spack",
]


def get_parser():
    parser = argparse.ArgumentParser(description="Container Similarity")
    parser.add_argument(
        "--data",
        default=os.path.join(root, "data"),
        help="data directory for results",
    )
    return parser


def read_file(filename):
    with open(filename, "r") as fd:
        content = fd.read()
    return content


def read_json(filename):
    return json.loads(read_file(filename))


def write_json(obj, filename):
    with open(filename, "w") as fd:
        fd.write(json.dumps(obj, indent=4))


def recursive_find(base, pattern="*.*"):
    """
    Recursively find and yield files matching a glob pattern.
    """
    for root, _, filenames in os.walk(base):
        for filename in filenames:
            if not re.search(pattern, filename):
                continue
            yield os.path.join(root, filename)


def find_inputs(input_dir):
    """
    Find inputs (results files)
    """
    files = []
    for filename in recursive_find(input_dir, pattern="manifests-config-layers.json"):
        # We only have data for small
        files.append(filename)
    return files


def main():
    global ensemble_containers
    global study_containers
    global spack_containers
    parser = get_parser()
    args, _ = parser.parse_known_args()

    # Perform analysis for each set of similar and not similar containers
    container_sets = {
        "performance-study": study_containers,
        "containers": ensemble_containers,
        "spack": spack_containers,
    }
    for label, containers in container_sets.items():

        # Output directory for containers
        data_dir = os.path.join(args.data, "containers", label)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Get manifests for our container set
        retrieve_manifests(data_dir, containers)

        # Now read in manifests - the json pattern
        files = find_inputs(data_dir)

        # Output directory for images
        data_dir = os.path.join(args.data, "similarity", label)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # The rest is to calculate similarity
        # Filter down to those in our study
        df = parse_manifests(files)
        df.to_csv(os.path.join(data_dir, "layer-sizes.csv"))

        # Make some plots of sizes and similarity
        plot_layers(df, data_dir, label)

        # Finally, similarity based on image configs
        plot_config_similarity(files, data_dir, label)
        print()


def plot_config_similarity(files, outdir, label):
    # This is a content digest we will calculate
    df = pandas.DataFrame(
        columns=[
            "uri",
            "full_uri",
            "digest",
        ]
    )
    idx = 0

    for filename in files:
        uri, item = derive_uri_from_filepath(filename)

        # Have each group of tags as a transaction
        for tag, cfg in item["configs"].items():
            for layer in cfg["history"]:
                hasher = hashlib.sha256()
                full_uri = f"{uri}:{tag}"
                if "created_by" not in layer:
                    continue
                content = layer["created_by"].replace(" ", "").lower()
                hasher.update(bytes(content.encode("utf-8")))
                digest = hasher.hexdigest()
                df.loc[idx, :] = [
                    uri,
                    full_uri,
                    digest,
                ]
                idx += 1

    calculate_similarity(
        df, outdir, "container-layer-content-similarity", label + "-content"
    )


def calculate_similarity(df, outdir, outfile, label):
    """
    Calculate pairwaise similarity of containers and save to file
    """
    # Now calculate similiarty
    sims = pandas.DataFrame(
        index=df.full_uri.unique().tolist(), columns=df.full_uri.unique().tolist()
    )

    # This is similarity based on EXACT layer digests
    total = len(sims.index)
    for i, a in enumerate(sims.index):
        for b in sims.index:
            if a == b:
                sims.loc[a, b] = 1
                continue
            # Otherwise, we want to know the number of digests they share
            # Let's calculate jacaard similarity:
            # intersection(a,b) / union(a,b)
            layers_a = set(df[df.full_uri == a].digest.tolist())
            layers_b = set(df[df.full_uri == b].digest.tolist())
            score = len(layers_a.intersection(layers_b)) / len(layers_a.union(layers_b))
            sims.loc[a, b] = score

    sims.to_csv(os.path.join(outdir, f"{outfile}-similarity.csv"))

    # Update sims index and columns to make them shorter (they will render on the plot)
    names = [
        x.replace("ghcr.io/converged-computing/", "").replace("metric-", "")
        for x in sims.index.tolist()
    ]
    sims.index = names
    sims.columns = names

    # Now plot it! Remove containers so we just have tags left
    plt.figure(figsize=(36, 36))
    sims = sims.astype(float)
    # Ensure range is 0 to 1 to match performance study
    m = sns.heatmap(
        sims, annot=True, vmin=0.0, vmax=1.0, cmap="BrBG", mask=(sims == 0.0)
    )
    m.set_facecolor("black")
    plt.savefig(os.path.join(outdir, f"{outfile}.png"))
    plt.savefig(os.path.join(outdir, f"{outfile}.svg"))
    plt.clf()

    m = sns.clustermap(sims, vmin=0.0, vmax=1.0, annot=False, cmap="BrBG")
    plt.savefig(os.path.join(outdir, f"cluster-{outfile}.png"))
    plt.savefig(os.path.join(outdir, f"cluster-{outfile}.svg"))
    plt.clf()

    # Get a gist of the groups
    new_order = m.dendrogram_row.reordered_ind
    new_rows = sims.index[new_order].tolist()
    new_order = m.dendrogram_col.reordered_ind
    new_cols = sims.index[new_order].tolist()
    write_json(
        {"rows": new_rows, "cols": new_cols},
        os.path.join(outdir, f"cluster-{outfile}-labels.json"),
    )

    # Print similarity
    print(f"Similarity for {label}")
    mean = numpy.mean(sims.values)
    std = numpy.std(sims.values)
    print("mean: " + str(mean))
    print("std " + str(std))


def plot_layers(df, outdir, label):
    """
    Plot a histogram of layers
    """
    print(f"Stats for container set {label}")
    # Summary of space. How many layers?
    print("How many layers?")
    print(df.shape)
    print("How many unique URIs not including tags?")
    print(len(df.uri.unique()))
    print("How many unique URIs including tags?")
    print(len(df.full_uri.unique()))
    print("How many unique layer digests?")
    unique_layers = len(df.digest.unique())
    print(unique_layers)
    # Filter out empty layers and small layers (WORKDIR, etc)
    # This value is arbitrary, over 1MB
    total_layers = df.shape[0]
    subset = df[df.layer_size > 1000000]
    values = subset.layer_size.values
    ax = sns.histplot(values)
    plt.title(
        f"Sizes of {unique_layers} unique layers across {total_layers} layers and 11 application builds"
    )
    ax.set_xlabel("Size (bytes)", fontsize=16)
    plt.savefig(os.path.join(outdir, "layer-size-histogram.png"))
    plt.clf()

    # Now calculate similiarty
    calculate_similarity(df, outdir, "container-similarity", label + "-digests")


def parse_manifests(files):
    """
    Given a listing of files, parse into results data framed
    """
    # fields are consistent
    df = pandas.DataFrame(
        columns=[
            "uri",
            "full_uri",
            "layer_size",
            "digest",
            "media_type",
            "schema_version",
        ]
    )
    idx = 0

    # manifests has the following:
    # shared digests across images
    # distribution of sizes in different contexts
    # distribution of platforms / arch
    seen = set()
    for filename in files:
        if filename in seen:
            continue
        uri, item = derive_uri_from_filepath(filename)

        # Have each group of tags as a transaction
        for tag, manifest in item["manifests"].items():
            created_at = item["configs"][tag]["created"].rsplit("T")[0]
            created_at = f"{created_at} 00:00:00"

            full_uri = f"{uri}:{tag}"
            if "layers" not in manifest:
                print(f"Missing layers for {uri}")
                continue

            for i, layer in enumerate(manifest["layers"]):
                digest = layer["digest"]
                size = layer["size"]
                mt = layer["mediaType"]
                sv = manifest["schemaVersion"]
                df.loc[idx, :] = [
                    uri,
                    full_uri,
                    size,
                    digest,
                    mt,
                    sv,
                ]
                idx += 1

        seen.add(filename)

    return df


def retrieve_manifests(data_dir, containers):
    """
    Retrieve manifests for a set of containers, if they do not exist.
    """
    # For each dockerfile FROM, we want to get:
    # 1. tags over time
    # 2. for each tag:
    # 3.   total size (summed from manifest)
    # 4.   number of layers (manifest)
    # 5.   size of each layer
    # The config has timestamps for creation of layers
    misses = set()

    # Generate unique list of uris and tags (most containers have multiple tags)
    lookup = {}
    for uri in containers:
        if ":" in uri:
            uri, tag = uri.split(":", 1)
        else:
            tag = "latest"
        if uri not in lookup:
            lookup[uri] = set()
        lookup[uri].add(tag)

    # Save list of output files
    output_files = []
    for uri, tags in lookup.items():
        image_outdir = os.path.join(data_dir, uri)
        output_file = os.path.join(image_outdir, "manifests-config-layers.json")
        output_files.append(output_file)
        if os.path.exists(output_file):
            continue
        if not os.path.exists(image_outdir):
            os.makedirs(image_outdir)

        try:
            print(f"Looking for tags {tags} for {uri}")
            parse_image(uri, image_outdir, list(tags))
        except Exception as exc:
            print(f"Issue parsing image {uri}: {exc}")
            misses.add(uri)
            if os.path.exists(image_outdir) and not os.path.exists(output_file):
                shutil.rmtree(image_outdir)

    # At time of study, no misses
    if misses:
        print(misses)

    # Parse manifests to get layer metadata
    df = parse_manifests(output_files)
    df.to_csv(os.path.join(data_dir, "container-layers-csv"))


def parse_time_pulled(time_pulled):
    minutes = 0
    # First check for milliseconds, if reported in ms there aren't seconds or minutes
    if "ms" in time_pulled:
        return float(time_pulled.replace("ms", "", 1)) / 1000
    if "m" in time_pulled:
        minutes, rest = time_pulled.split("m", 1)
        minutes = int(minutes)
        time_pulled = rest
    seconds = float(time_pulled.rstrip("s"))
    return (minutes * 60) + seconds


def derive_uri_from_filepath(filename):
    parsed = os.path.relpath(filename, root).split(os.sep, 3)[-1].strip(os.sep)
    uri, _ = parsed.rsplit(os.sep, 1)
    item = read_json(filename)
    return uri, item


def parse_manifests(files):
    """
    Given a listing of files, parse into results data framed
    """
    # fields are consistent
    df = pandas.DataFrame(
        columns=[
            "uri",
            "full_uri",
            "layer_size",
            "platform",
            "arch",
            "digest",
            "os",
            "schema_version",
        ]
    )
    idx = 0

    # manifests has the following:
    # shared digests across images
    # distribution of sizes in different contexts
    # distribution of platforms / arch
    seen = set()
    for filename in files:
        if filename in seen:
            continue
        uri, item = derive_uri_from_filepath(filename)

        if "manifests" not in item:
            continue

        # Have each group of tags as a transaction
        for tag, manifest in item.get("manifests", {}).items():
            # Don't parse manifest lists
            if (
                "mediaType" not in manifest
                or manifest["mediaType"]
                == "application/vnd.docker.distribution.manifest.list.v2+json"
            ):
                continue
            if "layers" not in manifest or manifest["schemaVersion"] == 1:
                continue
            if tag not in item["configs"]:
                continue

            created_at = item["configs"][tag]["created"].rsplit("T")[0]
            created_at = f"{created_at} 00:00:00"

            full_uri = f"{uri}:{tag}"
            for i, layer in enumerate(manifest["layers"]):
                platform = layer.get("platform") or {}
                arch = platform.get("architecture") or "unknown"
                digest = layer["digest"]
                opsys = platform.get("os") or "unknown"
                size = layer["size"]
                sv = manifest["schemaVersion"]
                df.loc[idx, :] = [
                    uri,
                    full_uri,
                    size,
                    platform,
                    arch,
                    digest,
                    opsys,
                    sv,
                ]
                idx += 1

        seen.add(filename)

    return df


def parse_image(uri, image_outdir, tags=None):
    """
    Parse an image, getting manifests and configs and
    layers for each tag.
    """
    image = DockerImage(uri)

    # Cache tags
    if tags is None:
        tags = image.tags()

    manifests = {}
    configs = {}

    # Only get 500 tags
    if len(tags) > 500:
        tags = tags[:500]

    print(f"  Found {len(tags)} for {uri}")
    for tag in tags:
        if tag.endswith("sig") or tag.endswith("att"):
            continue
        print(f"  Retrieving tag {tag}")
        try:
            # This has layers and sizes
            manifests[tag] = image.manifest(tag)
            # Get the image config - this has creation dates
            # And also what is in every layer!
            configs[tag] = image.config(tag)
        except Exception as ex:
            print(f"  Issue retrieving tag {tag}: {ex}")

    # Save data -
    result = {"manifests": manifests, "tags": tags, "configs": configs}
    write_json(result, os.path.join(image_outdir, "manifests-config-layers.json"))


class DockerImage:
    """
    A thin client for getting metadata about an image.
    """

    def __init__(self, container_name):
        self.container_name = container_name

        # might not last forever, but we can use it for now
        self.apiroot = "https://crane.ggcr.dev"

    def get_request(self, url):
        """
        Perform a get request, expecting status code 200.
        """
        response = requests.get(url)
        if response.status_code != 200:
            sys.exit("Issue with request %s" % url)
        return response

    def tags(self):
        """
        Get image tags.
        """
        # Quay does not follow the distribution spec, crane only returns 50
        if "quay.io" in self.container_name:
            return self.tags_quay()

        url = "%s/ls/%s" % (self.apiroot, self.container_name)
        response = self.get_request(url)
        tags = [x.strip() for x in response.text.split("\n") if x.strip()]
        # Don't include tags for vex or sbom
        tags = [x for x in tags if not re.search("[.](sbom|vex)$", x)]
        return tags

    def tags_quay(self):
        """
        Custom endpoint to handle quay and pagination.
        """
        repository = self.container_name.replace("quay.io/", "", 1)
        page = 1
        tags = []
        has_more = True
        while has_more:
            url = f"https://quay.io/api/v1/repository/{repository}/tag/?limit=100&page={page}"
            response = self.get_request(url).json()
            new_tags = [
                x.get("name") for x in response.get("tags", {}) if x.get("name")
            ]
            new_tags = [x for x in new_tags if not re.search("[.](sbom|vex)$", x)]
            tags += new_tags
            has_more = response.get("has_additional") is True
            page += 1
        return tags

    def manifest(self, tag):
        url = "%s/manifest/%s:%s" % (self.apiroot, self.container_name, tag)
        response = self.get_request(url)
        return response.json()

    def digest(self, tag):
        url = "%s/digest/%s:%s" % (self.apiroot, self.container_name, tag)
        response = self.get_request(url)
        if "could not parse reference" in response:
            sys.exit("Issue getting digest: %s" % response)
        if "unsupported status" in response:
            sys.exit("Issue getting digest: %s" % response)
        if "MANIFEST_UNKNOWN" in response.text:
            sys.exit(
                f"The tag {tag} you provided is not known. Check that it and the container both exist."
            )
        return response.text

    def config(self, tag):
        url = "%s/config/%s:%s" % (self.apiroot, self.container_name, tag)
        return self.get_request(url).json()


if __name__ == "__main__":
    main()
