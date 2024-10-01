# Pulling Experiment

We will be using a matrix of containers to test pulling across a number of total image sizes and layer counts.
For each container, the layer size is determined based on the image size / number of layers. The total size has 5MB subtracted to account for the busybox base image. There are 71 images built for the study, which you can see tags for in [run-experiment.py](run-experiment.py).

I'm first going to test a small cluster (4 nodes) with two instance types, the purpose being to see if the instance type (and more cpu/ram) can decrease pull time. We will either run across a range (cost allowing) or if not, choose a single size. I'm going to start with n1-standard-16, which has 16vCPU and 60GB RAM. Each instance is ~0.76 an hour, and I'm hoping we can try scaling up to 256 nodes. I'll test on something small like 4 nodes. I am then going to test on n1-standard-64 ($3.03, 64 vCPU and 240GB memory). We are going to use an indexed job for both.

## Design

```console
For each cluster size:
  Create the cluster
  Start monitoring service (see below) for pulls
  For each container in the set:
    Create a MiniCluster that sleeps for a second
    Wait for job to complete and go away
```

## Testing

I did some quick testing to see if the instance memory had an impact, making a large jump so I could see it.

Total experiment time for size 4 nodes:
 - size 4 nodes, n1-standard-16: 54.24 minutes (~3)
 - size 4 nodes, n1-standard-64: 52.73 minutes
 
I don't think times are different enough to justify the increase in cost.
 
```console
Experiments are done!
total time to run is 3254.424793243408 seconds

job.batch "container-pull" deleted
Experiments are done!
total time to run is 3164.1695561408997 seconds
```

## Experiment

### 1. Setup

Bring up the cluster (with 16, 32, 64, 128, and 256 nodes) and run the experiment:

```bash
GOOGLE_PROJECT=myproject
# 16, 32, 64, 128
NODES=4

time gcloud container clusters create test-cluster \
    --threads-per-core=1 \
    --num-nodes=$NODES \
    --machine-type=n1-standard-64 \
    --enable-gvnic \
    --region=us-central1-a \
    --project=${GOOGLE_PROJECT} 
```

Prepare a metadata directory with pull times (change the directory name to the instance size):

```bash
mkdir -p metadata/n1-standard-64
```

### 2. Monitoring

Deploy monitoring:

```bash
git clone https://github.com/resmoio/kubernetes-event-exporter /tmp/kubernetes-event-exporter
cd /tmp/kubernetes-event-exporter
kubectl create namespace monitoring
kubectl apply -f deploy
```

Save nodes for size

```bash
kubectl get nodes -o json > metadata/nodes-$NODES.json
```

Start monitoring (this goes in its own terminal):

```bash
kubectl logs -n monitoring event-exporter-xxxxxxxxx -f  |& tee ./metadata/n1-standard-64/events-size-$NODES-$(date +%s).json
```

### 3. Experiment

> This is entirely automated

Run the experiment:

```bash
python run-experiment.py  --nodes 4
```

When you are done:

```bash
gcloud container clusters delete test-cluster --region=us-central1-a
```

### 4. Analysis

First we want to parse the monitoring metadata.

```bash
# Raw times raw-times.json
python analysis/1-prepare-data.py

# Get docker manifests
python analysis/2-docker-manifests.py

# This generates plots!
python analysis/3-parse-containers.py

# And similarity
python analysis/4-similarity.py
```

Next step: need to double check that base image (which is the same) accounts for
the slight similarity values. The only reason we'd have the gradient is because there are a different number of things being compared in sets with different layers. Likely we should subtract out the base image. After that, can run the study on the smaller instance size 8 and see if we get any very different results.


