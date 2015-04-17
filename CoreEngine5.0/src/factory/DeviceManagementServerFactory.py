# -*- coding: GBK -*-
'''
  Created on 2014-6-18

  @author: lizhinian
  
  changed on 2015-04-14
  @author: guanxingquan
'''

from CoreServices import DeviceManagementService
from basic.ConfigurationReader import Config
from CoreServices.ttypes import DeviceDetails
from basic import ThriftClient
from basic.Constants import Arbiter,globalParameter,deviceName
from basic.Constants import onlineDevice,updateDevice,deleteDevice
from basic.Constants import configControl,videoStrategy,photoStrategy
from basic.Constants import CameraConfig,ServerConfig
# from arbiter.utils.Constants import streamControl
import logging
import time
from basic.MysqlOperator import Mysql
#log = logging.getLogger("TestDeviceManagementServer")

log = logging.getLogger("TestDeviceManagementServer")
class DeviceManagementServerFactory():
    client = None 
    def __init__(self):
        try:
            host = Config(ServerConfig).getFromConfigs(Arbiter, "arbiter-server-host")
            port = Config(ServerConfig).getFromConfigs(Arbiter, "device-management-server-port")
            self.client = ThriftClient.getThriftClient(host, port, DeviceManagementService)
        except Exception,e:
            log.error("DeviceManagementServer error:%s",e)
            raise Exception("DeviceManagementServer setup!")
    
    def tearDown(self):
        ThriftClient.closeThriftClient()
        
    def getDeviceModel(self):
        '''
        Will get a List about all model in device service
        '''
        modelLists = self.client.listModels()
        for model in modelLists:
            print model
        pass
    
    def getAllDevices(self):
        client_list = self.client.listDevices("all").sort()
        log.debug("The List through Client is %s",client_list)
        db_list = Mysql().getDevicesList().sort()
        log.debug("The list from database is %s",db_list)
        result = cmp(client_list, db_list)
        log.debug("The Comparison result is [%s]",result)
        if result == 0:
            return True
        else:
            return False
        pass
    
    def tryToAddDevice(self,models):
        try:
            log.debug("test add device")
            name = Config(CameraConfig).getFromConfig(models,"name")
            deviceDetails = self.getDeviceDetails(models,True)
            result = self.client.addDevice(deviceDetails)
            log.debug("add device=%s,result=%s", deviceDetails, result)
            if result:
                log.debug("add device success")
                Config(CameraConfig).writeToConfig(deviceName, "addedDeviceName", name)
                Config(CameraConfig).writeToConfig(updateDevice, "device-id", result)
                Config(CameraConfig).writeToConfig(deleteDevice, "device-id", result)
                return True
            else:
                log.debug('add device to Arbiter fail')
                return False
        except Exception,e:
            log.error('Error:%s',e)
    
    def beginVideoRecording(self):
        '''
           start video  
        '''
        Config(CameraConfig).writeToConfig(onlineDevice, "cloud-recording-enabled","true")
        deviceDetail = self.getDeviceDetails(onlineDevice,False)
        result = self.client.updateDevice(deviceDetail)
        log.debug("begin video recording, result : %s",result)
        return result
    
    def stopVideoRecording(self):
        Config(CameraConfig).writeToConfig(onlineDevice, "cloud-recording-enabled","false")
        deviceDetail = self.getDeviceDetails(onlineDevice,False)
        result = self.client.updateDevice(deviceDetail)
        log.debug("stop video recording, result : %s",result)
        return result
    
    def testVideoStrategy(self):
        
        try:
            log.debug('Test Video Strategy')
            chunk_size = Config(ServerConfig).getFromConfigs(configControl,"chunk-size")
            result = self.beginVideoRecording()
            if result:
                time.sleep(40)
            
            istrue = True
            v_sum = 0
            while istrue:
                current_time_in_seconds = time.time()
                localtime_in_seconds = time.localtime(current_time_in_seconds)
                utc_time = time.strftime("%d%m%Y%H%M%S",time.gmtime(current_time_in_seconds))
                localtime = time.strftime("%d%m%Y%H%M%S",localtime_in_seconds)
                minutes = time.strftime("%M",localtime_in_seconds)
                seconds = time.strftime('%S',localtime_in_seconds)
                
                if eval(minutes)%(int)(chunk_size)==0 and seconds=="00":
                    if v_sum==0:
                        Config(ServerConfig).writeToConfig(videoStrategy, "liveview-begin-time-UTC",utc_time)
                        Config(ServerConfig).writeToConfig(videoStrategy, "liveview-begin-time-local",localtime)
                    else:
                        Config(CameraConfig).writeToConfig(onlineDevice, "cloud-recording-enabled","true")
                        self.client.updateDevice(self.getDeviceDetails(onlineDevice,False))
                        
                    log.debug('msg:the next will sleep 2*60*3s~')
                    
                    v_sum = v_sum + 1
                    time.sleep(eval(chunk_size)*60*2)
                    Config(CameraConfig).writeToConfig(onlineDevice, "cloud-recording-enabled","false")
                    deviceDetail2 = self.getDeviceDetails(onlineDevice,False)
                    self.client.updateDevice(deviceDetail2)
                    
                    if v_sum == 2:
                        Config(ServerConfig).writeToConfig(videoStrategy, "liveview-end-time-UTC",time.strftime("%d%m%Y%H%M%S",time.gmtime()))
                        Config(ServerConfig).writeToConfig(videoStrategy, "liveview-end-time-local",time.strftime("%d%m%Y%H%M%S",time.localtime()))
                        istrue = False
                    if v_sum == 1:
                        time.sleep(eval(chunk_size)*30)
                    log.debug('the %d cycle end',v_sum)
            
            #when the while end
            log.debug('TestVideoStrategy success!')
            return True
        
        except Exception,e:
            log.error('error:%s',e)
            log.debug('The Test Strategy start fail')
            return False
     
    def testPhotoStrategy(self):
        p_sum = 0
        try:
            log.debug('Test Image Strategy')
            interval = Config(CameraConfig).getFromConfigs(onlineDevice,"snapshot-recording-interval")
            Config(CameraConfig).writeToConfig(onlineDevice, "snapshot-recording-enabled","true")
            deviceDetail1 = self.getDeviceDetails(onlineDevice,False)
            result = self.client.updateDevice(deviceDetail1)
            log.debug('result:%s',result)
            
            # sleep 40 seconds after begin image recording, waiting DS to register the device
            if result and p_sum==0:
                time.sleep(40)
            istrue = True
            while istrue:
                current_time_in_seconds = time.time()
                seconds = time.strftime('%S',time.localtime(current_time_in_seconds))
                if eval(str(current_time_in_seconds))%eval(interval)==0 and eval(str(seconds))%eval(interval)==0:
                    if p_sum==0:
                        Config(ServerConfig).writeToConfig(photoStrategy, "photo-begin-time-local",time.strftime("%d%m%Y%H%M%S",time.localtime(current_time_in_seconds)))
                        Config(ServerConfig).writeToConfig(photoStrategy, "photo-begin-time-UTC",time.strftime("%d%m%Y%H%M%S",time.gmtime(current_time_in_seconds)))
                    else:
                        Config(CameraConfig).writeToConfig(onlineDevice, "snapshot-recording-enabled","true")
                        self.client.updateDevice(self.getDeviceDetails(onlineDevice,False))
                    p_sum = p_sum + 1
                    log.debug('msg:sleep 60s')
                    time.sleep(eval(interval)*12)
                    
                    # stop image recording
                    Config(CameraConfig).writeToConfig(onlineDevice, "snapshot-recording-enabled","false")
                    deviceDetail2 = self.getDeviceDetails(onlineDevice,False)
                    result = self.client.updateDevice(deviceDetail2)
                    if result==True and p_sum==1:
                        log.debug('msg:sleep 60s')
                        time.sleep(eval(interval)*12)
                        log.debug('waiting  next~')
                    if p_sum == 2:
                        Config(ServerConfig).writeToConfig(photoStrategy, "photo-end-time-UTC",time.strftime("%d%m%Y%H%M%S",time.gmtime()))
                        Config(ServerConfig).writeToConfig(photoStrategy, "photo-end-time-local",time.strftime("%d%m%Y%H%M%S",time.localtime()))
                        istrue = False
            
            #when the while end
            log.debug('testPhotoStrategy success!')
            return True
        except Exception,e:
            log.error('error:%s',e)
            log.debug('Test Strategy start fail')
            return False
    
    def testDeleteDevice(self):
        try:
            log.debug("test delete device")
            deviceId = Config(CameraConfig).getFromConfigs(deleteDevice, "device-id")
            result = self.client.deleteDevice(deviceId)
            log.debug("remove device=" + deviceId + ",result=" + (str)(result))            
            if result == False:
                log.debug('delete device fail')
            else:
                log.debug("delete device success")
            return result
        except Exception,e:
            log.error("delete device exception=%s", e)
            raise Exception("delete device exception")
         
    def testUpdateDevice(self):
        try:
            log.debug("test update device")
            deviceDetails = self.getDeviceDetails(updateDevice,False)
            result = self.client.updateDevice(deviceDetails)
            log.debug("update device=%s,result=%s", deviceDetails, result)
            if result:
                log.debug('update device success')
#                 raise Exception("update device fail")
            else:
                log.debug("update device failed")
            return result
        except Exception,e:
            log.error("update exception, %s", e)
            raise Exception("update device fail")
    
    

    def getDeviceDetails(self, manipulate,isadd):
        configuration = Config(CameraConfig)
        config = configuration.getConfig()
        if isadd==False:
            deviceId = config.get(updateDevice,'device-id')
        else:
            deviceId = config.get(globalParameter,'device-id')
        
        name = config.get(manipulate,'name')
        key = config.get(globalParameter,'key')
        host = config.get(manipulate,'host')
        port = config.get(manipulate,'port')
        login = config.get(manipulate,'login')
        password = config.get(manipulate,'password')
        address = config.get(manipulate,'address')
        lat = config.get(manipulate,'lat')
        lng = config.get(manipulate,'lng')
        accountId = config.get(globalParameter,'account-id')
        modelId = config.get(manipulate,'model-id')
        statusId = None
        functionalityId = None
        alertFlag = None
        alive = None
        currentPositionId = None
        action = None
        eventSettings = None
        deviceServerUrls = config.get(globalParameter,'device-server-urls')
        liveview = None
        snapshotRecordingEnabled = config.get(globalParameter,'snapshot-recording-enabled')
        snapshotRecordingInterval = config.get(globalParameter,'snapshot-recording-interval')
        cloudRecordingEnabled = config.get(globalParameter,'cloud-recording-enabled')
        device = DeviceDetails(deviceId, name, key, host, port, login, 
                            password, address, lat, lng, accountId,
                            modelId, statusId , functionalityId , alertFlag ,
                            alive , currentPositionId , action , eventSettings ,
                                deviceServerUrls, liveview , snapshotRecordingEnabled, 
                                snapshotRecordingInterval, cloudRecordingEnabled)
        return device
    
    
    #here are some auxiliary methods
#     def getDeviceDetailss(self, manipulate,ishost):
#         configuration = Config()
#         config = configuration.getConfig()
#         if manipulate == onlineDevice:
#             deviceId = config.get(onlineDevice,'device-id')
#             name = config.get(onlineDevice,'name')
#             key = config.get(onlineDevice,'key')
#             host = config.get(onlineDevice,'host')
#             port = config.get(onlineDevice,'port')
#             login = config.get(onlineDevice,'login')
#             password = config.get(onlineDevice,'password')
#             address = config.get(onlineDevice,'address')
#             lat = config.get(onlineDevice,'lat')
#             lng = config.get(onlineDevice,'lng')
#             accountId = config.get(onlineDevice,'account-id')
#             modelId = config.get(onlineDevice,'model-id')
#             statusId = None
#             functionalityId = None
#             alertFlag = None
#             alive = None
#             currentPositionId = None
#             action = None
#             eventSettings = None
#             deviceServerUrls = config.get(onlineDevice,'device-server-urls')
#             liveview = None
#             snapshotRecordingEnabled = config.get(onlineDevice,'snapshot-recording-enabled')
#             snapshotRecordingInterval = config.get(onlineDevice,'snapshot-recording-interval')
#             cloudRecordingEnabled = config.get(onlineDevice,'cloud-recording-enabled')
#             device = DeviceDetails(deviceId, name, key, host, port, login, 
#                                password, address, lat, lng, accountId,
#                                modelId, statusId , functionalityId , alertFlag ,
#                                 alive , currentPositionId , action , eventSettings ,
#                                  deviceServerUrls, liveview , snapshotRecordingEnabled, 
#                                  snapshotRecordingInterval, cloudRecordingEnabled)
#             return device
#         elif manipulate == updateDevice:
#             deviceId = config.get(updateDevice,'device-id')
#             if ishost==True:
#                 host = config.get(updateDevice,'host')
#             else:
#                 host = config.get(onlineDevice,'host')
#             name = config.get(onlineDevice,'name')
#             key = config.get(onlineDevice,'key')
#             port = config.get(onlineDevice,'port')
#             login = config.get(onlineDevice,'login')
#             password = config.get(onlineDevice,'password')
#             address = config.get(onlineDevice,'address')
#             lat = config.get(onlineDevice,'lat')
#             lng = config.get(onlineDevice,'lng')
#             accountId = config.get(onlineDevice,'account-id')
#             modelId = config.get(onlineDevice,'model-id')
#             statusId = None
#             functionalityId = None
#             alertFlag = None
#             alive = None
#             currentPositionId = None
#             action = None
#             eventSettings = None
#             deviceServerUrls = config.get(onlineDevice,'device-server-urls')
#             liveview = None
#             snapshotRecordingEnabled = config.get(onlineDevice,'snapshot-recording-enabled')
#             snapshotRecordingInterval = config.get(onlineDevice,'snapshot-recording-interval')
#             cloudRecordingEnabled = config.get(onlineDevice,'cloud-recording-enabled')
#             device = DeviceDetails(deviceId, name, key, host, port, login, 
#                                password, address, lat, lng, accountId,
#                                modelId, statusId , functionalityId , alertFlag ,
#                                 alive , currentPositionId , action , eventSettings ,
#                                  deviceServerUrls, liveview , snapshotRecordingEnabled, 
#                                  snapshotRecordingInterval, cloudRecordingEnabled)
#             return device
#         else:
#             log.debug("no manipulate selected")
#             return
