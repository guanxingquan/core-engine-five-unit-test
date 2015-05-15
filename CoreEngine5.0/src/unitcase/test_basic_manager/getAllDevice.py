'''
Created on 2015-4-16

@author: kaisquare
'''

from factory.DeviceManagementServerFactory import DeviceManagementServerClient

class TestGetAllDevice(object):
    '''
    Test ListDevices()
    '''


    def __init__(self):
        '''
        '''
        self.deviceManage = DeviceManagementServerClient()
        
    def test_getDeviceList(self):
        '''
        Get all device
        '''
        result = self.deviceManage.getAllDevices()
        assert result