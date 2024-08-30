#! /usr/bin/env bash

# Read .env file
export $(grep -v '^#' .buildenv | xargs)

docker build \
    --build-arg PYTHON_VERSION=$PYTHON_VERSION \
    --tag $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG \
    --tag $DOCKERHUB_USER/$IMAGE_NAME:latest \
    "$@" \
    .
