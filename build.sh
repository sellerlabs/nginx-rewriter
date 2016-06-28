#!/bin/bash
set -ev
if [ $1 == "test" ]; then
  docker run -it sellerlabs/nginx-rewriter
elif [ $1 == "store-container" ]; then
  docker login -e="$DOCKER_EMAIL" -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
  docker push sellerlabs/nginx-rewriter
fi