#!/bin/bash

# Install Mysql
yum update
yum install -y wget
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
rpm -ivh mysql-community-release-el7-5.noarch.rpm
yum update
yum install -y mysql-server
systemctl start mysqld
yum install -y git
mkdir /home/superset
cd /home/superset
git clone https://github.com/analyticsMD/incubator-superset.git
pip install docker-compose
docker login -uqventusci -p
docker pull qventus/superset:0.31.4
cd /home/superset/incubator-superset
git checkout qventus-release-0.31.2
cd contrib/docker
