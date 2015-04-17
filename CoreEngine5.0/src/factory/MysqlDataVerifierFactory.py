# -*- coding: GBK -*-
'''
Created on 2014-6-20

@author: Administrator
'''
#you should check the data in MySQL to verify if your Operation
#is successful in this Class

from basic.MysqlOperator import Mysql
from basic import MysqlConnector, Constants
from basic.Constants import deviceName
from basic.ConfigurationReader import Config
from basic.Constants import updateDevice,CameraConfig,ServerConfig
import time
import logging
import json


log = logging.getLogger("TestMysqlDataVerifier")
class MysqlDataVerifier():
    
    con = None
    def __init__(self):
        #connect to DB
        pass
    def tearDown(self):
        #close DB connection
        MysqlConnector.closeConnection()
        
    def testCorrectnessInDevices(self,models):
        '''
        check if there is a device named  in devices
        '''
        
        try:
            log.debug("test if device added to table devices")
            #select from devices to verify if there is a device named "unittest-amtk"
            config = Config(CameraConfig).getConfig()
            Id = config.get(updateDevice, "device-id")
            
            #the second one is device name
            result = self.isSame(Id, models)
            
            if result:
                log.debug('device Information is same Devices table data.!')
                return True
            else:
                log.debug("added to devices fail,it is different of devices data")
                return False
        except Exception,e:
            log.error("exception, %s", e)

    def isCorrectnessInDsDevice(self):
        try:
            config = Config(CameraConfig).getConfig()
            Id = config.get(updateDevice, "device-id")
            dsDevice = Mysql().getDsDeviceById(Id)
            if dsDevice != None and dsDevice[0][3] == 2:
                return True
            else:
                return False
        except Exception,e:
            log.exception("%s",e)
            pass
        pass
#     def testCorrectnessInDsDeviceInfo(self):
#         '''
#         check if there is a device named "unittest-amtk" in ds_device_info
#         '''
#         try:
#             log.debug("test if device added to ds_device_info")
#             #get device's id whose name is "unittest-amtk" 
#             device = Mysql().getDeviceByName()
#             deviceId = device[0][0]#the first filed in devices is deviceId
#             #select from ds_device_info to verify if there is a device named "unittest-amtk"        
#             dsDeviceInfo = Mysql().getDsDeviceInfo(deviceId)
#             log.debug("ds_device_info=%s", dsDeviceInfo)
#             #the second one is device_info which contains deviceName
#             deviceInfo = dsDeviceInfo[0][2]
#             isDeviceExist = False
#             Real_DeviceName = Config("device-information.cfg").getFromConfig(deviceName, "addedDeviceName")
#             if Real_DeviceName in deviceInfo:
#                 isDeviceExist = True
#                 log.debug("device name in ds_device_info=%s",deviceInfo)
#                 log.debug("added to dsDeviceInfo correctly/success!")
#             else:
#                 log.debug("device name not in ds_device_info")
#             return isDeviceExist
#         except Exception,e:
#             log.error("exception, %s", e)
#             return False
    
#     def testIfDeviceAddedToDs(self):
#         '''
#         get the value of server_id in ds_device_info to see if the device
#         added to DS successfully. 
#         '''
#         try:
#             log.debug("test if device added to a DS")
#             #sleep some time to wait the device added to DS
#             log.debug("sleep 40 seconds to wait DS register")
#             time.sleep(40)
#             device = Mysql().getDeviceByName()
#             deviceId = device[0][0]#the first filed in devices is deviceId
#             dsDeviceInfo = Mysql().getDsDeviceInfo(deviceId)
#             dsId = dsDeviceInfo[0][4]
#             log.debug("ds_device_info=%s", dsDeviceInfo)
#             if dsId == -1:
#                 log.debug('maybe device has not added to DS')
#                 return False
#             return True
#         except Exception,e:
#             log.error("exception, %s", e)
#             return False
        
#     def testMatchUpInChannelDeviceMap(self):
#         '''
#         See if the matchup in channel_device_map is correct
#         '''
#         try:
#             device = Mysql().getDeviceByName()
#             deviceId = device[0][0]
#             
#             #on Kai-node, check the channel_device matchup
#             log.debug("test channel_device_map")
#             map = Mysql().getChannelDeviceMap()
#             log.debug("channel-device-map=%s",map)
#             #if there is device_id in the channel_device_map, then the map is correct
#             if len(map) != 0:
#                 for each in map:
#                     #node_device_id
#                     nodeDeviceId = each[2]
#                     if (nodeDeviceId == deviceId):
#                         log.debug("device_channel map is correct.") 
#             raise Exception("maybe")
#         except Exception,e:
#             log.error("exception, %s", e)
#             raise Exception("device-channel-map exception")
#         #on KUP, the judge process will be different 
    
    def isSame(self,device_id,models):
        #Config file Model information
        config = Config(CameraConfig).getConfig()
        name = config.get(models, "name")
        model_id = config.get(models, "model-id")
        address = config.get(models,"address")
#         lat = config.get(updateDevice,"lat")
#         lng = config.get(updateDevice,"lng")
        host = config.get(models,"host")
        port = config.get(models,"port")
        login = config.get(models,"login")
        passwd = config.get(models,"password")
#         key = config.get(models,"key")
        
        #DB device Information
        device = Mysql().getDeviceById(device_id)
        log.debug("device:%s",device)
        log.debug("name:%s",device[0][1])
        log.debug("key:%s",device[0][2])
        log.debug("host:%s",device[0][3])
        log.debug("lat:%s",device[0][4])
        log.debug("lng:%s",device[0][5])
        log.debug("model-id:%s",device[0][6])
#         log.debug("other:%s",device[0][8])
        
        loginInfo = json.loads(device[0][8])
        log.debug("port:%s",loginInfo["port"])
        
#         print type(device[0][6])
#         print type(model_id)
        booleans = (name == device[0][1] and host == device[0][3] and model_id == str(device[0][6]) and
                    port == loginInfo["port"] and login == loginInfo["login"] and passwd == loginInfo["password"] and address == loginInfo["address"])
        log.debug("Boolean: %s",booleans)
        
        if booleans:
            return True
        else:
            return False
        pass
        
    
    def updataDeviceResult(self):
        #real parm
        config = Config(CameraConfig).getConfig()
        Id = config.get(updateDevice, "device-id")
        result = self.isSame(Id, updateDevice)
        if result:
            return True
        return False
        
#     def testIfDeviceUpdated(self):
#         '''
#         check if the device's host updated to the new one correctly
#         in devices and ds_device_info
#         '''
#         try:
#             log.debug("test if device updated correctly")
#             #get device's id whose name is "unittest-amtk" 
#             device = Mysql().getDeviceByName()
#             deviceId = device[0][0]#the first filed in devices is deviceId
#             updatedHost = device[0][3]
#             log.debug("updated host=%s", updatedHost)
#             
#             #if this device updated correctly in devices
#             hostUpdatedInDevices = False
#             #get the updated host from configuration.cfg
#             intendedHost = Config(CameraConfig).getFromConfigs(Constants.updateDevice, "host")
#             if intendedHost !=  updatedHost:
#                 hostUpdatedInDevices = True
#             
#             #select from ds_device_info to verify if the device's host updated successfully        
#             dsDeviceInfo = Mysql().getDsDeviceInfo(deviceId)
#             log.debug("ds_device_info=%s",dsDeviceInfo)
#             #the second one is device_info which contains device's host
#             deviceInfo = dsDeviceInfo[0][2]
#             hostUpdatedInDsDevInfo = False
#             if intendedHost in deviceInfo:
#                 hostUpdatedInDsDevInfo = True
#             
#             #only if host updated in devices and ds_device_info, the update is successful
#             if hostUpdatedInDevices == False | hostUpdatedInDsDevInfo == False:
#                 log.debug('device updated fail')
#                 raise Exception("device updated fail")
#             
#             #self.assertEqual(hostUpdated, True,"maybe device update fail")
#             log.debug("device updated correctly")
#         except Exception,e:
#             log.error("exception, %s", e)
#             raise Exception("")
        
    def testIfDeviceDeleted(self):
        '''
        check data in devices\ds_device_info, to see if the device is deleted correclty
        '''
        try:
            log.debug("test if device deleted correctly")
            #get device's id whose name is "unittest-amtk" 
            config = Config(CameraConfig).getConfig()
            Id = config.get(updateDevice, "device-id")
            device = Mysql().getDeviceById(Id)
            log.debug("deleted device=%s",device)
#             deviceId = Config(CameraConfig).getFromConfigs(Constants.deleteDevice, "device-id")
            if(len(device) == 0):
                return True
            else:
                log.debug('maybe device deleted fail')
                return False
        except Exception,e:
            log.error("exception, %s", e)
#             return False
        
    def cleanDeviceInfo(self):
#         device = Mysql().getDeviceByName()
#         log.debug("deleted device=%s",device)
        deviceId = Config(CameraConfig).getFromConfigs(Constants.deleteDevice, "device-id")
        result = Mysql().cleanDeviceInfo(deviceId)
        log.debug("clean device, result=%s",result)
    
    def testIfAddedToStreamSessionInfo(self):
        '''
        check if added to stream_session_info correctly
        '''
        deviceId = Config(CameraConfig).getFromConfigs(Constants.deleteDevice, "device-id")
        streamSessionInfo = Mysql().getStreamSessionInfo(deviceId)
        log.debug("streamSessionInfo=%s",streamSessionInfo)
        if streamSessionInfo != None:
            log.debug("add to stream_session_info success.")
            return True
        else:
            log.debug("add to stream_session_info fail.")
            return False
    
    def testIfDelFromStreamSessionInfo(self):
        '''
        check if delete from stream_session_info correctly when the session is timeout
        '''
        #sleep sometime between check the streamSessionInfo
        ttl = Config(CameraConfig).getFromConfigs(Constants.streamControl, "ttl")
        timeToSleep = int(ttl) + 10
        log.debug("sleep %s seconds before test delete stream_session_info", timeToSleep)
        time.sleep(timeToSleep)
        deviceId = Config(CameraConfig).getFromConfigs(Constants.deleteDevice, "device-id")
        streamSessionInfo = Mysql().getStreamSessionInfo(deviceId)
        log.debug("streamSessionInfo=%s",streamSessionInfo)
        if len(streamSessionInfo) == 0:
            log.debug("delete stream_session_info success.")
            return True
        else:
            log.debug("delete from stream_session_info fail.")
            return False
        
    def testConfigurationsHavKUP(self):
        name = "kup-arbiter-host"
        value = Config(ServerConfig).getFromConfigs(Constants.configControl,"kup-arbiter-host")
        configurations = Mysql().getConfigurationsInfo(name,value)
        if len(configurations)!=0:
            log.debug('msg:KUP add success')
            return True
        else:
            log.debug("KUP not set success")
            return False
    #----some auxiliary methods
    def isExist(self):
        pass   
        
        
        