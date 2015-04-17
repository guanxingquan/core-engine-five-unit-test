from factory.DeviceManagementServerFactory import DeviceManagementServerFactory

from basic.Constants import onlineDevice



def test_addOnline():
    DeviceManagementServerFactory().tryToAddDevice(onlineDevice)