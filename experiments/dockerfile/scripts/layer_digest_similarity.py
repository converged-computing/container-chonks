#!/usr/bin/env python3

import sqlite3
import pandas
import argparse
import os
import sys
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

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
    return parser


def count_values_in_range(series, range_min, range_max):
    return series.between(left=range_min, right=range_max).sum()


def main():
    """
    Generate cosine distance matrix from digest Jacaard similarity.
    """
    parser = get_parser()
    args, _ = parser.parse_known_args()

    # Read back into data frame
    conn = sqlite3.connect(args.database)
    cursor = conn.cursor()

    manifest_df = pandas.read_sql_query(
        "SELECT * from manifests",
        conn,
        parse_dates={"datetime": "%Y-%m-%d %H:%M:%S"},
    )
    conn.close()

    import IPython

    IPython.embed()
    sys.exit()

    def similarity_cosine_by_chunk(manifest_df, start, end):
        matrix_len = manifest_df.shape[0]  # Not sparse numpy.ndarray
        if end > matrix_len:
            end = matrix_len
        return cosine_similarity(
            X=model.document_vectors[start:end], Y=model.document_vectors
        )

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
    m = sns.clustermap(sims, vmin=0.0, vmax=1.0, annot=False, cmap="BrBG")
    plt.savefig(os.path.join(root, "img", f"cluster-layer-digest-similarity.png"))
    plt.clf()


if __name__ == "__main__":
    main()
