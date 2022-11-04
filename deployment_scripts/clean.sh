#!/bin/bash

sudo rm -rf /home/ubuntu/trident
if [ -d /home/ubuntu/trident/ ]; then
    rm -rf /home/ubuntu/trident/
fi
mkdir -vp /home/ubuntu/trident/