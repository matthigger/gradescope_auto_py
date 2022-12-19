#!/usr/bin/env bash

# install python pips
apt-get install python3-pip
pip3 install virtualenv

# setup virtual environment and install necessary packages
virtualenv venv
source venv/bin/active
pip3 install gradescope_auto_py
pip3 install -r requirements.txt