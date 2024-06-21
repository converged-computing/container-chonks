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
        description="Parse Dockerfile Layers",
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

    # Find Dockerfile again
    files = list(utils.recursive_find(root, "Dockerfile*"))
    print(f"Total Dockerfile across project: {len(files)}")

    # This gets replaced with a space (to make new tokens)
    punctuation = "('|\"|;|:|=|_|-|\n|\t|#|[.]|[*]|[&]|[@])"

    # This gets removed
    removed = "(<|>|{|}|[|]|[)]|[(]|[]]|[[]|[$]|[/])"

    root_dir = os.path.dirname(args.results)
    fd = open(os.path.join(root_dir, "scientific-dockerfile-image-corpus.txt"), "w")
    meta = open(os.path.join(root_dir, "scientific-dockerfile-image-index.txt"), "w")

    for dockerfile in files:     
        lines = utils.read_file(dockerfile)
        tokens = []
        # Get rid of punctuation that could make commands different
        content = re.sub(punctuation, " ", lines)
        content = re.sub(removed, " ", content)
        line = content.lower().split()

        # Get rid of single characters
        tokens = [x for x in line if len(x) > 1]

        # Also get rid of shas and commits
        tokens = [x for x in tokens if len(x) != 64 and len(x) != 40]

        # Try adding layers only once, and count uniqueness here
        assembled = " ".join(tokens)
        fd.write(assembled + "\n")
        meta.write(dockerfile + "\n")

    fd.close()
    meta.close()


if __name__ == "__main__":
    main()
