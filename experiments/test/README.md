# Quick test of sizes

This is a quick test to see if pulling one large layer on many nodes is even possible.
 
## Experiments

After prototyping, you can create a cluster on c2d-standard-8 for a size of interest. Note that I'm leaving out the network optimization. We will follow [these best practices](https://cloud.google.com/architecture/best-practices-for-using-mpi-on-compute-engine).

```bash
GOOGLE_PROJECT=myproject
gcloud container clusters create test-cluster \
    --threads-per-core=1 \
    --num-nodes=8 \
    --disk-size=150GB \
    --no-enable-autorepair \
    --no-enable-autoupgrade \
    --region=us-central1-a \
    --project=${GOOGLE_PROJECT} \
    --machine-type=c2d-standard-8
```

Default disk size is 100GB so we are making it a little bigger.


### Build containers

Let's build a few sizes and push to one registry for testing the range. We will test on 8 nodes.

```bash
docker build -f Dockerfile.10 -t vanessa/container-chonks:1-10 .
docker build -f Dockerfile.25 -t vanessa/container-chonks:1-25 .
docker build -f Dockerfile.50 -t vanessa/container-chonks:1-50 .
```

Here they are:

```console
$ docker images | grep chonk
vanessa/container-chonks   1-50      5b96172305c3   4 hours ago    53.7GB
vanessa/container-chonks   1-10      373cfc3e9d88   4 hours ago    10.7GB
vanessa/container-chonks   1-25      65df1c12a308   4 hours ago    26.9GB
```
Let's start with the largest.

```bash
# This took 39 minutes, with one pod/8 failing twice and ErrImgBackoff
kubectl apply -f job-50.yaml
kubectl get pods --watch

# This took 17 minutes
kubectl apply -f job-25.yaml
kubectl get pods --watch

# First pod was running after 13 minutes, finished at 14, second running at 15 finished at 16. Third at 17 minutes.
# I had to --force delete the original chonk (50GB) for these to go from pending to container creating
kubectl apply -f job-25.yaml
kubectl get pods --watch
```

Interesting! The termination is taking just as long - we need to look into what is happening here. Possible ideas:

- termination time (to unmount)

I can see this message in events:

```
62m         Warning   InvalidDiskCapacity                      node/gke-test-cluster-default-pool-8956c06c-w5t0   invalid capacity 0 on image filesystem
```
And the pods are stuck Terminating. We likely need to understand this. There seems to be some issue going on with scheduling and the kubelet with respect to CPU needs, because I had to force delete pods for them to leave Pending.

I am going to predict that failure is mostly related to the size of a layer and not the overall container, but a larger overall container will take longer to pull. So there are two variables - container total size, and layer size, and I'll try to set it up so I have a consistent total size across multiple layer counts. Then we can give advice about if more / fewer layers is better (the doctrine is fewer but if there is a failure/backoff maybe this is wrong). Then the next set of variables that are interesting are the size of cluster, and for that I predict that the probability of failure on any single node is consistent, and so the chance of overall failure goes up. But maybe if you are making a ton of pulls for the same container (this would be a different experiment, maybe thousands of tiny containers?) you might hit a rate limit. What is interesting for this (along with the comparison between registries and assessment of the size of containers is the ecosystem) is also evaluating the pull strategies between different runtimes, which is an OCI maintained standard but I suspect there are subtle differences. For example, I maintain oras-py so I've implemented all of those points (...can't say incredibly well :P)

Final "result" (not really, just subjectively looking) for this 50GB container is 30 minutes! And 1/8 nodes had a backoff / error on pull. I'd bet that would vary by registry, by the container runtime, and by networking for your cluster. Lots of variables to think about.

### Clean Up

When you are done:

```bash
gcloud container clusters delete test-cluster --region=us-central1-a
```
