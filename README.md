[![CircleCI](https://dl.circleci.com/status-badge/img/gh/snyk/code-review-exercise-python/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/snyk/code-review-exercise-python/tree/main)

# README

A web server that provides a basic HTTP API for querying the dependency
tree of an [npm](https://npmjs.org) package.

## Prerequisites

- [Python 3.13](https://www.python.org/downloads/release/python-3131/)

## Getting Started

### Running in a virtual environment

To install dependencies and start the server in development mode:

```sh
poetry install
poetry run uvicorn app:app --host="127.0.0.1" --port="3000" --log-level="info" --reload
```

### Running in a Docker container

For convenience a `Makefile` is provided to run Docker commands

#### Building the Docker image

`make build`

#### Building the Docker image with the development tools

`make build-dev`

#### Running the Docker container

```shell
make runserver
```

### API

The server will now be running on an available port (defaulting to 3000) and will restart on changes to the files in `/npm_deps`

The server contains two endpoints
`- /healthcheck`

- `/package/:packageName/:packageVersion`

Here is an example that uses `curl` and
`jq` to fetch the dependencies for `react@16.13.0`

```sh
curl -s http://localhost:3000/package/react/16.13.0 | jq .
```

## Testing

You can run the tests with this command:

```sh
poetry run pytest
```

You can alternatively run the tests inside the Docker image (built in development mode):

```sh
make test
```

## Pre-commit

The code is linted using `pre-commit`, you can run this via:

```sh
pre-commit run -a -v
```

or using Docker

```sh
make lint-all
```
