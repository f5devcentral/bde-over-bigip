#!/bin/bash

for n in 20001 20002 20003; do 
    (python /root/workdir/test/send-to-fluentd/$n-send-n-continuously.py 1 &)
done