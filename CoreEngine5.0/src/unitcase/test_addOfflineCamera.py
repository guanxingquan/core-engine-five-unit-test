from factory.DeviceManagementServerFactory import DeviceManagementServerFactory

from basic.Constants import offlineDevice



def test_addOnline():
    DeviceManagementServerFactory().tryToAddDevice(offlineDevice)