#!/usr/bin/env python3

import argparse
import os

import sqlite3

import matplotlib.pyplot as plt
import metricsoperator.utils as utils
import pandas
from datetime import datetime
from container_guts.main import ManifestGenerator

plt.style.use("bmh")
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Find Base Images",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--out",
        help="directory to save parsed results",
        default=os.path.join(root, "data", "dockerfile"),
    )
    parser.add_argument(
        "--database",
        help="database with guts results",
        default=os.path.join("/tmp", "guts"),
    )
    return parser


def main():
    """
    Run the main plotting operation!
    """
    parser = get_parser()
    args, _ = parser.parse_known_args()

    # Output images and data
    outdir = os.path.abspath(args.out)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if not os.path.exists(args.database):
        sys.exit(
            f"Please clone https://github.com/singularityhub/shpc-guts to {args.database}"
        )

    # Output file
    outfile = os.path.join(outdir, "container-guts-image-bases.json")
    results = {}
    if os.path.exists(outfile):
        results = utils.read_json(outfile)

    # List of images file
    db_file = os.path.join(root, "data", "dockerfile", "data-frame.db")
    manifest_file = os.path.join(outdir, "docker-images.txt")
    if not os.path.exists(manifest_file):
        # This does the actual parsing of data into a formatted variant
        # Has keys results, iters, and columns
        # parse_manifests(files, args, categories, db_file)

        conn = sqlite3.connect(db_file)
        # cursor = conn.cursor()

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
        images = list(manifest_df.uri.unique())
        utils.write_file("\n".join(images), manifest_file)

    else:
        images = [x for x in utils.read_file(manifest_file).split("\n") if x]

    # For each image, run guts! This can get us the paths and filesystem for inspection
    cli = ManifestGenerator(tech="docker")
    issues = set()
    for i, image in enumerate(images):
        if os.path.exists(outfile):
            os.system(f"cp {outfile} {outfile}.bpk")
        if image in results:
            continue
        try:
            scores = cli.similar(image, database=args.database)
            manifest = list(scores.values())[0]
            match = manifest["similar"]["most_similar"]
        except:
            print("There was an issue!")
            issues.add(image)
            continue
        results[image] = match
        print(
            f"Image {image} is most similar to {match['base_image']} with a score of {match['score']}"
        )
        # Note we could save all the similarities, but the data is large
        if i % 10 == 0:
            utils.write_json(results, outfile)

    utils.write_json(results, outfile)
    import IPython

    IPython.embed()
    sys.exit()


if __name__ == "__main__":
    main()
