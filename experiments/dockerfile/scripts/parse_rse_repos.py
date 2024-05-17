#!/usr/bin/env python3

from datetime import datetime, timedelta

from rse.main import Encyclopedia
from rse.utils.command import Command
import rse.utils.file as utils


import tempfile
import requests
import json
import argparse
import sys
import shutil
import os

here = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(here)

token = os.environ.get("GITHUB_TOKEN")
if not token:
    sys.exit("Please export GITHUB_TOKEN")


def clone(url, dest):
    dest = os.path.join(dest, os.path.basename(url))
    cmd = Command("git clone --depth 1 %s %s" % (url, dest))
    cmd.execute()
    if cmd.returncode != 0:
        print("Issue cloning %s" % url)
        return
    return dest


def get_parser():
    parser = argparse.ArgumentParser(description="Dockerfile Scraper")
    parser.add_argument(
        "--outdir",
        default=os.path.join(root, "data", "rseng"),
        help="output data directory for results",
    )
    parser.add_argument(
        "--days",
        default=100,
        help="days to search for repos over",
    )
    parser.add_argument(
        "--settings-file",
        dest="settings_file",
        help="custom path to settings file.",
    )
    return parser


def main():
    parser = get_parser()
    args, _ = parser.parse_known_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    # Parse these known ML orgs

    # Create a base temporary folder to work from
    tempdir = tempfile.mkdtemp()

    pedia = Encyclopedia(args.settings_file)
    repos = list(pedia.list())
    total = len(repos)
    seen = set()

    for i, reponame in enumerate(repos):
        print(f"{i} of {total}", end="\r")

        # Prepare to clone the repository
        repo = pedia.get(reponame[0])
        if not repo.url or repo.url in seen:
            print(f"Skipping {repo.url}")
            continue

        user, _ = repo.url.split("/")[-2:]
        reponame = "/".join(reponame[0].split("/")[1:])
        path = os.path.join(args.outdir, user, reponame)
        if os.path.exists(path):
            continue

        os.makedirs(path)
        dest = None
        try:
            # Try clone (and cut out early if not successful)
            dest = clone(repo.url, tempdir)
            if not dest:
                continue

            # Recursive find Dockerfile and copy to keep
            files = list(utils.recursive_find(dest, "Dockerfile*"))
            print(f"  Found {len(files)} Dockerfile in {reponame}")
            # Note that we keep the path so we don't try again on rerun

            for filename in files:
                # Get relative path to repo
                relpath = os.path.relpath(filename, os.path.join(tempdir, reponame))
                file_dest = os.path.join(path, relpath)
                dirname = os.path.dirname(file_dest)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                if not os.path.exists(file_dest):
                    shutil.copyfile(filename, file_dest)
        except:
            import IPython

            IPython.embed()
            sys.exit()
            print(f"Issue with {repo.url}, skipping")

        if dest:
            cleanup(dest)

    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)


def cleanup(dest):
    try:
        if dest and os.path.exists(dest):
            shutil.rmtree(dest)
    except:
        print("Likely too many files, check with ulimit -n and set with ulimit -n 4096")
        import IPython

        IPython.embed()


if __name__ == "__main__":
    main()
