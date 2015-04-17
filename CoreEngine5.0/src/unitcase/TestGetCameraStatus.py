'''
Created on 2015-4-16

@author: guanxingquan
'''
from factory.DeviceManagementServerFactory import DeviceManagementServerFactory
from factory.MysqlDataVerifierFactory import MysqlDataVerifier
from basic.Constants import CameraConfig,onlineDevice,offlineDevice
from time import sleep
def setUp():
    pass

def tearDown():
    MysqlDataVerifier().cleanDeviceInfo()
    pass

def addOnlineDevice():
    addResult = DeviceManagementServerFactory().tryToAddDevice(onlineDevice)
    assert addResult
    sleep(40)
    isInDeServer = MysqlDataVerifier().isCorrectnessInDsDevice()
    assert isInDeServer
    pass

def addOfflineDevice():
    pass

def test_getOnlineStatus():
    pass

def test_getOfflineStatus():
    pass