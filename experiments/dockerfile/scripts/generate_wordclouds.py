#!/usr/bin/env python3


import argparse
import os
import sys
import rse.utils.file as utils
from top2vec import Top2Vec
import matplotlib.pyplot as plt

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
            "top2vec-with-doc2vec-dockerfile-image-learn.model",
        ),
    )
    parser.add_argument(
        "--outname",
        help="basename of output markdown",
        default="top2vec-jobspec-database.md",
    )
    return parser


# 19,856 topics! That is too many
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

    # Get topics, sizes and numbers
    topic_sizes, topic_nums = model.get_topic_sizes()

    number_topics = model.get_num_topics()
    print(f"There are {number_topics} topics")
    topic_words, word_scores, topic_nums = model.get_topics(number_topics)

    outdir = os.path.dirname(args.model)
    outdir = os.path.join(outdir, "wordcloud")
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for i, topic in enumerate(topic_nums):
        if i > 100:
            break
        print(f"Generating plot for {topic}")
        model.generate_topic_wordcloud(topic)
        print(" ".join(topic_words[i]))
        plt.savefig(
            os.path.join(outdir, f"{topic}-cloud.png"),
        )
        plt.clf()

    # Generate a README for them
    with open(os.path.join(outdir, "README.md"), "w") as fd:
        fd.write("# Topic Wordclouds\n")
        fd.write("> Top 100\n")
        for i, topic in enumerate(topic_nums):
            if i > 100:
                break
            image = f"{topic}-cloud.png"
            fd.write(f"\n## Topic {topic}\n")
            words = topic_words[i]
            fd.write("\n```console\n")
            fd.write(" ".join(words) + "\n")
            fd.write("```\n")
            fd.write(f"![{image}]({image})\n")


if __name__ == "__main__":
    main()
