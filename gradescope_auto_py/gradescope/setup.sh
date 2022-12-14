#!/usr/bin/env bash

# install python pips
apt-get install python3-pip
pip3 install virtualenv

# setup virtual environment and install necessary packages
virtualenv venv
source venv/bin/active
pip install gradescope_auto_py
pip install -r requirements.txt