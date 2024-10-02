# Pulling Experiments

We will be using a matrix of containers to test pulling across a number of total image sizes and layer counts.
For each container, the layer size is determined based on the image size / number of layers. The total size has 5MB subtracted to account for the busybox base image. There are 71 images built for the study, which you can see tags for in [run-experiment.py](run-experiment.py). The tool to generate the lists of containers (and the actual containers in the registry) is [converged-computing/container-crafter](https://github.com/converged-computing/container-crafter).

## Design

```console
For each cluster size:
  Create the cluster
  Start monitoring service (see below) for pulls
  Deploy service that clears cache every 1800 seconds so we don't run out of room
  For each container in the set:
    Create a job that does nothing, this will record container pulling events
    Wait for job to complete and go away, continue
```

## Experiments

### run1

> test pulling containers on n1-standard-16 sizes 4-256

This was the first set of experiments run after testing - an attempt to reduce the number of layers to the median (9) and the max (125) layers and increase sizes. The time was much more reasonable (~11 minutes the first time). It definitely was faster! I wound up running it twice, adding more sizes the second time (and this was the final container set). For this final set of containers, the experiment was run as follows:

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
# kubectl logs -n monitoring $(kubectl get pods -n monitoring | jq -r [0].metadata.name) -f  |& tee ./metadata/run1/$NODES/events-size-$NODES-$(date +%s).json

python run-experiment.py --nodes $NODES --study ./studies/run1.json
gcloud container clusters delete test-cluster --region=us-central1-a

done
```

Here is the output from the script (wrapping automation for all runs):

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

Note how the total experiment time goes up by quite a bit, but the plots don't reflect that. There is something else in here taking time - maybe just waiting for the job to complete?

#### Analysis

Here is how to run scripts to generate plots, etc.

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
The scripts in [analysis](analysis) provide parsing of experiment metadata. See [test](test.md) for preliminary testing. Here are the complete times (recorded by the script) that wrapped the experiment.

Here are the two plots (y scale is the same):


![analysis/data/run1/img/pull_times_duration_by_size_run1_125_layers.png](analysis/data/run1/img/pull_times_duration_by_size_run1_125_layers.png)
![analysis/data/run1/img/pull_times_duration_by_size_run1_9_layers.png](analysis/data/run1/img/pull_times_duration_by_size_run1_9_layers.png)

I see the following:

- The larger number of layers (smaller size per layer) has an overall higher median value, but much less variation. This makes sense, because maybe it could be less burden on the network, or less subject to variability of it?
- The smaller number of layers (and larger size per layer) has a lower overall mean, but much larger variation. I'd guess the longer pull makes it more subject to the network. If extraction is used in container pulling, this could also reflect the filesystem.

I believe that layer extraction is done sequentially, so there are two pieces to that. More layers == more things to do, but they are smaller tasks. The flip is fewer extractions, but each one is larger. I think we need to look at the influence of network and storage. We can do that next. 
