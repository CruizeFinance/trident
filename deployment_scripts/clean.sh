#!/bin/bash
# this file is used to clean the project  from the server so that we can redeploy it.
sudo rm -rf /home/ubuntu/trident
if [ -d /home/ubuntu/trident/ ]; then
    rm -rf /home/ubuntu/trident/
fi
mkdir -vp /home/ubuntu/trident/