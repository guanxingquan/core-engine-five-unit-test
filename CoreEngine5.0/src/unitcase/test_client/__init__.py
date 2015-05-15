'''
Create 2015-04-17
@author: Guan Xingquan
'''

from factory.DeviceManagementServerFactory import DeviceManagementServerClient
from factory.MysqlDataVerifierFactory import MysqlDataVerifier
from basic.Constants import onlineDevice
from time import sleep
from basic import LogUtil,GlobalFunction

log = LogUtil.getLog("ClientInit")

def setUp(self):
    print "Init a online device..."
    addResult = DeviceManagementServerClient().tryToAddDevice(onlineDevice)
    assert addResult
    sleep(60)
    isconnected = MysqlDataVerifier().isConnected()
    assert isconnected
    pass

def tearDown(self):
    print "Clean device information..."
    GlobalFunction.CommonInter().clearStorageData()
    DeviceManagementServerClient().testDeleteDevice()
    MysqlDataVerifier().cleanDeviceInfo()
    pass

