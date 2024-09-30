#!/usr/bin/env python3

import pandas
import argparse
import os
import sys
from top2vec import Top2Vec
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

here = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(here)


def get_parser():
    parser = argparse.ArgumentParser(description="top2vec")
    parser.add_argument(
        "--model",
        help="model input file",
        default=os.path.join(
            root,
            "data",
            "dockerfile",
            "top2vec-with-top2vec-unique-layers-learn.model",
        ),
    )
    return parser


def count_values_in_range(series, range_min, range_max):
    return series.between(left=range_min, right=range_max).sum()


def main():
    """
    Generate cosine distance matrix from vectors.
    """
    parser = get_parser()
    args, _ = parser.parse_known_args()

    # Note that I had to run this on a large VM to not get killed
    model_path = args.model
    if not os.path.exists(model_path):
        sys.exit(f"Model path {model_path} does not exist.")
    model = Top2Vec.load(model_path)

    # This is similarity on the level of layers
    # model.document_vectors.shape
    #  (582391, 300)
    model.document_vectors.shape
    chunk_size = 10000
    matrix_len = model.document_vectors.shape[0]

    def similarity_cosine_by_chunk(model, start, end):
        matrix_len = model.document_vectors.shape[0]  # Not sparse numpy.ndarray
        if end > matrix_len:
            end = matrix_len
        return cosine_similarity(
            X=model.document_vectors[start:end], Y=model.document_vectors
        )

    df = None
    total = int(matrix_len / chunk_size)
    for i, chunk_start in enumerate(range(0, matrix_len, chunk_size)):
        print(f"Processing chunk {i} of {total}")
        cosine_similarity_chunk = similarity_cosine_by_chunk(
            model, chunk_start, chunk_start + chunk_size
        )
        sims = pandas.DataFrame(cosine_similarity_chunk)
        if df is None:
            df = get_ranges(sims)
        else:
            updated = get_ranges(sims)
            new_counts = updated["counts"] + df["counts"]
            df["counts"] = new_counts
        print(df)

    # Handle cosine_similarity_chunk  ( Write it to file_timestamp and close the file )
    # Do not open the same file again or you may end up with out of memory after few chunks
    df.to_csv(os.path.join(root, "data", "dockerfile", "layer-sims-counts.csv"))
    outfile = os.path.join(root, "img", "layer-similarity-histogram.png")
    plt.figure(figsize=(12, 6))
    sns.barplot(df, y="counts", x="cosine")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.title("Cosine Similarity for 582K Unique Image Layers")
    plt.savefig(outfile)
    plt.clf()


def get_ranges(sims):
    """
    Get range counts for a similarity matrix chunk
    """
    range_0 = (
        sims.apply(
            func=lambda row: count_values_in_range(row, -0.5, -0.4), axis=1
        ).sum()
        / 2
    )
    print(f"{range_0} are in range -0.5 to -0.4")
    range_1 = (
        sims.apply(
            func=lambda row: count_values_in_range(row, -0.4, -0.3), axis=1
        ).sum()
        / 2
    )
    print(f"{range_1} are in range -0.4 to -0.3")
    range_2 = (
        sims.apply(
            func=lambda row: count_values_in_range(row, -0.3, -0.2), axis=1
        ).sum()
        / 2
    )
    print(f"{range_2} are in range -0.3 to -0.2")
    range_3 = (
        sims.apply(
            func=lambda row: count_values_in_range(row, -0.2, -0.1), axis=1
        ).sum()
        / 2
    )
    print(f"{range_3} are in range -0.2 to -0.1")
    range_4 = (
        sims.apply(func=lambda row: count_values_in_range(row, -0.1, 0.0), axis=1).sum()
        / 2
    )
    print(f"{range_4} are in range -0.1 to -0.0")
    range_5 = (
        sims.apply(func=lambda row: count_values_in_range(row, 0.0, 0.1), axis=1).sum()
        / 2
    )
    print(f"{range_5} are in range 0.0 to 0.1")
    range_6 = (
        sims.apply(func=lambda row: count_values_in_range(row, 0.1, 0.2), axis=1).sum()
        / 2
    )
    print(f"{range_6} are in range 0.1 to 0.2")
    range_7 = (
        sims.apply(func=lambda row: count_values_in_range(row, 0.2, 0.3), axis=1).sum()
        / 2
    )
    print(f"{range_7} are in range 0.2 to 0.3")
    range_8 = (
        sims.apply(func=lambda row: count_values_in_range(row, 0.3, 0.4), axis=1).sum()
        / 2
    )
    print(f"{range_8} are in range 0.3 to 0.4")
    range_9 = (
        sims.apply(func=lambda row: count_values_in_range(row, 0.4, 0.5), axis=1).sum()
        / 2
    )
    print(f"{range_8} are in range 0.4 to 0.5")
    range_10 = (
        sims.apply(func=lambda row: count_values_in_range(row, 0.5, 0.6), axis=1).sum()
        / 2
    )
    print(f"{range_10} are in range 0.5 to 0.6")
    range_11 = (
        sims.apply(func=lambda row: count_values_in_range(row, 0.6, 0.7), axis=1).sum()
        / 2
    )
    print(f"{range_11} are in range 0.6 to 0.7")
    range_12 = (
        sims.apply(func=lambda row: count_values_in_range(row, 0.7, 0.8), axis=1).sum()
        / 2
    )
    print(f"{range_12} are in range 0.7 to 0.8")
    range_13 = (
        sims.apply(func=lambda row: count_values_in_range(row, 0.8, 0.9), axis=1).sum()
        / 2
    )
    print(f"{range_13} are in range 0.8 to 0.9")
    range_14 = (
        sims.apply(func=lambda row: count_values_in_range(row, 0.9, 1.0), axis=1).sum()
        / 2
    )
    print(f"{range_14} are in range 0.9 to 1.0")

    ranges = [
        range_0,
        range_1,
        range_2,
        range_3,
        range_4,
        range_5,
        range_6,
        range_7,
        range_8,
        range_9,
        range_10,
        range_11,
        range_12,
        range_13,
        range_14,
    ]
    y = [
        "-0.5 to -0.4",
        "-0.4 to -0.3",
        "-0.3 to -0.2",
        "-0.2 to -0.1",
        "-0.1 to 0.0",
        "0.0 to 0.1",
        "0.1 to 0.2",
        "0.2 to 0.3",
        "0.3 to 0.4",
        "0.4 to 0.5",
        "0.5 to 0.6",
        "0.6 to 0.7",
        "0.7 to 0.8",
        "0.8 to 0.9",
        "0.9 to 1.0",
    ]

    df = pandas.DataFrame()
    df["counts"] = ranges
    df["cosine"] = y
    return df


if __name__ == "__main__":
    main()
