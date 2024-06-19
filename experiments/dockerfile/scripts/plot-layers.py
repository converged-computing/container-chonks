#!/usr/bin/env python3

import argparse
import collections
import fnmatch
import string
import os
import math
import numpy

import sqlite3

from collections import OrderedDict
import matplotlib.pyplot as plt
import metricsoperator.utils as utils
import pandas
import seaborn as sns
import re
from datetime import datetime
from metricsoperator.metrics.app.lammps import parse_lammps

plt.style.use("bmh")
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Plot Dockerfile Layers",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--results",
        help="directory with raw results data",
        default=os.path.join(root, "data", "dockerfile", "registry"),
    )
    parser.add_argument(
        "--out",
        help="directory to save parsed results",
        default=os.path.join(root, "img"),
    )
    return parser


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
    """
    Run the main plotting operation!
    """
    parser = get_parser()
    args, _ = parser.parse_known_args()

    # Output images and data
    outdir = os.path.abspath(args.out)
    indir = os.path.abspath(args.results)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Find input files (skip anything with test)
    files = find_inputs(indir)
    if not files:
        raise ValueError(f"There are no input files in {indir}")

    # This gives us categories
    category_file = os.path.join(
        root, "data", "dockerfile", "dockerfile-counts-cleaned.json"
    )
    categories = utils.read_json(category_file)

    # Database file
    db_file = os.path.join(root, "data", "dockerfile", "data-frame.db")

    manifest_file = os.path.join(outdir, "docker-layers.csv")
    if not os.path.exists(manifest_file):
        # This does the actual parsing of data into a formatted variant
        # Has keys results, iters, and columns
        # parse_manifests(files, args, categories, db_file)

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Damn that's a big table!
        # cursor.execute('select count(*) from manifests;')
        # <sqlite3.Cursor at 0x7b71848f80c0>
        # cursor.fetchone()
        # (2872188,)
        manifest_df = pandas.read_sql_query(
            "SELECT * from manifests",
            conn,
            parse_dates={"datetime": "%Y-%m-%d %H:%M:%S"},
        )
        conn.close()

        # There are a few bad date times we will need to filter out.
        dts = []
        for x in manifest_df.created_at:
            try:
                dts.append(
                    pandas.to_datetime(datetime.strptime(x, "%Y-%M-%d 00:00:00").date())
                )
            except:
                dts.append(None)

        # Add to the data frame and filter out null rows.
        manifest_df["created_dt"] = dts
        manifest_df = manifest_df.loc[manifest_df.created_dt.isnull() == False]
        manifest_df.created_dt = pandas.to_datetime(manifest_df.created_dt)

        # Show means grouped by experiment to sanity check plots
        manifest_df.to_csv(manifest_file)
    else:
        manifest_df = pandas.read_csv(
            os.path.join(outdir, "docker-layers.csv"), index_col=0
        )

    # We need to tokenize the content of the layers
    # We won't save to data frame, but write directly to file
    parse_configs(files, args, categories, db_file)
    # plot_results(manifest_df, outdir)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def derive_by_year(df, outdir):
    # Create a variant that groups by year
    by_year = pandas.DataFrame(columns=["uri", "size", "year", "size_log"])
    idx = 0
    for item, size in df.groupby(["uri", df.created_dt.dt.year])["size"].mean().items():
        by_year.loc[idx, :] = item[0], size, item[1], numpy.log(size)
        idx += 1

    # Try using all data and creating year column
    df["year"] = df.created_dt.dt.year

    # Filter out those earlier than 2014 - those dates have to be erroneous
    by_year = by_year[by_year.year >= 2010]
    return by_year


def plot_results(df, outdir):
    """
    Plot dockerfile results
    """
    # by_year = derive_by_year(df, outdir)
    # df_by_year = df[df.year >= 2010]
    # size_logs = [numpy.log(x) for x in df_by_year["size"]]
    # df_by_year["size_log"] = size_logs

    # How have the number of layers changed over time?
    layer_file = os.path.join(outdir, "layer-counts-by-year.csv")
    if not os.path.exists(layer_file):
        layer_counts = derive_layer_counts(df)
        layer_counts.to_csv(layer_file)
    else:
        layer_counts = pandas.read_csv(layer_file, index_col=0)

    import IPython

    IPython.embed()
    sys.exit()

    colors = sns.color_palette("hls", 16)
    hexcolors = colors.as_hex()
    types = list(by_year.year.unique())
    types.sort()

    # ALWAYS double check this ordering, this
    # is almost always wrong and the colors are messed up
    palette = collections.OrderedDict()
    for t in types:
        palette[t] = hexcolors.pop(0)

    # What about shared layers?
    digests_file = os.path.join(outdir, "layer-counts.csv")
    if not os.path.exists(digests_file):
        digests = df.groupby(["digest"])["digest"].count()
        digests = digests.sort_values(ascending=False)

        # Figure out what the layers are. Let's choose those above a threshold.

        # How many are unique?
        print(len(digests.values[digests.values == 1]))
        # 312,095

        # How many >1: 216,354
        print(len(digests.values[digests.values > 1]))

        # How many layers > 2
        print(len(digests.values[digests.values > 2]))
        # 136054

        # > 50?: 9255
        print(len(digests.values[digests.values > 50]))

        # > 100? 3333
        print(len(digests.values[digests.values > 100]))

        # Make a histogram that shows this - but remove top repeated layer outlier
        filtered_digests = digests.values[digests.values > 100][1:]
        sns.histplot(
            pandas.DataFrame(filtered_digests, columns=["layers-repeated"]),
            x="layers-repeated",
        )
        plt.title(f"Layer Usage (Repetition) Across 2.8 Million Layers")
        plt.savefig(os.path.join(outdir, f"layer-repetition.png"))
        plt.clf()

        digests.to_csv(digests_file)
    else:
        digests = pandas.read_csv(digests_file, index_col=0)

    # Let's now look up what is in these layers! The top 100 are ok
    files = find_inputs(os.path.join(root, "data", "dockerfile", "registry"))

    # Add the layer count of each digest
    digests = pandas.DataFrame(digests)
    find_digests(files, digests, outdir)

    # Get rid of the NAN years (1970 and 1980)
    layer_counts = layer_counts[layer_counts.year >= 2014]
    layers_logs = [numpy.log(x) for x in layer_counts["layers"]]
    layer_counts["layers_logs"] = layers_logs

    make_plot(
        layer_counts,
        title=f"Number of layers per image by Year",
        tag="layers_per_image_log",
        ydimension="layers_logs",
        xdimension="year",
        outdir=outdir,
        ext="png",
        plotname="by_year",
        hue="year",
        palette=palette,
        plot_type="bar",
        xlabel="Year",
        ylabel="Layers per image (log)",
    )

    make_plot(
        layer_counts,
        title=f"Number of layers per image by Year",
        tag="layers_per_image",
        ydimension="layers",
        xdimension="year",
        outdir=outdir,
        ext="png",
        plotname="by_year",
        hue="year",
        palette=palette,
        plot_type="bar",
        xlabel="Year",
        ylabel="Layers per image",
    )

    plt.figure(figsize=(30, 12))
    make_plot(
        by_year,
        title=f"Mean layer sizes by Year",
        tag="size_by_year",
        ydimension="size_log",
        xdimension="year",
        outdir=outdir,
        ext="png",
        plotname="size_by_year",
        hue="year",
        palette=palette,
        plot_type="bar",
        xlabel="Year",
        ylabel="Log of Size (bytes)",
    )

    make_plot(
        df_by_year,
        title=f"Layer sizes by Year",
        tag="all_size_by_year",
        ydimension="size_log",
        xdimension="year",
        outdir=outdir,
        ext="png",
        plotname="all_size_by_year",
        hue="year",
        palette=palette,
        plot_type="bar",
        xlabel="Year",
        ylabel="Log Size (bytes)",
    )

    # It doesn't look like layer sizes are changing that much -
    # let's look at sum across images.
    summed_uri = pandas.DataFrame(columns=["uri", "size", "year", "size_log"])
    idx = 0
    for item, size in df.groupby(["uri", df.created_dt.dt.year])["size"].sum().items():
        summed_uri.loc[idx, :] = item[0], size, item[1], numpy.log(size)
        idx += 1

    summed_uri = summed_uri[summed_uri.year >= 2010]

    make_plot(
        summed_uri,
        title=f"Total Image Sizes by Year",
        tag="total_size_by_year",
        ydimension="size_log",
        xdimension="year",
        outdir=outdir,
        ext="png",
        plotname="total_size_by_year",
        hue="year",
        palette=palette,
        plot_type="bar",
        xlabel="Year",
        ylabel="Log of Size (bytes)",
    )

    # These are log sizes - to get a sense of the actual sizes
    # These are for individual layers
    print(f'Mean by layer: {df_by_year["size"].mean()}')
    print(f'Std by layer: {df_by_year["size"].std()}')
    print(f'Min by layer: {df_by_year["size"].min()}')
    print(f'Max by layer: {df_by_year["size"].max()}')

    # Mean by layer: 32982115.600011025
    # Std by layer: 203136133.56106418
    # Min by layer: 32
    # Max by layer: 11265416851

    print(f'Mean by image: {summed_uri["size"].mean()}')
    print(f'Std by image: {summed_uri["size"].std()}')
    print(f'Min by image: {summed_uri["size"].min()}')
    print(f'Max by image: {summed_uri["size"].max()}')

    # Mean by image: 18349246051.69792
    # Std by image: 79008670679.2305
    # Min by image: 1376848
    # Max by image: 2077795078486

    # Those are bytes - convert to GB
    print(f'Mean by image: {convert_size(summed_uri["size"].mean())}')
    print(f'Std by image: {convert_size(summed_uri["size"].std())}')
    print(f'Min by image: {convert_size(summed_uri["size"].min())}')
    print(f'Max by image: {convert_size(summed_uri["size"].max())}')

    # Mean by image: 17.09 GB
    # Std by image: 73.58 GB
    # Min by image: 1.31 MB
    # Max by image: 1.89 TB

    # Print mean image size by year:
    years = summed_uri.year.unique()
    years.sort()
    for year in years:
        subset = summed_uri[summed_uri.year == year]
        print(f"=== YEAR {year}")
        print(f'Mean by image: {convert_size(subset["size"].mean())}')
        print(f'Std by image: {convert_size(subset["size"].std())}')
        print(f'Min by image: {convert_size(subset["size"].min())}')
        print(f'Max by image: {convert_size(subset["size"].max())}')


def get_category(uri, categories):
    category = "unknown"
    if uri in categories["machine-learning"]:
        category = "machine-learning"
    elif uri in categories["rseng"]:
        category = "rseng"
    # docker.io library is often not included
    if "docker.io" in uri and category == "unknown":
        simple_uri = uri.replace("docker.io/library/", "")
        if simple_uri in categories["machine-learning"]:
            category = "machine-learning"
        elif simple_uri in categories["rseng"]:
            category = "rseng"
    return category


def derive_layer_counts(df):
    # Count number of layers per unique uri - each is likely within a year already
    # We can separate into years after
    layer_counts = pandas.DataFrame(columns=["full_uri", "layers"])
    idx = 0

    # This index starts at 0
    for item, layer_count in df.groupby(["full_uri"])["layer_number"].max().items():
        layer_counts.loc[idx, :] = item, layer_count + 1
        idx += 1

    # We can't include year, but we can calculate a range of years
    years = []
    uris = []
    repeated = 0
    missing = 0
    for row in layer_counts.iterrows():
        year = df.loc[df.full_uri == row[1].full_uri].year
        year = list(set(year.values))
        if len(year) == 1:
            years.append(year)
            uris.append(row[1].full_uri)
        else:
            repeated += 1
    layer_counts["year"] = years
    return layer_counts


def parse_manifests(files, args, categories, db_file):
    """
    Given a listing of files, parse into results data frame
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    create_sql = """
    CREATE TABLE IF NOT EXISTS manifests (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      full_uri TEXT NOT NULL,
      uri TEXT NOT NULL,
      tag TEXT NOT NULL,
      layer_number INTEGER NOT NULL,
      architecture TEXT NOT NULL,
      digest TEXT NOT NULL,
      os TEXT NOT NULL,
      size INTEGER NOT NULL,
      schema_version TEXT NOT NULL,
      category TEXT NOT NULL,
      created_at DATETIME
    );
    """
    cursor.execute(create_sql)
    conn.commit()

    # fields are consistent
    fields = '("full_uri", "uri", "tag", "layer_number", "architecture", "digest", "os", "size", "schema_version", "category", "created_at")'

    # manifests has the following:
    # shared digests across images
    # distribution of sizes in different contexts
    # distribution of platforms / arch
    seen = set()
    for filename in files:
        if filename in seen:
            continue
        print(f"Parsing filename {filename}")
        parsed = os.path.relpath(filename, root).split("registry", 1)[-1].strip(os.sep)
        uri, _ = parsed.rsplit(os.sep, 1)
        item = utils.read_json(filename)

        if "manifests" not in item:
            continue

        category = get_category(uri, categories)

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
                values = f"('{full_uri}', '{uri}', '{tag}', {i}, '{arch}', '{digest}', '{opsys}', {size}, '{sv}', '{category}', '{created_at}')"
                cursor.execute(f"INSERT INTO manifests {fields} VALUES {values}")

        conn.commit()
        seen.add(filename)

    # check
    # res = cursor.execute("SELECT * FROM manifests;")
    # res.fetchone()
    conn.close()


def clean(input_data):
    import string

    lowercase = input_data.lower()
    return [
        x.strip()
        for x in re.sub(re.escape(string.punctuation), "", lowercase).split(" ")
        if x.strip()
    ]


def find_digests(files, digests, outdir):
    """
    Given a set of digests, look up the associated content.

    To do this we need the digest and the layer count.
    """
    # Let's get the top 100
    to_look_for = digests.index[0:100]

    # Database file
    db_file = os.path.join(root, "data", "dockerfile", "data-frame.db")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    to_look = {}
    for digest in to_look_for:
        cursor.execute(f"select * from manifests where digest = '{digest}';")
        result = cursor.fetchall()
        full_uri = result[1]
        if full_uri not in to_look:
            to_look[full_uri] = {}
        to_look[full_uri][digest] = {"layer_number": result[4]}

    utils.write_json(to_look, os.path.join(outdir, "top-100-digest-locations.json"))
    conn.close()

    for filename in files:
        parsed = os.path.relpath(filename, root).split("registry", 1)[-1].strip(os.sep)
        uri, _ = parsed.rsplit(os.sep, 1)
        item = utils.read_json(filename)

        # This is a manifest list
        for tag, cfg in item.get("configs", {}).items():
            full_uri = f"{uri}:{tag}"
            if full_uri not in to_look:
                continue
            for digest, manifest in to_look[full_uri].items():
                layer_number = manifest["layer_number"]
                to_look[full_uri][digest]["layer_content"] = cfg["history"][
                    layer_number
                ]
        break

    utils.write_json(to_look, os.path.join(outdir, "top-100-digest-locations.json"))

    # Print the counts / items to the screen
    # Note that I put this into a file
    print("# Top Layer Contents")
    for full_uri, manifest in to_look.items():
        for digest, content in manifest.items():
            count = digests[digests.index == digest].values[0]
            print(f"    Digest: {digest}")
            print(f"  Found In: {full_uri}")
            print(f"   Layer #: {content['layer_number']}")
            print(f"References: {count}")
            if "comment" in content:
                print(f"   Comment: {content['comment']}")
            print(f"   Created: {content['layer_content']['created']}")
            print(f"   Content: {content['layer_content']['created_by']}")
            print()


def parse_configs(files, args, categories, db_file):
    """
    We want to find similarity between layers by way of tokenizing -> top2vec.

    This will generate the corpus we can use.
    """
    root_dir = os.path.dirname(args.results)

    # This is for images
    fd = open(os.path.join(root_dir, "dockerfile-image-corpus.txt"), "w")

    # This is layers, all of them
    fdlayers_all = open(os.path.join(root_dir, "dockerfile-layer-corpus.txt"), "w")

    # This is for unique layers
    fdlayers = open(os.path.join(root_dir, "dockerfile-unique-layer-corpus.txt"), "w")

    # Metadata for each
    meta = open(os.path.join(root_dir, "dockerfile-image-index.txt"), "w")
    metalayers_all = open(os.path.join(root_dir, "dockerfile-layer-index.txt"), "w")
    metalayers = open(os.path.join(root_dir, "dockerfile-unique-layer-index.txt"), "w")

    # This gets replaced with a space (to make new tokens)
    punctuation = "('|\"|;|:|=|_|-|\n|\t|#|[.]|[*]|[&])"

    # This gets removed
    removed = "(<|>|{|}|[|]|[)]|[(]|[]]|[[]|[$]|[/])"

    total = len(files)
    seen = {}
    for i, filename in enumerate(files):
        print(f"Parsing {i} of {total}", end="\r")
        parsed = os.path.relpath(filename, root).split("registry", 1)[-1].strip(os.sep)
        uri, _ = parsed.rsplit(os.sep, 1)
        item = utils.read_json(filename)

        # This is a manifest list
        for tag, cfg in item.get("configs", {}).items():
            if "history" not in cfg:
                continue
            tokens = []
            for idx, entry in enumerate(cfg["history"]):
                if "created_by" not in entry:
                    continue
                # Get rid of punctuation that could make commands different
                content = re.sub(punctuation, " ", entry["created_by"])
                content = re.sub(removed, " ", content)
                line = content.lower().split()

                # Get rid of single characters
                tokens += [x for x in line if len(x) > 1]

                # Also get rid of shas and commits
                tokens = [x for x in tokens if len(x) != 64 and len(x) != 40]

                # Try adding layers only once, and count uniqueness here
                assembled = " ".join(tokens)

                # This file has all layers
                fdlayers_all.write(assembled + "\n")
                metalayers_all.write(filename + " " + tag + " " + str(idx) + "\n")

                if assembled not in seen:
                    seen[assembled] = -1
                seen[assembled] += 1

                # Don't add layers we've seen
                if seen[assembled] >= 1:
                    continue
                fdlayers.write(assembled + "\n")
                metalayers.write(filename + " " + tag + " " + str(idx) + "\n")

            # This has each image as one line
            fd.write(" ".join(tokens) + "\n")
            meta.write(filename + " " + tag + "\n")

    # We just need the count that the layers were repeated (identical)
    utils.write_json(seen, os.path.join(root_dir, "seen-layers-counts.json"))
    total = 0
    for _, count in seen.items():
        total += count

    # There are a total of 582391 duplicate layers
    print(f"There are a total of {len(seen)} duplicate layers")

    fdlayers.close()
    metalayers.close()
    fdlayers_all.close()
    metalayers_all.close()
    meta.close()
    fd.close()


def make_plot(
    df,
    title,
    tag,
    ydimension,
    xdimension,
    palette,
    xlabel,
    ylabel,
    ext="pdf",
    plotname="lammps",
    plot_type="violin",
    hue="experiment",
    outdir="img",
):
    """
    Helper function to make common plots.
    """
    plotfunc = sns.boxplot
    if plot_type == "violin":
        plotfunc = sns.violinplot

    ext = ext.strip(".")
    plt.figure(figsize=(12, 8))
    sns.set_style("dark")
    if plot_type == "violin":
        ax = plotfunc(
            x=xdimension, y=ydimension, hue=hue, data=df, linewidth=0.8, palette=palette
        )
    else:
        ax = plotfunc(
            x=xdimension,
            y=ydimension,
            hue=hue,
            data=df,
            linewidth=0.8,
            palette=palette,
            whis=[5, 95],
            dodge=False,
        )

    plt.title(title)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=14)
    ax.set_yticklabels(ax.get_yticks(), fontsize=14)
    plt.savefig(os.path.join(outdir, f"{tag}_{plotname}.{ext}"))
    plt.clf()


if __name__ == "__main__":
    main()
