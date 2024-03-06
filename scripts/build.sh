#!/bin/bash
VERSION=$( poetry version -s )

if [ -z "$HTTPS_PROXY" ]
then
    docker build -t ${ORGANISATION}/${PROJECT}:${VERSION} .
else
    docker build --build-arg HTTPS_PROXY=$HTTPS_PROXY -t ${ORGANISATION}/${PROJECT}:${VERSION} .
fi

docker tag ${ORGANISATION}/${PROJECT}:${VERSION} ${ORGANISATION}/${PROJECT}:latest
