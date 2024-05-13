# Container Chonks

We want to study the impact of pulling times (at different scales) for different sizes containers, meaning varying individual layer and total container sizes. This entire study is going to be powered by dd, which will allow us to generate files of arbitrary sizes.

 - [test](test): early testing of the design below. What I learned is that we need to likely evaluate the container landscape (average sizes) before deciding on our experiment design. 


Next steps are to sample a Dockerfile set to get container URIs and sizes that people are using.

## Design

This is early thinking for chonk experiments.

### Choosing the maximum size

It looks like the [Default Base Size](https://stackoverflow.com/questions/45479273/is-there-a-recommended-max-size-limit-for-docker-images-as-good-practice) is 100GB (see PR notes [here](https://github.com/moby/moby/pull/14709)) There are a few ways to generate layers of sizes, one is dd, another is head, but I wound up choosing truncate.

```bash
RUN truncate -s 50G layer1 && shred -n 1 RUN head -c 50G /dev/urandom > layer1.txt
RUN dd if=/dev/zero of=file.txt bs=1024 count=10240 
RUN truncate -s 50G layer1 && shred -n 1 layer1
```

This is a limit about the mount I think, and this also means we will need to:

1. map one pod per node
2. ensure the node is large enough for that
3. Give files generated with a particular size in a container a unique name to the container so they are not cached. 

We also should choose a very slim base image and then have an entrypoint command like echo that essentially starts and exits with 0.

### Procedure

```
For each of (approximate) total sizes 10, 25, 50, 75, 100 GB, do:
   Build container with 3 to max layers (127)
     For each registry in Docker Hub, GitHub packages, and Quay.io:
       For each cluster size of 2, 4, 8:
          start a job that will pull the container, time pull and keep track of any events
```

## TODO:

- Build and push all images to each registry (write a script that does this and saves URIs). The script should also get the exact final size.
- Write experiment running script.

### Testing

For testing, we can try 10,20, and 50GB first, and one layer, and see if it works. See the [test](test) directory for this experiment.

## License

HPCIC DevTools is distributed under the terms of the MIT license.
All new contributions must be made under this license.

See [LICENSE](https://github.com/converged-computing/cloud-select/blob/main/LICENSE),
[COPYRIGHT](https://github.com/converged-computing/cloud-select/blob/main/COPYRIGHT), and
[NOTICE](https://github.com/converged-computing/cloud-select/blob/main/NOTICE) for details.

SPDX-License-Identifier: (MIT)

LLNL-CODE- 842614
