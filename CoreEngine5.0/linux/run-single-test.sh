#!/bin/sh
#Run Client
#Created by guanxingquan
#Time 2015-04-16

cd /home/node/CoreEngine5.0/src/unitcase/test_client
echo "****************************" >> /home/node/CoreEngine5.0/log/nosetest.log
echo "*******  Test Start  ******" >> /home/node/CoreEngine5.0/log/nosetest.log
echo "****************************" >> /home/node/CoreEngine5.0/log/nosetest.log
nosetests -s -v Test1_Recording.py >> /home/node/CoreEngine5.0/log/nosetest.log 2>&1 &

tailf /home/node/CoreEngine5.0/log/nosetest.log
