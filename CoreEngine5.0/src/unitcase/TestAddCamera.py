'''
Created on 2015-4-10
@author: kaisquare

Edit on 2015-4-14
@author: guanxingquan

'''
from factory.DeviceManagementServerFactory import DeviceManagementServerFactory
from factory.MysqlDataVerifierFactory import MysqlDataVerifier
from basic.Constants import deviceModelA,deviceModelB,deviceModelC,deviceModelD
from basic.ConfigurationReader import Config
from basic.Constants import globalParameter,CameraConfig

class TestAddOfflineCamera(object):
    '''
    Add a lot of Camera Model
    '''

    def __init__(self):
        '''
        init Server necessary
        '''
        self.dms = DeviceManagementServerFactory()
        self.dataVerifier = MysqlDataVerifier()
        pass
    
    def setUp(self):
        Config(CameraConfig).writeToConfig(globalParameter, "snapshot-recording-enabled", "false")
        Config(CameraConfig).writeToConfig(globalParameter, "cloud-recording-enabled", "false")
        pass
    
    def tearDown(self):
        '''
        Clear Device Inforation
        '''
        self.dataVerifier.cleanDeviceInfo()
        pass
    
    def testcase_addCameraA(self):
        '''
        Add Camera name is !@#% Fail
        '''
        result = self.dms.tryToAddDevice(deviceModelA)
#         assert result
        isInDevices = self.dataVerifier.testCorrectnessInDevices(deviceModelA)
#         assert isInDevices
        if result and isInDevices:
            assert True
        else:
            assert False
        
    def testcase_addCameraB(self):
        '''
        Add Camera host is:360.480.200.118 Fail
        '''
        result = self.dms.tryToAddDevice(deviceModelB)
#         assert result
        isInDevices = self.dataVerifier.testCorrectnessInDevices(deviceModelB)
#         assert isInDevices
        if result and isInDevices:
            assert True
        else:
            assert False
    
    def testcase_addCameraC(self):
        '''
        Add Camera port is 80r3 Fail
        '''
        result = self.dms.tryToAddDevice(deviceModelC)
#         assert result
        isInDevices = self.dataVerifier.testCorrectnessInDevices(deviceModelC)
#         assert isInDevices
        if result and isInDevices:
            assert False
        else:
            assert True
    
    def testcase_addCameraD(self):
        '''
        Add Camera password is 11*@#$TY&1==1
        '''
        result = self.dms.tryToAddDevice(deviceModelD)
#         assert result
        isInDevices = self.dataVerifier.testCorrectnessInDevices(deviceModelD)
#         assert isInDevices
        if result and isInDevices:
            assert True
        else:
            assert False
    
    