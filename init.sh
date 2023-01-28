#!/bin/bash

filename="blog_data.json"
# build migrations 
python manage.py migrate
# load data
python manage.py loaddata $filename