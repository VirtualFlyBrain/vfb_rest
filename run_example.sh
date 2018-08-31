#!/bin/bash
docker build -t vfbidserver .
docker run --rm -p 8000:8000 --net=dockernet --env=KBpassword=neo4j/neo -v -ti vfbidserver
