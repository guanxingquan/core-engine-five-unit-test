'''
Created on 2015-4-16

@author: kaisquare
'''

from factory.DeviceManagementServerFactory import DeviceManagementServerFactory

class TestGetAllDevice(object):
    '''
    Test ListDevices()
    '''


    def __init__(self):
        '''
        '''
        self.deviceManage = DeviceManagementServerFactory()
        
    def test_getDeviceList(self):
        '''
        Get all device
        '''
        result = self.deviceManage.getAllDevices()
        assert result