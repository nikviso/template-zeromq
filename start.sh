#!/bin/bash

#set -m
#set -e

while true
    if ! ps ax | grep python3 | grep zmqserver.py | grep -v grep > /dev/null; then
       cd /usr/zmqserver/
       screen -S test -d -m ./zmqserver.py
    fi
    do sleep 3
done
