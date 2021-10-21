#!/bin/bash

cdir=`cd $(dirname $0); pwd`;
export HOMEDIR=$cdir/..

chmod -R 777 $HOMEDIR/data/* # permission denied in linux.
chmod 777 $HOMEDIR/logs/fluentd/*
rm -rf $HOMEDIR/data/kafka/* # remove legacy kafka data for no persistence.

# ERROR: [1] bootstrap checks failed
# [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
sysctl -w vm.max_map_count=262144

# docker-compose -f $HOMEDIR/deps/conf.d/docker-compose.yml $demo_yml_option down # force remove and recreate the network
docker-compose -f $HOMEDIR/deps/conf.d/docker-compose.yml up -d --force-recreate --remove-orphans

# sleep 1
# for n in "CTRLBOX" "FLUENTD"; do 
#     docker ps | grep "$n" > /dev/null
#     if [ $? -ne 0 ]; then echo "$n not found, cannot forward, quit."; exit 1; fi
# done

# docker exec CTRLBOX "/root/workdir/scripts/cmds-in-ctrlbox/setup-efk.sh"

# x='
# 0. start docker containers..
# 1. kibana:          import kibana settings
# 2. elasticsearch:   create index mapping

# 3. edit .setup.rc.
# (. bigip:           create a fake virtual server on bigip)

# 4. bigip:           create logging irule
# 5. bigip:           setup bigip virtual server irule

# 6. ctrlbox          run python http-test.py
# '
