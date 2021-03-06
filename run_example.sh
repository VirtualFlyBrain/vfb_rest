#!/bin/bash
docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet
docker build -t vfbidserver .
docker run --rm -p 8000:8000 --net=dockernet --env=KBpassword=neo4j/neo -v  -ti vfbidserver

#CREATE (n:Property {iri:'http://purl.org/dc/elements/1.1/contributor',short_form:'contributor',label:'contributor'})
