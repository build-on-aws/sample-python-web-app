#!/bin/bash -xe


# Read the first parameter into $SAMPLE_APP
if [[ "$1" != "" ]]; then
    SAMPLE_APP="$1"
else
    echo "Please specify the location of web application you are trying to deploy."
    exit 1
fi

# # Read the second parameter into $UWSGI_SERVICE_FILE
# if [[ "$2" != "" ]]; then
#     UWSGI_SERVICE_FILE="$2"
# else
#     echo "Please specify the location of the uWSGI systemd service unit file."
#     exit 1
# fi

# # Read the third parameter into $NGINX_CONFIG
# if [[ "$3" != "" ]]; then
#     NGINX_CONFIG="$3"
# else
#     echo "Please specify the location of the nginx config file."
#     exit 1
# fi


# Install OS packages
yum update -y
yum groupinstall -y "Development Tools"
amazon-linux-extras install -y nginx1
yum install -y nginx python3 python3-pip python3-devel
pip3 install pipenv wheel
pip3 install uwsgi

# Install my-web-app into the /home/ec2-user/SampleApp directory
mkdir -p /var/www/SampleApp
cp $SAMPLE_APP /var/www/SampleApp/SampleApp.zip
cd /var/www/SampleApp
unzip SampleApp.zip
rm SampleApp.zip
sudo - pipenv install
usermod -a -G nginx ec2-user
chown ec2-user:nginx -R ./*
chown ec2-user:nginx /var/www
chown ec2-user:nginx /var/www/SampleApp

# Install uWSGI as a systemd service, enable it to run at boot, then start it
#cp $UWSGI_SERVICE_FILE /etc/systemd/system/mywebapp.uwsgi.service
cp sample-app.uwsgi.service /etc/systemd/system/mywebapp.uwsgi.service
mkdir -p /var/log/uwsgi
chown nginx:nginx /var/log/uwsgi
systemctl enable mywebapp.uwsgi.service
systemctl start mywebapp.uwsgi.service

# Copy the nginx config file, then ensure nginx starts at boot, and restart it to load the config
cp nginx-app.conf /etc/nginx/conf.d/nginx-app.conf
systemctl enable nginx.service
systemctl stop nginx.service
systemctl restart nginx.service


echo "Custom configuration for sample application complete."