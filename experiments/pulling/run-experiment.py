#!/usr/bin/env python3

import argparse
import json
import os
import sys
import tempfile
import time

from jinja2 import Template

here = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    with open(filename, "r") as fd:
        content = fd.read()
    return content


job_template_file = os.path.join(here, "job-template.yaml")
if not os.path.exists(job_template_file):
    sys.exit(f"Job template {job_template_file} is missing.")

job_template = read_file(job_template_file)

tags_testing = [
    "1-layers-size-127399102-bytes",
    "1-layers-size-387602448-bytes",
    "1-layers-size-48702097-bytes",
    "10-layers-size-127399102-bytes",
    "10-layers-size-19034736629-bytes",
    "10-layers-size-387602448-bytes",
    "10-layers-size-48702097-bytes",
    "100-layers-size-127399102-bytes",
    "100-layers-size-19034736629-bytes",
    "100-layers-size-387602448-bytes",
    "100-layers-size-48702097-bytes",
    "11-layers-size-127399102-bytes",
    "11-layers-size-19034736629-bytes",
    "11-layers-size-387602448-bytes",
    "11-layers-size-48702097-bytes",
    "12-layers-size-127399102-bytes",
    "12-layers-size-19034736629-bytes",
    "12-layers-size-387602448-bytes",
    "12-layers-size-48702097-bytes",
    "13-layers-size-127399102-bytes",
    "13-layers-size-19034736629-bytes",
    "13-layers-size-387602448-bytes",
    "13-layers-size-48702097-bytes",
    "14-layers-size-127399102-bytes",
    "14-layers-size-19034736629-bytes",
    "14-layers-size-387602448-bytes",
    "14-layers-size-48702097-bytes",
    "2-layers-size-127399102-bytes",
    "2-layers-size-19034736629-bytes",
    "2-layers-size-387602448-bytes",
    "2-layers-size-48702097-bytes",
    "25-layers-size-127399102-bytes",
    "25-layers-size-19034736629-bytes",
    "25-layers-size-387602448-bytes",
    "25-layers-size-48702097-bytes",
    "3-layers-size-127399102-bytes",
    "3-layers-size-19034736629-bytes",
    "3-layers-size-387602448-bytes",
    "3-layers-size-48702097-bytes",
    "4-layers-size-127399102-bytes",
    "4-layers-size-19034736629-bytes",
    "4-layers-size-387602448-bytes",
    "4-layers-size-48702097-bytes",
    "5-layers-size-127399102-bytes",
    "5-layers-size-19034736629-bytes",
    "5-layers-size-387602448-bytes",
    "5-layers-size-48702097-bytes",
    "50-layers-size-127399102-bytes",
    "50-layers-size-19034736629-bytes",
    "50-layers-size-387602448-bytes",
    "50-layers-size-48702097-bytes",
    "6-layers-size-127399102-bytes",
    "6-layers-size-19034736629-bytes",
    "6-layers-size-387602448-bytes",
    "6-layers-size-48702097-bytes",
    "7-layers-size-127399102-bytes",
    "7-layers-size-19034736629-bytes",
    "7-layers-size-387602448-bytes",
    "7-layers-size-48702097-bytes",
    "75-layers-size-127399102-bytes",
    "75-layers-size-19034736629-bytes",
    "75-layers-size-387602448-bytes",
    "75-layers-size-48702097-bytes",
    "8-layers-size-127399102-bytes",
    "8-layers-size-19034736629-bytes",
    "8-layers-size-387602448-bytes",
    "8-layers-size-48702097-bytes",
    "9-layers-size-127399102-bytes",
    "9-layers-size-19034736629-bytes",
    "9-layers-size-387602448-bytes",
    "9-layers-size-48702097-bytes",
]

uri = "ghcr.io/converged-computing/container-chonks-run1"

tags = [
    "125-layers-size-103513992-bytes",
    "125-layers-size-1176249324-bytes",
    "125-layers-size-127399102-bytes",
    "125-layers-size-158049655-bytes",
    "125-layers-size-19034736629-bytes",
    "125-layers-size-213665412-bytes",
    "125-layers-size-266728773-bytes",
    "125-layers-size-2770722493-bytes",
    "125-layers-size-315018606-bytes",
    "125-layers-size-387602448-bytes",
    "125-layers-size-48702097-bytes",
    "125-layers-size-491514346-bytes",
    "125-layers-size-53049507-bytes",
    "125-layers-size-66460665-bytes",
    "125-layers-size-682439577-bytes",
    "125-layers-size-86388866-bytes",
    "9-layers-size-103513992-bytes",
    "9-layers-size-1176249324-bytes",
    "9-layers-size-127399102-bytes",
    "9-layers-size-158049655-bytes",
    "9-layers-size-19034736629-bytes",
    "9-layers-size-213665412-bytes",
    "9-layers-size-266728773-bytes",
    "9-layers-size-2770722493-bytes",
    "9-layers-size-315018606-bytes",
    "9-layers-size-387602448-bytes",
    "9-layers-size-48702097-bytes",
    "9-layers-size-491514346-bytes",
    "9-layers-size-53049507-bytes",
    "9-layers-size-66460665-bytes",
    "9-layers-size-682439577-bytes",
    "9-layers-size-86388866-bytes",
    "125-layers-size-10902729561-bytes",
    "125-layers-size-14968733095-bytes",
    "125-layers-size-6836726027-bytes",
    "9-layers-size-10902729561-bytes",
    "9-layers-size-14968733095-bytes",
    "9-layers-size-6836726027-bytes",
]

def get_parser():
    parser = argparse.ArgumentParser(
        description="Container Pulling Study",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--nodes",
        help="number of nodes to create for job",
        type=int,
        default=4,
    )
    return parser


def read_json(filename):
    """
    Read json from file.
    """
    with open(filename, "r") as fd:
        content = json.loads(fd.read())
    return content


def confirm_action(question):
    """
    Ask for confirmation of an action
    """
    response = input(question + " (yes/no)? ")
    while len(response) < 1 or response[0].lower().strip() not in "ynyesno":
        response = input("Please answer yes or no: ")
    if response[0].lower().strip() in "no":
        return False
    return True


def write_json(obj, filename):
    """
    write json to output file
    """
    with open(filename, "w") as fd:
        fd.write(json.dumps(obj, indent=4))


def write_file(content, filename):
    with open(filename, "w") as fd:
        fd.write(content)


def get_tmpfile(prefix="job-", suffix=".yaml"):
    """
    Get a temporary file to write the job yaml to.
    """
    tmpdir = tempfile.gettempdir()
    prefix = os.path.join(tmpdir, os.path.basename(prefix))
    fd, tmp_file = tempfile.mkstemp(prefix=prefix, suffix=suffix)
    os.close(fd)
    return tmp_file


def run_job(container, args):
    """
    Run a job to pull a container.
    """
    template = Template(job_template)
    subs = {"size": args.nodes, "container": container}
    templated = template.render(subs)

    # Write to temporary file just to submit!
    job_yaml = get_tmpfile()
    write_file(templated, job_yaml)
    run_kubectl(f"apply -f {job_yaml}")

    # the name is always container-pull
    time.sleep(5)

    # Wait for job to finish
    run_kubectl("wait --for=condition=complete job/container-pull --timeout=1200s")
    run_kubectl(f"delete -f {job_yaml} --wait=true", allow_fail=True)
    os.remove(job_yaml)


def run_kubectl(command, allow_fail=False):
    """
    Wrapper to client to run command with kubectl.

    This requires you to run the gcloud command first.
    """
    global cli
    command = f"kubectl {command}"
    print(command)
    res = os.system(command)
    if res != 0 and not allow_fail:
        print(
            f"ERROR: running {command} - debug and ensure it works before exiting from session."
        )
        import IPython

        IPython.embed()
    return res


def clean_cache():
    run_kubectl(
        "apply -f https://raw.githubusercontent.com/andyzhangx/demo/master/dev/docker-image-cleanup.yaml"
    )


def run_experiments(args):
    """
    Wrap experiment running separately in case we lose spot nodes and can recover
    """
    # This cleans up every 1800 seconds
    clean_cache()
    total = len(tags)
    for i, tag in enumerate(tags):
        container = f"{uri}:{tag}"
        print(f"Running experiment for container {container}, {i} of {total}")
        run_job(container, args)
    print("Experiments are done!")


def main():
    """
    Run experiments that time pulling of containers across nodes.

    This script simply needs to apply and manage the yaml, so no
    need to save results, etc.
    """
    parser = get_parser()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, _ = parser.parse_known_args()

    print("🪴️ Planning to run:")
    print(f"   Containers: {len(tags)}")
    print(f"        nodes: {args.nodes}")
    if not confirm_action("Would you like to continue?"):
        sys.exit("📺️ Cancelled!")

    # Main experiment running, show total time just for user FYI
    start_experiments = time.time()
    run_experiments(args)
    stop_experiments = time.time()
    total = stop_experiments - start_experiments
    print(f"total time to run is {total} seconds")


if __name__ == "__main__":
    main()
