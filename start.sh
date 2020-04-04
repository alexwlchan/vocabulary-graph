#!/usr/bin/env bash

set -o errexit
set -o nounset

pip3 install --user -r requirements.txt
gunicorn --bind "0.0.0.0:5000" --workers 4 app:app
