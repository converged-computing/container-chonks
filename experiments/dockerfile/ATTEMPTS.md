# Attempts

## Attempt 1

> This did not work (still) because of API limits.

We are going to programatically get Dockerfile from GitHub. While we could do a clone to search for them across a repository, it's more a convention to have one at the top level, so we are going to guess the path, trying both master and main. Since the GitHub API limits to 1K results, we are going to search in the range of a week.

```bash
pip install rse
export GITHUB_TOKEN=xxxxxxxxx
python search.py
```
