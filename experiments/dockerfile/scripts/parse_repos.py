#!/usr/bin/env python3

from datetime import datetime, timedelta

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


def get_range(dt, days=360):
    """
    Get the range of datetimes.
    """
    # Allow function to be used for both cases
    if isinstance(dt, str):
        dt = datetime.strptime(dt, "%Y-%m-%d")
    next_dt = dt + timedelta(days=days)
    return str(dt).split(" ")[0], str(next_dt).split(" ")[0]


def get_parser():
    parser = argparse.ArgumentParser(description="Dockerfile Scraper")
    parser.add_argument(
        "--outdir",
        default=os.path.join(root, "data", "orgs"),
        help="output data directory for results",
    )
    parser.add_argument(
        "--days",
        default=100,
        help="days to search for repos over",
    )
    return parser


def main():
    parser = get_parser()
    args, _ = parser.parse_known_args()

    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    # Parse these known ML orgs
    orgs = [
        # "nvidia",
        # "huggingface",
        # "pytorch",
        # "tensorflow",
        # "azure",
        # "udacity",
        # "tensorflow",
        # "scikit-learn",
    ]

    # Create a base temporary folder to work from
    tempdir = tempfile.mkdtemp()

    # Prepare headers
    headers = {
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github+json",
    }

    # Let's parse by 1 week at a time
    # Going backwards in time
    results = []
    for org in orgs:
        # Create an output directory for the org
        outdir = os.path.join(args.outdir, org)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        url = f"https://api.github.com/orgs/{org}/repos"

        print(f"Looking for repos for {org}")
        # Keep track of repos seen so we don't do them twice
        seen = set()

        # Get listing of repos
        total_results = 1
        page = 1
        repos = []
        while total_results > 0:
            response = requests.get(
                url, headers=headers, params={"per_page": 100, "page": page}
            )

            if response.status_code == 200:
                new_repos = response.json()
                repos += new_repos
                total_results = len(new_repos)
                print(f"Found {total_results} new repos")
                page += 1

            else:
                total_results = 0
                break

        print(f"Found a total of {len(repos)} repositories for {org}")

        for item in repos:
            user, repo = item["html_url"].split("/")[-2:]
            uri = f"{user}/{repo}"
            if uri in seen:
                continue

            seen.add(uri)
            path = os.path.join(outdir, user, repo)

            if not os.path.exists(path):
                os.makedirs(path)
            dest = None
            try:
                # Try clone (and cut out early if not successful)
                dest = clone(item["html_url"], tempdir)
                if not dest:
                    continue

                # Recursive find Dockerfile and copy to keep
                files = list(utils.recursive_find(dest, "Dockerfile*"))
                print(f"  Found {len(files)} Dockerfile in {uri}")
                # Note that we keep the path so we don't try again on rerun

                for filename in files:
                    # Get relative path to repo
                    relpath = os.path.relpath(filename, os.path.join(tempdir, repo))
                    file_dest = os.path.join(path, relpath)
                    dirname = os.path.dirname(file_dest)
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                    if not os.path.exists(file_dest):
                        shutil.copyfile(filename, file_dest)
            except:
                print(f"Issue with {item['html_url']}, skipping")

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
