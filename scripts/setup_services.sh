#!/bin/bash -xe
## Install uWSGI as a systemd service, enable it to run at boot, then start it
cp /var/www/SampleApp/sample-app.uwsgi.service /etc/systemd/system/mywebapp.uwsgi.service
mkdir -p /var/log/uwsgi
chown nginx:nginx /var/log/uwsgi
systemctl enable mywebapp.uwsgi.service

## Copy the nginx config file, then ensure nginx starts at boot, and restart it to load the config
cp /var/www/SampleApp/nginx-app.conf /etc/nginx/conf.d/nginx-app.conf
mkdir -p /var/log/nginx
chown nginx:nginx /var/log/nginx
systemctl enable nginx.service
