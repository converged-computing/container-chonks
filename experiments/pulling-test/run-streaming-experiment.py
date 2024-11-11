#!/usr/bin/env python3

import argparse
import json
import os
import re
import sys
import tempfile
import time
import uuid

from jinja2 import Template

here = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    with open(filename, "r") as fd:
        content = fd.read()
    return content


job_template_file = os.path.join(here, "minicluster-template.yaml")
if not os.path.exists(job_template_file):
    sys.exit(f"Job template {job_template_file} is missing.")

job_template = read_file(job_template_file)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Container Pulling Study",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--outdir",
        help="path to output directory",
        default=os.path.join(here, "metadata", "streaming-test", "logs"),
    )
    parser.add_argument(
        "--study",
        help="path to study.json with container list to use",
        default=os.path.join(here, "studies", "streaming.json"),
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


def run_job(container, nodes, entry, outdir):
    """
    Run a job to pull a container.
    """
    template = Template(job_template)
    subs = {
        "size": nodes,
        "container": container,
        "pre": entry.get("pre"),
        "tasks": entry["tasks"],
        "command": entry["command"],
    }
    templated = template.render(subs)

    # Output file based on container name
    suffix = str(uuid.uuid4())
    outfile = re.sub("(-|[.]|:|/)", "_", container) + "-" + suffix[0:8] + ".log"
    outpath = os.path.join(outdir, outfile)

    # Write to temporary file just to submit!
    job_yaml = get_tmpfile()
    write_file(templated, job_yaml)
    run_kubectl(f"apply -f {job_yaml}")

    time.sleep(10)

    # Wait for job to finish
    run_kubectl("wait --for=condition=complete job/flux-sample --timeout=1200s")

    # Save the log (note this is hard coded into streaming output directory
    print(f"Writing output file to {outpath}")
    run_kubectl(
        f"logs $(kubectl get pods -o json | jq -r .items[0].metadata.name) > {outpath}"
    )
    run_kubectl(f"delete -f {job_yaml} --wait=true", allow_fail=True)
    os.remove(job_yaml)

    # Make sure we are completely deleted before starting next
    run_kubectl(
        "wait --for=delete pod/$(kubectl get pods -o json | jq -r .items[0].metadata.name) --timeout=60s"
    )


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


def install_operator():
    run_kubectl("apply -f ./flux-operator.yaml")


def run_experiments(nodes, study, outdir):
    """
    Wrap experiment running separately in case we lose spot nodes and can recover
    """
    # This cleans up every 1800 seconds
    install_operator()
    total = len(study)
    for i, entry in enumerate(study):
        container = entry["image"]
        print(f"Running experiment for container {container}, {i} of {total}")
        run_job(container, nodes, entry, outdir)
    print("Experiments are done!")


def read_study(study_file, nodes):
    """
    Read the study json file, which should have lookup indices
    by the nodes (size) as a strong, and then for each entry:

    image: the full uri (including tag) of the container
    tasks: the number of tasks to use for the recipe
    command: yes, that.
    """
    if not study_file:
        sys.exit("You must provide a --study json file")
    if not os.path.exists(study_file):
        sys.exit(f"Study json file {study_file} does not exist.")
    study = read_json(study_file)
    if str(nodes) not in study:
        sys.exit(f"The nodes {nodes} key is missing")
    required = ["image", "tasks", "command"]
    for i, entry in enumerate(study[str(nodes)]):
        for field in required:
            if field not in entry:
                sys.exit(f"Study json entry at index {i} is missing field '{field}'")
    return study


def main():
    """
    Run experiments that time pulling of containers across nodes.

    This script simply needs to apply and manage the yaml, so no
    need to save results, etc.
    """
    parser = get_parser()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, _ = parser.parse_known_args()

    # Read in the study and unwrap it!
    study = read_study(args.study, args.nodes)[str(args.nodes)]

    # Ensure output directory exists
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)

    print("🪴️ Planning to run:")
    print(f" Containers: {len(study)}")
    print(f"     outdir: {args.outdir}")
    print(f"      nodes: {args.nodes}")
    if not confirm_action("Would you like to continue?"):
        sys.exit("📺️ Canceled!")

    # Main experiment running, show total time just for user FYI
    start_experiments = time.time()
    run_experiments(args.nodes, study, args.outdir)
    stop_experiments = time.time()
    total = stop_experiments - start_experiments
    print(f"total time to run is {total} seconds")


if __name__ == "__main__":
    main()
