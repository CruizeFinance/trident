#!/bin/bash

gunicorn --bind 0.0.0.0:8000 settings_config.wsgi
sudo systemctl restart gunicorn