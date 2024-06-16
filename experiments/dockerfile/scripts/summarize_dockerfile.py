#!/usr/bin/env python3

import rse.utils.file as utils

import requests
import argparse
import sys
import shutil
import os
import re

here = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(here)


def get_parser():
    parser = argparse.ArgumentParser(description="Dockerfile Parser")
    parser.add_argument(
        "--outdir",
        default=os.path.join(root, "data", "dockerfile"),
        help="output data directory for results",
    )
    return parser


def main():
    parser = get_parser()
    args, _ = parser.parse_known_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    files = list(utils.recursive_find(root, "Dockerfile*"))
    print(f"Total Dockerfile across project: {len(files)}")

    # Number in rse repos?
    total_rse_repos = 0
    total_with_dockerfile = 0

    rse_repos_root = os.path.join(root, "data", "rseng")
    for parent in os.listdir(rse_repos_root):
        parent_path = os.path.join(rse_repos_root, parent)
        for child in os.listdir(parent_path):
            child_path = os.path.join(parent_path, child)
            total_rse_repos += 1
            if len(list(utils.recursive_find(child_path, "Dockerfile*"))) > 0:
                total_with_dockerfile += 1
            print("%s/%s" % (total_with_dockerfile, total_rse_repos), end="\r")

    # Now let's tabulate FROM images across RSENG repos and ML ones
    froms = {"machine-learning": {}, "rseng": {}}
    for dockerfile in files:
        lines = utils.read_file(dockerfile)
        # This is janky but will get rid of FROM, spaces and "as" x
        lines = [
            x.strip().replace("FROM", "").strip().split(" ")[0].strip()
            for x in lines
            if "FROM" in x
        ]

        # machine learning image
        for x in lines:
            # Skip ones with variables
            if "$" in x or "#" in x:
                continue
            if "/orgs/" in dockerfile:
                if x not in froms["machine-learning"]:
                    froms["machine-learning"][x] = 0
                froms["machine-learning"][x] += 1
            else:
                if x not in froms["rseng"]:
                    froms["rseng"][x] = 0
                froms["rseng"][x] += 1

    # Write file, sorted by value
    froms["machine-learning"] = {
        k: v
        for k, v in sorted(
            froms["machine-learning"].items(), key=lambda item: item[1], reverse=True
        )
    }
    froms["rseng"] = {
        k: v
        for k, v in sorted(
            froms["rseng"].items(), key=lambda item: item[1], reverse=True
        )
    }
    outfile = os.path.join(args.outdir, "dockerfile-counts.json")
    utils.write_json(froms, outfile)

    # For each dockerfile FROM, we want to get:
    # 1. tags over time
    # 2. for each tag:
    # 3.   total size (summed from manifest)
    # 4.   number of layers (manifest)
    # 5.   size of each layer
    # The config has timestamps for creation of layers

    # For this parsing we are just going to get (and save) the data for each
    data_outdir = os.path.join(args.outdir, "registry")

    # Top level output
    seen = set()

    # Keep track of those not parseable
    misses = set()

    # Get common uris
    uris = list(froms["machine-learning"].keys()) + list(froms["rseng"].keys())
    for uri in uris:
        print(f"Getting manifests, configs, and tags for {uri}")

        try:
            # If we have a tag, remove for now
            if "@" in uri:
                uri = uri.split("@")[0]
            if ":" in uri:
                uri = uri.split(":")[0]
        except:
            continue

        if uri in seen:
            continue
        seen.add(uri)

        image_outdir = os.path.join(data_outdir, uri)
        output_file = os.path.join(image_outdir, "manifests-config-layers.json")
        if os.path.exists(output_file):
            print(f"Skipping {output_file}, already exists.")
            continue
        if not os.path.exists(image_outdir):
            os.makedirs(image_outdir)

        try:
            parse_image(uri, image_outdir)
        except Exception as exc:
            print(f"Issue parsing image {uri}: {exc}")
            misses.add(uri)
            if os.path.exists(image_outdir) and not os.path.exists(output_file):
                shutil.rmtree(image_outdir)

    print(misses)


def parse_image(uri, image_outdir):
    """
    Parse an image, getting manifests and configs and
    layers for each tag.
    """
    image = DockerImage(uri)

    # Cache tags
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
    utils.write_json(result, os.path.join(image_outdir, "manifests-config-layers.json"))


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
