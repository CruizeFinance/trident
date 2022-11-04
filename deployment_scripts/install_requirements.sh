#!/bin/bash

sudo apt-get install python3-pip python3-dev nginx
sudo apt-get install -y python-psycopg2 libncurses5-dev libffi libffi-devel libxml2-devel libxslt-devel libxslt1-dev
sudo apt-get install -y python-lxml python-devel gcc patch python-setuptools
sudo apt-get install -y gcc-c++ flex epel-release
cp /home/ubunt/.env /home/ubuntu/trident/
sudo pip3 install virtualenv
virtualenv env
source env/bin/activate
echo $PWD
req="/../requirements.txt"
script_dir=$(dirname "$0")
pip install -r $script_dir$req
