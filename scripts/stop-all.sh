#!/bin/bash 

cdir=`cd $(dirname $0);pwd`
export HOMEDIR=$cdir/..

docker-compose -f $HOMEDIR/deps/conf.d/docker-compose.yml down

