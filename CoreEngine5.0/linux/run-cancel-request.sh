#!/bin/sh
#Run Client
#Created by guanxingquan
#Time 2015-04-16

cd /home/ubuntu/CoreEngine5.0/src/unitcase/test_kaiup_server
echo "" >> /home/ubuntu/CoreEngine5.0/log/nosetest.log
echo "****************************" >> /home/ubuntu/CoreEngine5.0/log/nosetest.log
echo "*******  Test Start  ******" >> /home/ubuntu/CoreEngine5.0/log/nosetest.log
echo "****************************" >> /home/ubuntu/CoreEngine5.0/log/nosetest.log
nosetests -s -v test_kaiup_stopped_request.py >> /home/ubuntu/CoreEngine5.0/log/nosetest.log 2>&1 &

tailf /home/ubuntu/CoreEngine5.0/log/nosetest.log
