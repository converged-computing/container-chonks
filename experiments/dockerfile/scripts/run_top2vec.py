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
    parser = argparse.ArgumentParser(description="word2vec")
    parser.add_argument(
        "--input",
        help="tokenized jobspec files",
        default=os.path.join(root, "data", "dockerfile", "dockerfile-corpus.txt"),
    )
    return parser


def main():
    """
    Generate cosine distance matrix from vectors.
    """
    parser = get_parser()
    args, _ = parser.parse_known_args()
    if not os.path.exists(args.input):
        sys.exit(f"{args.input} does not exist.")

    corpus = [x.strip() for x in utils.read_file(args.input)]

    outdir = os.path.dirname(args.input)
    outdir = os.path.join(outdir, "top2vec")

    # Note I was running this on a VM - YOLO
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # Note that I had to run this on a large VM to not get killed
    model_path = os.path.join(outdir, "top2vec.model")
    if not os.path.exists(model_path):
        model = Top2Vec(corpus, speed='learn', embedding_model="doc2vec")
        model.save(model_path)
    else:
        model = Top2Vec.load(model_path)

    # Get topics, sizes and numbers
    topic_sizes, topic_nums = model.get_topic_sizes()

    # 362
    number_topics = model.get_num_topics()
    topic_words, word_scores, topic_nums = model.get_topics(number_topics)

    for i, topic in enumerate(topic_nums):
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
        for i, topic in enumerate(topic_nums):
            image = f"{topic}-cloud.png"
            fd.write(f"\n## Topic {topic}\n")
            words = topic_words[i]
            fd.write("\n```console\n")
            fd.write(" ".join(words) + "\n")
            fd.write("```\n")
            fd.write(f"![{image}]({image})\n")

    # Copy everything back...


if __name__ == "__main__":
    main()
