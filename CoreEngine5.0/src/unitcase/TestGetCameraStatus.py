'''
Created on 2015-4-16

@author: guanxingquan
'''
from factory.DeviceManagementServerFactory import DeviceManagementServerFactory
from factory.MysqlDataVerifierFactory import MysqlDataVerifier
from factory.DeviceControlServiceFactory import DeviceControlServiceClient
from basic.Constants import onlineDevice,offlineDevice
from time import sleep

class TestGetCameraStatus(object):
    
    def __init__(self):
        self.deviceManage = DeviceManagementServerFactory()
        self.mysqlData = MysqlDataVerifier()
        self.deviceContol = DeviceControlServiceClient()
        pass
    
    def setUp(self):
        pass
    
    def tearDown(self):
        MysqlDataVerifier().cleanDeviceInfo()
        pass
    
    def test_getOnlineDeviceStatus(self):
        '''
        Test online device Status is Online
        '''
        addResult = self.deviceManage.tryToAddDevice(onlineDevice)
        assert addResult
        sleep(40) 
        isconnected = self.mysqlData.isConnected()
        assert isconnected
        connStatus = self.deviceContol.judgeDeviceStatus()
        assert connStatus
        pass
    
    def test_getOfflineDeviceStatus(self):
        '''
        Test offline device Status is offline
        '''
        addResult = self.deviceManage.tryToAddDevice(offlineDevice)
        assert addResult
        sleep(40) 
        isconnected = self.mysqlData.isConnected()
        assert isconnected==False
        disconnected = self.deviceContol.judgeDeviceStatus()
        assert disconnected
        pass
    
    def test_changeStatus(self):
        '''
        Test this Process: online-->offline-->online is success
        '''
        #add a onlineDevice
        addResult = self.deviceManage.tryToAddDevice(onlineDevice)
        assert addResult
        
        #sleep 50s to make sure it will produce a connected event
        sleep(50)
        
        #Now it should be connected
        first_connected = self.mysqlData.isConnected()
        assert first_connected
        
        
        #change to offlineDevice by update an error port to online device
        rightToErr = self.deviceManage.chagePort()
        assert rightToErr
        
        #sleep 50s to produce a disconnented event(int 4)
        sleep(50)
        
        #now should be disconnected
        connected = self.mysqlData.isConnected()
        assert connected==False
        
        #recovery right port
        errorToRight = self.deviceManage.chagePort()
        assert errorToRight
        
        #wait product event
        sleep(50)
        
        #now device should be connected
        sec_connected = self.mysqlData.isConnected()
        assert sec_connected
        
        #test over
        pass
    