#!/bin/bash
apt-get update -y
apt-get install -y python3 python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 bot.py
