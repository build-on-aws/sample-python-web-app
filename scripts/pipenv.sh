#!/bin/bash -xe

chown nginx:nginx -R /var/www/SampleApp/
cd /var/www/SampleApp
/usr/local/bin/pipenv install
