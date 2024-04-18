#!/bin/bash
source /opt/miniconda3/bin/activate base

cd /opt/tauvlo-backend/source
git pull
pip install -r requirements.txt
bash start-server.sh
