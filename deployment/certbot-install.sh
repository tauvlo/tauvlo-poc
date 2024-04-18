#!/bin/bash

# !! Port 80 needs to be accessible from the internet for this to work !!

sudo apt install snapd
sudo apt install nginx
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

sudo certbot --nginx
