#!/bin/sh

set -x

ID=$(docker create rce:latest)
HASH=$(sha256sum $1 | cut -d' ' -f1)
docker cp $1 $ID:/code.c
rm $1

echo 'running' > /app/log/$HASH.log
docker start $ID
sleep 10
docker logs $ID | head -c 1000 > /app/log/$HASH.log
docker stop -t 1 $ID 
docker rm $ID
