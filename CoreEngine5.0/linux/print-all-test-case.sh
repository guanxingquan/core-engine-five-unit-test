#!/bin/sh
#Run Client
#Created by guanxingquan
#Time 2015-04-16
echo "TEST START"
cd /home/node/CoreEngine5.0/src/unitcase/
nosetests --collect-only -v >> /home/node/CoreEngine5.0/log/nosetest.log
tailf /home/node/CoreEngine5.0/log/nosetest.log

