'''
Created on 2015-04-14

@author: guanxingquan
'''
import time
from factory.DeviceManagementServerFactory import DeviceManagementServerFactory
from factory.MysqlDataVerifierFactory import MysqlDataVerifier
from basic.Constants import deviceModelA
from basic.ConfigurationReader import Config
from basic.Constants import globalParameter,CameraConfig

class TestDeleteCamera(object):
    '''
    Test delete Camera
    '''


    def __init__(self):
        '''
        Init some Service
        '''
        self.deviceManage = DeviceManagementServerFactory()
        self.mysqlData = MysqlDataVerifier()
        
    def setUp(self):
        '''
        The premise:
            need a camera have in device server
        '''
        Config(CameraConfig).writeToConfig(globalParameter, "snapshot-recording-enabled", "false")
        Config(CameraConfig).writeToConfig(globalParameter, "cloud-recording-enabled", "false")
        result = self.deviceManage.tryToAddDevice(deviceModelA)
        assert result
        inresult = self.mysqlData.testCorrectnessInDevices(deviceModelA)
        assert inresult
        time.sleep(5)
    
    def tearDown(self):
        '''
        The end:
            need to clear test data when test end
        '''
        self.mysqlData.cleanDeviceInfo()
    
    def testcase_DeleteCamera(self):
        '''
        Test Delete Camera
        '''
        result = self.deviceManage.testDeleteDevice()
        deleteResu = self.mysqlData.testIfDeviceDeleted()
        if result and deleteResu:
            assert True
        else:
            assert False
        
        pass
    
    
    
    