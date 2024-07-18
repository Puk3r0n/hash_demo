
<h1 align="center">Deploy the project</h1>

## Description
This project is a Python application designed to download files from a repository
using the Gitea API. It retrieves files recursively, calculates their SHA256 hashes, and logs the 
results using the Loguru logging library.

## Python version
```
    python 3.9
```

## Download the project

```
    git clone git@github.com:Puk3r0n/hash_demo.git
```

```
    cd hash_demo
```

## Сreate a virtual environment and install dependencies

```
    python3 -m venv venv
    source venv/bin/activate
```
## Install dependencies
```
    make dependencies
```

## Run project
```
    make setup
```
