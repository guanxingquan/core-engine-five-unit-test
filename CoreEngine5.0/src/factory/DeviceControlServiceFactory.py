# -*- coding:GBK -*-
'''
Created on 2014-8-18

@author: guanxingquan
'''
from CoreServices import DeviceControlService
from basic.ConfigurationReader import Config
from basic import ThriftClient
from basic.Constants import Arbiter,deleteDevice,CameraConfig,ServerConfig
import logging
log = logging.getLogger('testDeviceControlService')

class DeviceControlServiceClient():
    client = None
    def __init__(self):
        try:
            host = Config(ServerConfig).getFromConfigs(Arbiter,"arbiter-server-host")
            port = Config(ServerConfig).getFromConfigs(Arbiter,"device-control-port")
            self.client = ThriftClient.getThriftClient(host,port,DeviceControlService)
        except Exception,e:
            log.Exception("Exception:%s",e)
            raise Exception("DeviceControlService _init_ Exception")
        
    def judgeDeviceStatus(self):
        '''
        Return True means Online ,else Offline
        '''
        try:
            deviceId = Config(CameraConfig).getFromConfigs(deleteDevice,"device-id")
            result = self.client.getDeviceStatus(deviceId)
            if result == "online":
                log.info("Device Online                OK")
                return True
            elif result == "offline":
                log.info("Device Offline                OK")
                return False
        except Exception,e:
            log.exception("Exception:%s",e)
        