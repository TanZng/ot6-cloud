#!/bin/sh
# go to the spider directory
cd /opt/repo/project
# run the spider
/usr/local/bin/scrapy crawl product --logfile $2 -a location=$1
