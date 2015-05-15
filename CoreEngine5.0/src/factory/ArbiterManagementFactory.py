'''
Created on 2015-4-29

@author: kaisquare
'''
from basic import ThriftClient
from ArbiterCommsAPI import ArbiterManagementService 
from basic.ConfigurationReader import Config
from basic.Constants import ServerConfig,CameraConfig,Arbiter,updateDevice,streamControl
import basic.LogUtil
import time
import uuid
import json
from _mysql import result

log = basic.LogUtil.getLog("ArbiterClient")
class ArbiterClient(object):
    '''
    Arbiter Management Service Client
    '''

    def __init__(self):
        '''
        Constructor
        '''
        try:
            host = Config(ServerConfig).getFromConfig(Arbiter, "arbiter-server-host")
            port = Config(ServerConfig).getFromConfig(Arbiter, "arbiter-port")
            self.client = ThriftClient.getThriftClient(host, port, ArbiterManagementService)
        except Exception,e:
            log.error("DeviceManagementServer error:%s",e)
            raise Exception("DeviceDataReceiverService setup:")
    
    def sendEventToArbiter(self):
        deviceId = Config(CameraConfig).getFromConfig(updateDevice, "device-id")
        uuId = uuid.uuid1()
        Config(ServerConfig).writeToConfig(streamControl,"event-id",str(uuId))
        channel = Config(ServerConfig).getFromConfig(streamControl, "channel-id")
        eventType = Config(ServerConfig).getFromConfig(streamControl, "event-type")
        eventTime = int(time.time())
        duration = Config(ServerConfig).getFromConfig(streamControl, "duration")
        datas = {"eventId":str(uuId),"duration":int(duration)}
        stringData = json.dumps(datas)
        binaryData = None
        try:
            result = self.client.sendEventData(deviceId, channel, eventType, eventTime, stringData, binaryData)
            return result
        except Exception,e:
            log.exception("%s",e)
    
    
            
        