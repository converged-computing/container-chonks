# Pulling Experiment

We will be using the following set of containers to test pulling across a number of total image sizes and layer counts.
For each entry below, the layer size is determined based on the image size / number of layers. The total size has 5MB subtracted to account for the busybox base image.

<details>

<summary>Images Built for Study</summary>

```console
⭐ Final image set built:
ghcr.io/converged-computing/container-chonks:1-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:2-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:3-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:4-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:5-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:6-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:7-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:8-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:9-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:10-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:11-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:12-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:13-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:14-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:25-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:50-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:75-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:100-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:125-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:150-layers-size-48702097-bytes
ghcr.io/converged-computing/container-chonks:1-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:2-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:3-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:4-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:5-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:6-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:7-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:8-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:9-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:10-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:11-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:12-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:13-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:14-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:25-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:50-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:75-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:100-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:125-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:150-layers-size-127399102-bytes
ghcr.io/converged-computing/container-chonks:1-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:2-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:3-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:4-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:5-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:6-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:7-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:8-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:9-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:10-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:11-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:12-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:13-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:14-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:25-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:50-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:75-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:100-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:125-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:150-layers-size-387602448-bytes
ghcr.io/converged-computing/container-chonks:1-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:2-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:3-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:4-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:5-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:6-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:7-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:8-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:9-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:10-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:11-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:12-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:13-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:14-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:25-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:50-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:75-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:100-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:125-layers-size-19034736629-bytes
ghcr.io/converged-computing/container-chonks:150-layers-size-19034736629-bytes
```

</details>

I'm going to start with n1-standard-16, which has 16vCPU and 60GB RAM. Each instance is ~0.76 an hour, and I'm hoping we can try scaling up to 256 nodes. I'll test on something small like 4 nodes. We are going to use an indexed job.

## Design

```console
For each cluster size:
  Create the cluster
  Start monitoring service (see below) for pulls
  For each container in the set:
    Create a MiniCluster that sleeps for a second
    Wait for job to complete and go away
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
    --machine-type=n1-standard-16 \
    --enable-gvnic \
    --region=us-central1-a \
    --project=${GOOGLE_PROJECT} 
```

Prepare a metadata directory with pull times:

```bash
mkdir -p metadata
```

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
kubectl logs -n monitoring event-exporter-xxxxxxxxx -f  |& tee ./metadata/events-size-$NODES-$(date +%s).json
```

Run the experiment:

```bash
python run-experiment.py
```

When you are done:

```bash
gcloud container clusters delete test-cluster --region=us-central1-a
```

