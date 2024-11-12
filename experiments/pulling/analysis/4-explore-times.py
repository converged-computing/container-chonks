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
    parser = argparse.ArgumentParser(description="Times Explorer")
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
            seconds = elapsed.seconds

        # parse layers, total size, and size per layer from tag
        tag = container.split(":")[-1]
        layers, rest = tag.split("-", 1)
        total_size = int(rest.split("-")[2])
        # subtract base image
        total_size -= 5000000
        layers = int(layers)
        layer_size = total_size / layers

        # parse all events for absolute timestamp
        # For these we want absolute timestamps to compare across
        # because we need to understand variation between nodes
        for event_name in ["pulled", "pulling", "scheduled", "created", "started"]:
            if event_name not in item["events"]:
                continue
            # For these, calculate a difference.
            previous_event = {"created": "pulled", "started": "created"}
            timestamp = item["events"][event_name]["timestamp"]
            parsed_timestamp = datetime.strptime(timestamp, timestamp_format)
            df.loc[idx, :] = [
                event_name + "-timestamp",
                parsed_timestamp.timestamp(),
                container,
                layers,
                total_size,
                layer_size,
                experiment,
                size,
            ]
            idx += 1
            if event_name in previous_event:
                previous_timestamp = item["events"][previous_event[event_name]][
                    "timestamp"
                ]
                previous_timestamp = datetime.strptime(
                    previous_timestamp, timestamp_format
                )
                elapsed = parsed_timestamp - previous_timestamp
                event_seconds = elapsed.seconds
                df.loc[idx, :] = [
                    event_name,
                    event_seconds,
                    container,
                    layers,
                    total_size,
                    layer_size,
                    experiment,
                    size,
                ]
                idx += 1
            continue

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

    save_prefix = save_prefix or "pull_times_experiment_type"

    # Assume containers need at least 20 seconds to pull
    if filter_below is not None:
        df = df[df.duration > filter_below]

    # There should only be one experiment here - raise an error if not the case!
    if len(df.experiment.unique()) != 1:
        raise ValueError("Found more than one experiment in the df, should not happen")

    experiment = list(df.experiment.unique())[0]

    # For now, assume just one layer size (what I did)
    if len(df.layers.unique()) > 1:
        raise ValueError("Found more than one layer count in the df, should not happen")

    # For each size, for each container, calculate the max-min timestmap
    # (how long it takes for all nodes to do same operation)
    ts_df = pandas.DataFrame(
        columns=["nodes", "event", "time_range_seconds", "container"]
    )
    idx = 0
    for size in df.nodes.unique():
        size_df = df[df.nodes == size]
        for container in df.container.unique():
            container_df = size_df[size_df.container == container]
            for event in [
                "pulled-timestamp",
                "pulling-timestamp",
                "scheduled-timestamp",
                "created-timestamp",
                "started-timestamp",
            ]:
                subset = container_df[container_df.event == event]
                duration = subset.duration.max() - subset.duration.min()
                ts_df.loc[idx, :] = [
                    size,
                    event.replace("-timestamp", ""),
                    duration,
                    container,
                ]
                idx += 1

    # Change container to just be size
    ts_df.container = [x.split(":")[-1] for x in ts_df.container]
    ts_df['image-size'] = [x.replace("9-layers-size-", "").replace('-', ' ') for x in ts_df.container]

    colors = sns.color_palette("hls", len(ts_df['image-size'].unique()))
    hexcolors = colors.as_hex()
    sizes = list(ts_df['image-size'].unique())
    sizes.sort()
    palette = collections.OrderedDict()
    for t in sizes:
        palette[t] = hexcolors.pop(0)

    for event in ts_df.event.unique():
        event_df = ts_df[ts_df.event == event]
        plotname=f"event_durations_size_{event}_{experiment}"
        ax = make_plot(
            event_df,
            title=f"Time Differences Between Event \"{event.capitalize()}\" Across Nodes",
            ydimension="time_range_seconds",
            xdimension="nodes",
            outdir=outdir,
            ext="png",
            plotname=plotname,
            hue="image-size",
            palette=palette,
            plot_type="bar",
            xlabel="Number of Nodes",
            ylabel="Latest-Earliest (Seconds)",
            # do_log=True,
            # With log, no ylimit
            # ylim=None,
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
    plotfunc = sns.lineplot
    if plot_type == "violin":
        plotfunc = sns.violinplot

    ext = ext.strip(".")
    plt.figure(figsize=(7, 3))
    sns.set_style("dark")
    if plot_type == "violin":
        ax = plotfunc(
            x=xdimension, y=ydimension, hue=hue, data=df, linewidth=0.8, palette=palette, marker="o",
        )
    else:
        ax = plotfunc(
            x=xdimension,
            y=ydimension,
            hue=hue,
            data=df,
            linewidth=1.8,
            palette=palette,
            # whis=[5, 95],
            # dodge=True,
        )
        # This range is specifically for pulling times -
        # so the ranges are equivalent
        if ylim is not None:
            ax.set(ylim=ylim)

    if do_log:
        plt.yscale("log")
    plt.title(title)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=14)
    ax.set_yticklabels(ax.get_yticks(), fontsize=14)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{plotname}.png"))
    plt.clf()
    return ax

if __name__ == "__main__":
    main()
