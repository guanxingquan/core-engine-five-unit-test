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
from basic import ThriftClient,LogUtil
from basic.Constants import Arbiter,globalParameter,deviceName, KAIUP, parameter
from basic.Constants import onlineDevice,updateDevice,deleteDevice
from basic.Constants import configControl,B_E_Time
from basic.Constants import CameraConfig,ServerConfig
import time
from basic.MysqlOperator import Mysql
from time import sleep

log = LogUtil.getLog("TestDeviceManagementServer")
class DeviceManagementServerClient():
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
        log.debug("Model List:%s",modelLists)
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
                Config(KAIUP).writeToConfig(parameter, "node-device-id", result)
                return True
            else:
                log.debug('add device to Arbiter fail')
                return False
        except Exception,e:
            log.error('Error:%s',e)
    
    def startVideoRecording(self):
        '''
           start video
        '''
        Config(CameraConfig).writeToConfig(globalParameter, "cloud-recording-enabled","true")
        deviceDetail = self.getDeviceDetails(onlineDevice,False)
        result = self.client.updateDevice(deviceDetail)
        log.debug("Begin video recording, result : %s",result)
        if result:
            sleep(30)
        return result
    
    def stopVideoRecording(self):
        Config(CameraConfig).writeToConfig(globalParameter, "cloud-recording-enabled","false")
        deviceDetail = self.getDeviceDetails(onlineDevice,False)
        result = self.client.updateDevice(deviceDetail)
        log.debug("Stop video recording, result : %s",result)
#         if result:
#             sleep(40)
        return result
    
    
    def runVideoStrategy(self):
        
        log.debug('Run Video Strategy...')
        chunk_size = Config(ServerConfig).getFromConfigs(configControl,"chunk-size")
        
        self.startVideoRecording()
        
        istrue = True
        v_sum = 0
        while istrue:
            current_time = time.time()
            minutes = time.strftime("%M",time.localtime(current_time))
            seconds = time.strftime('%S',time.localtime(current_time))
            booleans = int(minutes)%(int)(chunk_size)==0 and seconds=="00"
#             print booleans
            if booleans:
                log.debug('The %s cycle starting',v_sum+1)
                if v_sum == 0:
                    Config(ServerConfig).writeToConfig(B_E_Time, "begin-utc",current_time)
#                 if v_sum > 0:
#                     self.startVideoRecording()
                    
                log.debug('Next will sleep %ss~',eval(chunk_size)*60*2)
                
                v_sum = v_sum + 1
                
                time.sleep(eval(chunk_size)*60*2)
                
                self.stopVideoRecording()
                
                if v_sum == 2:
                    
                    Config(ServerConfig).writeToConfig(B_E_Time, "end-utc",time.time())
#                     self.stopVideoRecording()
                    istrue = False
                if v_sum == 1:
                    time.sleep(eval(chunk_size)*30)
                    self.startVideoRecording()
                    
                log.debug('The %s cycle ended',v_sum)
        
        #when the while end
        log.debug('Run VideoStrategy Ending!')
#         return True
        
#       return False
    
    def startImageRecording(self):
        Config(CameraConfig).writeToConfig(globalParameter, "snapshot-recording-enabled","true")
        deviceDetails = self.getDeviceDetails(onlineDevice, False)
        result = self.client.updateDevice(deviceDetails)
        log.debug("Begin Image recording, result : %s",result)
        if result:
            sleep(40)
        return result
    
    def stopImageRecording(self):
        Config(CameraConfig).writeToConfig(globalParameter, "snapshot-recording-enabled","false")
        deviceDetails = self.getDeviceDetails(onlineDevice, False)
        result = self.client.updateDevice(deviceDetails)
        log.debug("Stop Image recording, result : %s",result)
#         if result:
#             sleep(40)
        return result
    
    def runPhotoStrategy(self):
        
        log.debug('Run Image Strategy...')
        interval = Config(CameraConfig).getFromConfigs(globalParameter,"snapshot-recording-interval")
        self.startImageRecording()
        
        # sleep 40 seconds after begin image recording, waiting DS to register the device
        istrue = True
        p_sum = 0
        while istrue:
            current_time = time.time()
            seconds = time.strftime('%S',time.localtime(current_time))
            if eval(str(current_time))%eval(interval)==0 and eval(str(seconds))%eval(interval)==0:
                if p_sum==0:
                    Config(ServerConfig).writeToConfig(B_E_Time, "begin-utc",current_time)
                
                p_sum = p_sum + 1
                log.debug('Sleep Time: %ss',eval(interval)*12)
                time.sleep(eval(interval)*12)
                
                # stop image recording
                self.stopImageRecording()
                
                if p_sum==1:
                    log.debug('Sleep Time: %ss',eval(interval)*12)
                    time.sleep(eval(interval)*12)
                    log.debug('Waiting to Start Next...')
                    self.startImageRecording()
                if p_sum == 2:
                    Config(ServerConfig).writeToConfig(B_E_Time, "end-utc",time.time())
                    istrue = False
        
        #when the while end
        log.debug('Run PhotoStrategy Over!')
        return True
        
    
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
    
    def chagePort(self):
        config = Config(CameraConfig)
        rightPort = config.getFromConfig(onlineDevice, 'port')
        errorPort = config.getFromConfig(onlineDevice, 'error-port')
        config.writeToConfig(onlineDevice, 'port', errorPort)
        config.writeToConfig(onlineDevice, 'error-port', rightPort)
        deviceDetails = self.getDeviceDetails(onlineDevice,False)
        result = self.client.updateDevice(deviceDetails)
        if result:
            log.debug('update device success')
#                 raise Exception("update device fail")
        else:
            log.debug("update device failed")
            return result
        pass

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
