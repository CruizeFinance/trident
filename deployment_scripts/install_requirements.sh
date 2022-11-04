#!/bin/bash
sudo pip3 install virtualenv
virtualenv env
source env/bin/activate
echo $PWD
req="/../requirements.txt"
script_dir=$(dirname "$0")
pip install -r "$script_dir$req
