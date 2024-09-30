#!/usr/bin/env python3

import sqlite3
import pandas
import argparse
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

here = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(here)


def get_parser():
    parser = argparse.ArgumentParser(description="top2vec")
    parser.add_argument(
        "--database",
        help="database file",
        default=os.path.join(
            root,
            "data",
            "dockerfile",
            "data-frame.db",
        ),
    )
    parser.add_argument(
        "--skip-sims",
        help="Skip calculating similarities",
        default=False,
        action="store_true",
    )
    return parser


def main():
    """
    Generate cosine distance matrix from digest Jacaard similarity.
    """
    parser = get_parser()
    args, _ = parser.parse_known_args()

    # Read back into data frame
    conn = sqlite3.connect(args.database)

    manifest_df = pandas.read_sql_query(
        "SELECT * from manifests",
        conn,
        parse_dates={"datetime": "%Y-%m-%d %H:%M:%S"},
    )
    conn.close()

    # Calculate for only unique URIs - we assume within a URI (That has many tags)
    # the images are relatively similar. Each uri + tag will have multiple layers
    subset = pandas.DataFrame(columns=manifest_df.columns)
    unique_uris = manifest_df.uri.unique()
    total = len(unique_uris)
    for i, unique_uri in enumerate(unique_uris):
        print(f"Parsing {i} of {total}", end="\r")
        # First try for "latest"
        tmp = manifest_df[manifest_df.uri == unique_uri]
        tag = "latest"
        tmp_tagged = tmp[tmp.tag == tag]
        if tmp_tagged.shape[0] == 0:
            tag = tmp.iloc[0].tag
            tmp_tagged = tmp[tmp.tag == tag]
        subset = pandas.concat([subset, tmp_tagged])

    subset.to_csv(os.path.join(root, "data", "dockerfile", "full_uri_subset.csv"))

    # Calculate pairwise jacaard similarity - should be feasible with smaller set
    # it still takes 45min- an hour
    if not args.skip_sims:
        calculate_similarity(unique_uris, subset)

    # Get mean, and +/- 1 std for total size of layers
    items = list(manifest_df.groupby("full_uri")["size"])
    values = [x[1].values[0] for x in items]

    import IPython

    IPython.embed()
    # We can use these ranges for experiment
    show_summary(values, "Layers")
    print()

    # Now do for total image size
    by_size = manifest_df.groupby("full_uri")["size"].sum()
    show_summary(by_size.values, "Images")

    # Finally, the number of layers
    # This had to run overnight for me (slow)
    layer_digest_data = os.path.join(
        root, "data", "dockerfile", "image-layer-counts.csv"
    )
    if not os.path.exists(layer_digest_data):
        print("Calculating layer counts...")
        counts = pandas.DataFrame(columns=["full_uri", "number_layers"])
        unique_uris = list(manifest_df.full_uri.unique())
        total = len(unique_uris)
        idx = 0
        for i, uri in enumerate(unique_uris):
            print(f"{i} of {total}", end="\r")
            counts.loc[idx, :] = [
                uri,
                manifest_df[manifest_df.full_uri == uri].shape[0],
            ]
            idx += 1
        counts.to_csv(layer_digest_data)
    else:
        counts = pandas.read_csv(layer_digest_data, index_col=0)
    show_summary(counts["number_layers"].values, "Number of Layers")


def show_summary(values, label):
    """
    Print quartiles and medians for a list of values
    """
    mean = np.mean(values)
    std = np.std(values)
    print(f"{label} Mean and std: {mean}, {std}")
    for percentile in [25, 50, 75, 100]:
        print(f"{label} Percentile {percentile}: {np.percentile(values, percentile)}")
    median = np.median(values)
    print(f"{label} Median: {median}")
    print(f"{label} Median +1 quartile: {median + np.percentile(values, 25)}")
    print(f"{label} Median -1 quartile: {median - np.percentile(values, 25)}")


def calculate_similarity(unique_uris, subset):
    total = len(unique_uris)
    sims = pandas.DataFrame(columns=unique_uris, index=unique_uris)
    for i, a_label in enumerate(unique_uris):
        print(f"Processing {i} of {total}")
        for b_label in unique_uris:
            if a_label == b_label:
                sims.loc[a_label, b_label] = 1
                continue
            A = set(subset[subset.uri == a_label].digest.tolist())
            B = set(subset[subset.uri == b_label].digest.tolist())
            # Don't try to divide by zero
            union = len(A.union(B))
            if union == 0:
                sims.loc[a_label, b_label] = 0
                continue
            score = len(A.intersection(B)) / union
            sims.loc[a_label, b_label] = score

    sims.to_csv(os.path.join(root, "data", "dockerfile", "full_uri_similarity.csv"))

    # Calculate similarity metrics and plot
    mean = np.mean(sims.values)
    std = np.std(sims.values)
    print(f"Mean Jacaard score for digests is {mean} with std {std}")

    plt.figure(figsize=(36, 36))
    sims = sims.astype(float)

    # Ensure range is 0 to 1 to match similarity experiment plots
    sns.clustermap(sims, vmin=0.0, vmax=1.0, annot=False, cmap="BrBG")
    plt.savefig(os.path.join(root, "img", "cluster-layer-digest-similarity.png"))
    plt.clf()


if __name__ == "__main__":
    main()
