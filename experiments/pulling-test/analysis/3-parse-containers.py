#!/usr/bin/env python3

import argparse
import collections
import json
import os
import re
import sys
from datetime import datetime

import matplotlib.pylab as plt
import pandas
import seaborn as sns

here = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(here)

timestamp_format = "%Y-%m-%dT%H:%M:%SZ"


def get_parser():
    parser = argparse.ArgumentParser(description="Dockerfile Parser")
    parser.add_argument(
        "--data",
        default=os.path.join(here, "data"),
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


def main():
    parser = get_parser()
    args, _ = parser.parse_known_args()

    if not os.path.exists(args.data):
        sys.exit(f"{args.data} does not exist.")

    # Output directory for images
    data_dir = os.path.join(args.data, "img")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Read in raw times, which also has cloud, etc.
    times = read_json(os.path.join(args.data, "raw-times.json"))

    # Parse them into data frame too.
    times_df = parse_times(times)
    plot_times(times_df, data_dir)


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


def parse_times(times):
    """
    Read events and turn into data frame with container pull times
    """
    df = pandas.DataFrame(
        columns=[
            "event",
            "duration",
            "container",
            "layers",
            "total_size",
            "size_per_layer",
            "experiment",
            "nodes",
        ]
    )
    idx = 0
    for _, item in times.items():
        # The only experiment without a stated size is aws eks gpu, size 16
        experiment = item["experiment"]
        size = item["size"]
        container = item.get("container")
        if not container and "pulled" in item["events"]:
            container = (
                re.search('["].*["]', item["events"]["pulled"]["message"])
                .group()
                .strip('"')
            )

        if not container or "converged-computing" not in container:
            continue

        # We can do our own calculation based on timestamps here
        # These seem to be better in terms of granularity
        seconds = None
        # We can derive pull plus waiting from the message here
        # This is better data
        if "pulled" in item["events"] and seconds is None:
            message = item["events"]["pulled"]["message"]
            # If it's already pulled, don't count it
            if "already present on machine" in message.lower():
                continue
            time_pulled = re.search("[(].*[)]", message)
            time_pulled = time_pulled.group().split(" ")[0].replace("(", "")
            # parse time pulled
            seconds = parse_time_pulled(time_pulled)

        elif "pulling" in item["events"] and "pulled" in item["events"]:
            start = item["events"]["pulling"]["timestamp"]
            end = item["events"]["pulled"]["timestamp"]
            parsed_end = datetime.strptime(end, timestamp_format)
            parsed_start = datetime.strptime(start, timestamp_format)
            elapsed = parsed_end - parsed_start
            seconds = elapsed.min.seconds + elapsed.seconds

        # parse layers, total size, and size per layer from tag
        tag = container.split(":")[-1]
        layers, rest = tag.split("-", 1)
        total_size = int(rest.split("-")[2])
        # subtract base image
        total_size -= 5000000
        layers = int(layers)
        layer_size = total_size / layers
        if seconds is not None:
            df.loc[idx, :] = [
                "pulled",
                seconds,
                container,
                layers,
                total_size,
                layer_size,
                experiment,
                size,
            ]
            idx += 1
    return df


def plot_times(df, outdir):
    """
    Plot containers, generating images in the output directory.
    """
    plot_containers(df, outdir)


def plot_containers(df, outdir, save_prefix=None, filter_below=None, suffix=None):
    """
    Given an output directory, plot image to show pull times.
    """
    # Print the total sum of pull times
    experiment = df.experiment.unique()[0]
    print(f"Total duration (sum) for experiment {experiment}:")
    print(df.duration.sum())

    colors = sns.color_palette("hls", 20)
    save_prefix = save_prefix or "pull_times_experiment_type"

    # Assume containers need at least 20 seconds to pull
    if filter_below is not None:
        df = df[df.duration > filter_below]

    # There should only be one experiment here - raise an error if not the case!
    if len(df.experiment.unique()) != 1:
        raise ValueError("Found more than one experiment in the df, should not happen")

    experiment = list(df.experiment.unique())[0]

    # Let's break into two plots, one for each number of layers
    # within a plot, x axis is the cluster nodes (size) and color is image size
    for layers in df.layers.unique():
        subset = df[df.layers == layers]
        hexcolors = colors.as_hex()
        sizes = list(subset.nodes.unique())
        sizes.sort()
        palette = collections.OrderedDict()
        for t in sizes:
            palette[t] = hexcolors.pop(0)

        title = f"Container Pull times for Experiment with {layers} Layers, ghcr.io"
        if experiment == "run2":
            title = f"Container Pull times for Experiment with {layers} Layers, gcr.io"

        make_plot(
            subset,
            title=title,
            ydimension="duration",
            xdimension="total_size",
            outdir=outdir,
            ext="png",
            plotname=f"pull_times_duration_by_size_{experiment}_{layers}_layers_log",
            hue="nodes",
            palette=palette,
            plot_type="bar",
            xlabel="Total Image Size (bytes)",
            ylabel="Pull time (log of seconds)",
            do_log=True,
            # With log, no ylimit
            ylim=None,
        )

        ylim = None
        if experiment in ["run1", "run2", "run3"]:
            ylim = (0, 180)

        # Without log, set ylimit
        make_plot(
            subset,
            title=title,
            ydimension="duration",
            xdimension="total_size",
            outdir=outdir,
            ext="png",
            plotname=f"pull_times_duration_by_size_{experiment}_{layers}_layers",
            hue="nodes",
            palette=palette,
            plot_type="bar",
            xlabel="Total Image Size (bytes)",
            ylabel="Pull time (seconds)",
            ylim=ylim,
        )


def make_plot(
    df,
    title,
    ydimension,
    xdimension,
    xlabel,
    ylabel,
    palette=None,
    ext="pdf",
    plotname="lammps",
    plot_type="violin",
    hue=None,
    outdir="img",
    do_log=False,
    ylim=None,
):
    """
    Helper function to make common plots.
    """
    plotfunc = sns.boxplot
    if plot_type == "violin":
        plotfunc = sns.violinplot

    ext = ext.strip(".")
    plt.figure(figsize=(16, 8))
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
            dodge=True,
        )
        # This range is specifically for pulling times -
        # so the ranges are equivalent
        if ylim is not None:
            ax.set(ylim=ylim)

    if do_log:
        plt.yscale("log")
    plt.title(title)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=14)
    ax.set_yticklabels(ax.get_yticks(), fontsize=14)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{plotname}.{ext}"))
    plt.clf()


if __name__ == "__main__":
    main()
