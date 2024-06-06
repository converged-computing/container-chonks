# Dockerfile

## Design

This could be a really interesting study. I want to look at:

 - Across a set of ML orgs and research software containers, get a list of unique containers. For each:
   - Assess current total size and size of layers (an average? distribution?) Try to describe distribution?
   - Look at containers over time (represented by sorted version tags, I have a library that does this) and look at how the size / layer metrics change.
   
What we want to know from the above is, what does the "average" container look like in terms of size, both total and in layers, and then how has it changed over time. As a sub-analysis we can say something about the percentage of research software projects (from the RSEPedia) that provide containers, period.

Given the above, we can then create an experiment that properly measures just outside of the range of what people are actually building, min and max wise. Questions we want to answer:

1. What is the tradeoff between container size (total vs. layers)?
2. It it better to have fewer large layers or more smaller layers?
3. Can we determine redundandy of layers across containers (arguably that is a good thing)
4. Given the needs of storage and time to pull, what are strategies around that?

For the third point, it would be really useful to see some kind of overlap _between_ layers of containers. For example, if I'm running a bunch of ML containers on a cluster, it obviously would be better for storage to have many containers share the same layers. But what does it mean, design wise, to do that? For the fourth point, I'd like to investigate and test some of the caching or optimization strategies so, for example, we don't spend a ton of money on pulling containers alone.

## Parsing

Instead of trying to sample across all Dockerfile, let's sample those we find in GitHub organizations that we know do a lot of machine learning, etc. We will take two approaches:

**GitHub orgs**

- start with a list of GitHub orgs (e.g., nvidia, Hugging Face) and list repos
- clone all repos and find all Dockerfile
- get FROM name in Dockerfile
  - for each unique FROM, get the container tags, and sort across time
  - determine how size has changed over time (getting larger)?
  - create a distribution of sizes

```bash
export GITHUB_TOKEN=xxxxxxxxx
python scripts/parse_repos.py
```

**Software Databases**

We can do the same procedure, but just searching repositories in the [Research Software encyclopedia](https://rseng.github.io/software) to get a sampling of projects in the more rse (or closer to hpc maybe?) ecosystem. If bioconda containers also has a sampling of a different community, I have almost 10k known container URIs in shpc-registry.

```bash
git clone https://github.com/rseng/software /tmp/software
python scripts/parse_rse_repos.py --settings-file /tmp/software/rse.ini
python scripts/summarize_dockerfile.py
```

Stats:

- Total Dockerfile across project: 77449
- 694/4621 RSEng repos have at least one Dockerfile

Dragonfly?

## Analysis

```bash
python scripts/plot-layers.py
```

How many unique repositories (with many tags each)?
- 444

How many unique images?
- 56122

How many layers?
- 209505

Here are outputs from the script, first, the averages for layers and images:

```console
Mean by image: 18349246051.69792
Std by image: 79008670679.2305
Min by image: 1376848
Max by image: 2077795078486

Mean by image: 17.09 GB
Std by image: 73.58 GB
Min by image: 1.31 MB
Max by image: 1.89 TB    
```

And now breakdown by year:

```console
=== YEAR 2014
Mean by image: 191.8 MB
Std by image: 236.28 MB
Min by image: 24.73 MB
Max by image: 358.88 MB

=== YEAR 2015
Mean by image: 289.79 MB
Std by image: 202.29 MB
Min by image: 50.93 MB
Max by image: 664.97 MB

=== YEAR 2016
Mean by image: 3.14 GB
Std by image: 8.81 GB
Min by image: 2.54 MB
Max by image: 65.28 GB

=== YEAR 2017
Mean by image: 6.74 GB
Std by image: 44.69 GB
Min by image: 1.31 MB
Max by image: 798.86 GB

=== YEAR 2018
Mean by image: 8.63 GB
Std by image: 54.12 GB
Min by image: 1.97 MB
Max by image: 1.08 TB

=== YEAR 2019
Mean by image: 16.84 GB
Std by image: 50.08 GB
Min by image: 5.48 MB
Max by image: 769.4 GB

=== YEAR 2020
Mean by image: 19.15 GB
Std by image: 64.94 GB
Min by image: 4.07 MB
Max by image: 1.13 TB

=== YEAR 2021
Mean by image: 18.55 GB
Std by image: 52.28 GB
Min by image: 3.7 MB
Max by image: 546.94 GB

=== YEAR 2022
Mean by image: 25.65 GB
Std by image: 102.51 GB
Min by image: 9.23 MB
Max by image: 1.44 TB

=== YEAR 2023
Mean by image: 23.26 GB
Std by image: 100.67 GB
Min by image: 5.45 MB
Max by image: 1.73 TB

=== YEAR 2024
Mean by image: 16.91 GB
Std by image: 87.57 GB
Min by image: 1.84 MB
Max by image: 1.89 TB
```

Here are some interesting plots that show the pattern - these take the bytes and convert to log scale for easier reading.

![img/all_size_by_year_all_size_by_year.png](img/all_size_by_year_all_size_by_year.png)
![img/size_by_year_size_by_year.png](img/size_by_year_size_by_year.png)
![img/total_size_by_year_total_size_by_year.png](img/total_size_by_year_total_size_by_year.png)


Next:

 - Do we want to derive reasonable ranges / sizes from this to test pulling scenarios for?
 - How do we want to use config data (that has per layer instructions that can be tokenized)
   - We also have all the Dockerfile directives - ENV, WORKDIR, etc.
 - Should we focus on specific containers and look at some change over time?

## Attempt 1

> This did not work (still) because of API limits.

We are going to programatically get Dockerfile from GitHub. While we could do a clone to search for them across a repository, it's more a convention to have one at the top level, so we are going to guess the path, trying both master and main. Since the GitHub API limits to 1K results, we are going to search in the range of a week.

```bash
pip install rse
export GITHUB_TOKEN=xxxxxxxxx
python search.py
```


