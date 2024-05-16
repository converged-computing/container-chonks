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
        "--start-date",
        default="2013-04-11",
        help="starting date",
    )
    parser.add_argument(
        "--outdir",
        default=os.path.join(here, "data"),
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
    save_to = os.path.join(args.outdir, "dockerfile-paths.json")

    # This base url taskes a range
    base_url = f"https://api.github.com/search/repositories?q=language:Dockerfile+created:%sT00:00:00Z..%sT00:00:00Z&order=asc&per_page=100&topic:%s"

    # Try these topics
    topics = ["machine-learning"]

    # Create a base temporary folder to work from
    tempdir = tempfile.mkdtemp()

    # Prepare headers
    headers = {"Authorization": f"Bearer {token}", "X-GitHub-Api-Version": "2022-11-28"}

    # Let's parse by 1 week at a time
    # Going backwards in time
    results = []
    while True:
        # start at some date and go backwards by a week
        start = datetime.strptime(args.start_date, "%Y-%m-%d")

        for topic in topics:
            # Keep track of repos seen so we don't do them twice
            seen = set()

            outdir = os.path.join(args.outdir, topic)
            start, end = get_range(start, days=args.days)

            # try to guess raw url and retrieve
            print(
                f"Looking for repository with Dockerfile and topic {topic} in repository created from {start} to {end}"
            )
            url = base_url % (start, end, topic)

            next_page = 1
            while next_page is not None:
                response = requests.get(url + f"&page={next_page}", headers=headers)

                # Stop and interactive debugging
                if response.status_code != 200:
                    print(
                        f"Issue with request: {response.status_code} at {datetime.now()}"
                    )
                    import IPython

                    IPython.embed()

                items = response.json()
                count = items["total_count"]
                print(f"Found {count} results.")

                # Derive the next page
                if count == 0:
                    next_page = None
                else:
                    next_page += 1

                # Can't get more than 10 pages
                if next_page == 11:
                    next_page = None
                
                # We want to clone the repository and save dockerfiles
                for item in items["items"]:
                    # Get the path from the html_url
                    user, repo = item["html_url"].split("/")[-2:]
                    uri = f"{user}/{repo}"
                    if uri in seen:
                        continue

                    seen.add(uri)
                    path = os.path.join(outdir, user, repo)
                    if os.path.exists(path):
                        continue
                    os.makedirs(path)

                    dest = None
                    try:
                        # Try clone (and cut out early if not successful)
                        dest = clone(item["html_url"], tempdir)
                        if not dest:
                            continue

                        # Recursive find Dockerfile and copy to keep
                        files = list(utils.recursive_find(dest, "Dockerfile"))
                        print(f"  Found {len(files)} Dockerfile")
                        for filename in files:
                            # Get relative path to repo
                            relpath = os.path.relpath(
                                filename, os.path.join(tempdir, repo)
                            )
                            file_dest = os.path.join(path, relpath)
                            dirname = os.path.dirname(file_dest)
                            if not os.path.exists(dirname):
                                os.makedirs(dirname)
                            shutil.copyfile(filename, file_dest)
                    except:
                        print(f"Issue with {item['html_url']}, skipping")
                    try:
                        if dest and os.path.exists(dest):
                            shutil.rmtree(dest)
                    except:                        
                        print(
                            "Likely too many files, check with ulimit -n and set with ulimit -n 4096"
                        )
                        import IPython 
                        IPython.embed()

            # Advance to the next date, unless it is too soon
            start = end
            if datetime.strptime(start, "%Y-%m-%d") >= datetime.now():
                break

    import IPython
    IPython.embed()
    sys.exit()
    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)

if __name__ == "__main__":
    main()
