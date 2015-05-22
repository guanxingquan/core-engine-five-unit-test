#!/bin/sh
#Run Client
#Created by guanxingquan
#Time 2015-04-16
ps -ef | grep nosetests | awk '{print $2}' | xargs kill -9
echo "Nose Stoped"
#cd /home/node/CoreEngine5.0/src/unitcase/
#nosetests --collect-only -v >> /home/node/CoreEngine5.0/log/nosetest.log
#tailf /home/node/CoreEngine5.0/log/nosetest.log

