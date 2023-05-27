#!/bin/bash -xe
systemctl restart mywebapp.uwsgi.service
systemctl restart nginx.service
