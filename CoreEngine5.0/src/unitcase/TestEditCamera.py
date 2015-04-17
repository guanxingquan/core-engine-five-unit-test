'''
Created on 2015-4-14

@author: guanxingquan
'''
import time
from factory.DeviceManagementServerFactory import DeviceManagementServerFactory
from factory.MysqlDataVerifierFactory import MysqlDataVerifier
from basic.Constants import deviceModelA
from basic.ConfigurationReader import Config
from basic.Constants import globalParameter,CameraConfig

class TestEditCamera(object):
    '''
    Test Update Camera
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
        self.deviceManage.tryToAddDevice(deviceModelA)
        result = self.mysqlData.testCorrectnessInDevices(deviceModelA)
        assert result
        time.sleep(5)
    
    def tearDown(self):
        '''
        The end:
            need to clear test data when test end
        '''
        self.mysqlData.cleanDeviceInfo()
        
        
    def testcase_EditCamera(self):
        '''
        Test for Update
        '''
        result = self.deviceManage.testUpdateDevice()
#         assert result
        updataResu = self.mysqlData.updataDeviceResult()
#         assert updataResu
        if result and updataResu:
            assert True
        else:
            assert False
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    