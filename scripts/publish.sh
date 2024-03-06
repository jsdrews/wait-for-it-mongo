#!/bin/bash
VERSION=$( poetry version -s)

docker push $ORGANISATION/$PROJECT:$VERSION
docker push $ORGANISATION/$PROJECT:latest
