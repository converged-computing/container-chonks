#!/usr/bin/env python3

import pandas
import argparse
import os
import sys
from top2vec import Top2Vec
import seaborn as sns
import seaborn as sns
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
            "top2vec-with-doc2vec-image-tokens-learn.model",
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

    # Note that we have similarity on the level of the image here
    sim = cosine_similarity(model.document_vectors)
    sims = pandas.DataFrame(sim)

    # model.document_vectors.shape
    # This is the number of images
    # (309317, 300)

    # minimum should be -1
    # sims.min().min()
    # -0.5011855

    # max should be 1
    # sims.max().max()
    # 1.0000006

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
    print(f"{range_2} are in range -0.3 to -0.1")
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
    print(f"{range_4} are in range -0.1 to 0.0")
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

    # 26580.0 are in range -0.5 to -0.4
    # 10214756.0 are in range -0.4 to -0.3
    # 434408772.0 are in range -0.3 to -0.1
    # 4817538814.0 are in range -0.2 to -0.1
    # 14237460310.0 are in range -0.1 to 0.0
    # 12876001621.0 are in range 0.0 to 0.1
    # 6396681060.0 are in range 0.1 to 0.2
    # 4004250693.0 are in range 0.2 to 0.3
    # 2690671058.0 are in range 0.3 to 0.4
    # 2690671058.0 are in range 0.4 to 0.5
    # 632519754.0 are in range 0.5 to 0.6
    # 283613155.0 are in range 0.6 to 0.7
    # 100464254.0 are in range 0.7 to 0.8
    # 32083760.0 are in range 0.8 to 0.9
    # 10451894.5 are in range 0.9 to 1.0

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

    df.to_csv(
        os.path.join(here, "data", "dockerfile", "image-similarity-histogram.csv")
    )
    outfile = os.path.join(here, "img", "image-similarity-histogram.png")
    plt.figure(figsize=(12, 6))
    sns.barplot(df, y="counts", x="cosine")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.title("Cosine Similarity for 300K Docker Images")
    plt.savefig(outfile)
    plt.clf()


if __name__ == "__main__":
    main()
