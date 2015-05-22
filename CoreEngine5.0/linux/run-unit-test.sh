#!/bin/sh
#Run Client
#Created by guanxingquan
#Time 2015-04-16

cd /home/node/CoreEngine5.0/src/unitcase/client
nosetests -s -v --with-xunit --xunit-file=/home/node/CoreEngine5.0/log/nosetest.xml >> /home/node/CoreEngine5.0/log/nosetest.log 2>&1 &
echo "*******TEST START******"
tailf /home/node/CoreEngine5.0/log/nosetest.log
