#!/bin/bash
pkill -9 celery
celery worker -A creams_project & celery -A creams_project beat & celery flower -A creams_project --conf=./creams_project/flowerconfig.py
sleep 5
