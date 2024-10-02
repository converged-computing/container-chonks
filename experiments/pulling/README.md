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
## Experiment

### 1. Setup

Bring up the cluster (with 4, 8, 16, 32, 64, 128, and 256 nodes) and run the experiment:

```bash
GOOGLE_PROJECT=myproject
# 4, 8, 16, 32, 64, 128
NODES=64

time gcloud container clusters create test-cluster \
    --threads-per-core=1 \
    --num-nodes=$NODES \
    --machine-type=n1-standard-16 \
    --enable-gvnic \
    --region=us-central1-a \
    --project=${GOOGLE_PROJECT} 
```

Prepare a metadata directory with pull times (change the directory name to the instance size):

```bash
mkdir -p metadata/run1/$NODES
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
mkdir -p metadata/run1/$NODES
kubectl get nodes -o json > metadata/run1/$NODES/nodes-$NODES-$(date +%s).json
```

Start monitoring (this goes in its own terminal):

```bash
kubectl logs -n monitoring event-exporter-xxxxxxxxx -f  |& tee ./metadata/run1/$NODES/events-size-$NODES-$(date +%s).json
```

### 3. Experiment Test

> This is entirely automated

Run the experiment (and these are on the varying numbers of $NODES above)

```bash
python run-experiment.py --nodes 4
python run-experiment.py --nodes 8
python run-experiment.py --nodes 16
python run-experiment.py --nodes 32
python run-experiment.py --nodes 64

# NOT RUN YET
python run-experiment.py --nodes 128
python run-experiment.py --nodes 256
```

When you are done:

```bash
gcloud container clusters delete test-cluster --region=us-central1-a
```

### 4. Experiment

Let's make a more consolidated loop

```console
GOOGLE_PROJECT=myproject
for NODES in 4 8 16 32 64 128 256
  do

time gcloud container clusters create test-cluster \
    --threads-per-core=1 \
    --num-nodes=$NODES \
    --machine-type=n1-standard-16 \
    --enable-gvnic \
    --region=us-central1-a \
    --project=${GOOGLE_PROJECT} 

cd /tmp/kubernetes-event-exporter
kubectl create namespace monitoring
kubectl apply -f deploy
cd -

mkdir -p metadata/run1/$NODES
kubectl get nodes -o json > metadata/run1/$NODES/nodes-$NODES-$(date +%s).json

# In another terminal
# NODES=64
# kubectl logs -n monitoring event-exporter-xxxxxxxxx -f  |& tee ./metadata/run1/$NODES/events-size-$NODES-$(date +%s).json

python run-experiment.py --nodes $NODES
gcloud container clusters delete test-cluster --region=us-central1-a

done
```

### 5. Analysis

The scripts in [analysis](analysis) provide parsing of experiment metadata.

#### run1

This was an attempt to reduce the number of layers to the median (9) and increase sizes. The time was much more reasonable (~11 minutes the first time). It definitely was faster! I wound up running it twice, adding more sizes the second time (and this was the final container set).

```console
# size 4 (not final study containers)
job.batch "container-pull" deleted
Experiments are done!
total time to run is 694.6678006649017 seconds

# size 4 (final study containers)
job.batch "container-pull" deleted
Experiments are done!
total time to run is 1383.645084142685 seconds

# size 8
job.batch "container-pull" deleted
Experiments are done!
total time to run is 1392.8416512012482 seconds

# size 16
kubectl delete -f /tmp/job-86ljvb30.yaml --wait=true
job.batch "container-pull" deleted
Experiments are done!
total time to run is 1408.475350856781 seconds

# size 32
kubectl delete -f /tmp/job-8x3al9cq.yaml --wait=true
job.batch "container-pull" deleted
Experiments are done!
total time to run is 1426.8381447792053 seconds

# size 64
job.batch/container-pull condition met
kubectl delete -f /tmp/job-a_75wuum.yaml --wait=true
job.batch "container-pull" deleted
Experiments are done!
total time to run is 1535.1909275054932 seconds

# size 128
kubectl delete -f /tmp/job-jd3nj2cz.yaml --wait=true
job.batch "container-pull" deleted
Experiments are done!
total time to run is 1940.994199514389 seconds

# size 256
kubectl wait --for=condition=complete job/container-pull --timeout=1200s
job.batch/container-pull condition met
kubectl delete -f /tmp/job-er3kyteb.yaml --wait=true
job.batch "container-pull" deleted
Experiments are done!
total time to run is 2884.183334827423 seconds
```

Note how the total experiment time goes up by quite a bit, but the plots don't reflect that. There is something else in here taking time - maybe just waiting for the job to complete? Here are the two plots (y scale is the same):


![analysis/data/run1/img/pull_times_duration_by_size_run1_125_layers.png](analysis/data/run1/img/pull_times_duration_by_size_run1_125_layers.png)
![analysis/data/run1/img/pull_times_duration_by_size_run1_9_layers.png](analysis/data/run1/img/pull_times_duration_by_size_run1_9_layers.png)

I see the following:

- The larger number of layers (smaller size per layer) has an overall higher median value, but much less variation. This makes sense, because maybe it could be less burden on the network, or less subject to variability of it?
- The smaller number of layers (and larger size per layer) has a lower overall mean, but much larger variation. I'd guess the longer pull makes it more subject to the network. If extraction is used in container pulling, this could also reflect the filesystem.

I believe that layer extraction is done sequentially, so there are two pieces to that. More layers == more things to do, but they are smaller tasks. The flip is fewer extractions, but each one is larger. I think we need to look at the influence of network and storage. We can do that next.

```bash
# Raw times raw-times.json
python analysis/1-prepare-data.py --root ./metadata/run1 --out ./analysis/data/run1

# Get docker manifests (only need to do this once when containers are new)
# python analysis/2-docker-manifests.py --data ./analysis/data/run1

# This generates (or updates) plots!
python analysis/3-parse-containers.py --data ./analysis/data/run1

# And similarity
python analysis/4-similarity.py --data ./analysis/data/run1
```

![analysis/data/run1/img/pull_times_test_duration_by_size_run1.png](analysis/data/run1/img/pull_times_test_duration_by_size_run1.png)

Okay I like the dichotomy between the two layer extremes - I'd like to keep that to see how it scales across nodes. I am also thinking we will want to test GitHub packages and Google's local registry, for comparison.
This still shows a huge swing up to pulling, and I think we need to see more sizes there, even if they are at the top of the sizes in terms of percentiles. The reason is because we can expect ML containers to get larger.

#### test 

I first did some quick testing to see if the instance memory had an impact, making a large jump so I could see it. 

Total experiment time for size 4 nodes:
 - size 4 nodes, n1-standard-16: 54.24 minutes (~3)
 - size 4 nodes, n1-standard-64: 52.73 minutes
 
I don't think times are different enough to justify the increase in cost, so we will stick with n1-standard-16 for the study.

```console
Experiments are done!
total time to run is 3254.424793243408 seconds

job.batch "container-pull" deleted
Experiments are done!
total time to run is 3164.1695561408997 seconds

# size 32
kubectl delete -f /tmp/job-3wrfgtai.yaml --wait=true
job.batch "container-pull" deleted
Experiments are done!
total time to run is 1398.415813446045 seconds

# size 64
kubectl delete -f /tmp/job-a_75wuum.yaml --wait=true
job.batch "container-pull" deleted
Experiments are done!
total time to run is 1535.1909275054932 seconds
```

Difference in the above?
```console
(3254.424793243408/3164.1695561408997)
1.0285241468578523
# aka, about 1.028x faster

How much more expensive?
3254.424793243408 * (4*0.76) = 9893.451371459962
3164.1695561408997 * (4*3.03) = 38349.7350204277
38349.7350204277 / 9893.451371459962
3.87 x more expensive!
```

TLDR: 1.028x faster, but 3.87x more expensive, not worth it.

```bash
# Raw times raw-times.json
python analysis/1-prepare-data.py --root ./metadata/test --out ./analysis/data/test

# Get docker manifests
python analysis/2-docker-manifests.py --data ./analysis/data/test

# This generates plots!
python analysis/3-parse-containers.py --data ./analysis/data/test

# And similarity
python analysis/4-similarity.py --data ./analysis/data/test
```

I next looked at the plot of number of layers by image size over time. What I see here is that number of layers does not seem to matter. What matters is the total size.

![analysis/data/test/img/pull_times_test_duration_by_size_n1-standard-16.png](analysis/data/test/img/pull_times_test_duration_by_size_n1-standard-16.png)
![analysis/data/test/img/pull_times_test_duration_by_size_n1-standard-64.png](analysis/data/test/img/pull_times_test_duration_by_size_n1-standard-64.png)

I think the plot I want to see is the size of the cluster (nodes) on the x axis, and then the hue be the image size. I'll choose a small number of number of layers for the variety but I'm not convinced it matters. Finally, when we remove the base (busybox) we see they are entirely different. This is good - the tool is working as expected!

![analysis/data/similarity/pulling/cluster-container-similarity.png](analysis/data/similarity/pulling/cluster-container-similarity.png)

Next step: adjust parameter space to have fewer layer size options, and more sizes. After that, can run the study on the smaller instance size 8 and see if we get any very different results.
