# -*- coding: GBK -*-
'''
 Created on 2014-7-16

@author: guanxingquan
'''

from CoreServices import ConfigControlService
from factory.DeviceManagementServerFactory import DeviceManagementServerClient
from basic.ConfigurationReader import Config
from basic import ThriftClient,LogUtil,GlobalFunction
from basic.Constants import Arbiter,configControl,deleteDevice,ServerConfig,CameraConfig,\
    streamControl
from time import sleep

log = LogUtil.getLog('testConfigControlService')
class ConfigControlServiceClient():
    client = None 
    def __init__(self):
        self.commonInter = GlobalFunction.CommonInter()
        try:
            host = Config(ServerConfig).getFromConfigs(Arbiter, "arbiter-server-host")
            port = Config(ServerConfig).getFromConfigs(Arbiter, "config-control-server-port")
            self.client = ThriftClient.getThriftClient(host, port, ConfigControlService)
            self.deviceManage = DeviceManagementServerClient()
        except Exception, e:
            log.error("ConfigControlService init error:%s",e)
            raise Exception("ConfigControlService Exception")
    
    def tearDown(self):
        ThriftClient.closeThriftClient()
    
    def setKaiUpServer(self):
        try:
            kupHost = Config(ServerConfig).getFromConfigs(configControl,"kup-arbiter-host")
            result = self.client.setCloudServer(kupHost)
            log.debug("result:%s",result)
            return result
        except Exception,e:
            log.error("Set Cloud Server found an error: %s ",e)
#             return False

    def getSetChunkSizeResult(self):
        '''
          make sure setChunkSize() is success function
        '''
        try:
            log.debug('SetChunkSize...')
            size = Config(ServerConfig).getFromConfigs(configControl,"chunk-size")
#             print size
            result = self.client.setChunkSize((int)(size))
#             print result
            if result:
                log.debug('this function set chunk-size is success!')
            else:
                log.debug('the test have error~~')
            return result
        except Exception,e:
            log.error("SetChunkSize error:%s",e)
            return False
#             raise Exception("testSetChunkSize exception")
    def getSetStreamLimitResult(self,size):
        try:
            deviceId = Config(CameraConfig).getFromConfigs(deleteDevice,"device-id")
            result = self.client.setStreamStorageLimit(deviceId,"0",size)
            log.debug('setStreamStorageLimit : %sM result : %s',size,result)
            return result
        except Exception,e:
            log.error('error : %s',e)
            return None
    
    def judgeSetLimitZero(self):
        result = self.getSetChunkSizeResult()
        if result==False:
            return None
        self.commonInter.clearStorageData()
        startsize = self.commonInter.getdirsize()
        if startsize!=0:
            return None
        self.deviceManage.startVideoRecording()
        result = self.getSetStreamLimitResult(0)
        if result==False:
#             log.info("set storage size is 0M False!")
            self.deviceManage.stopVideoRecording()
            return False
        sleep(120)
        self.deviceManage.stopVideoRecording()
        sleep(120)
        endsize = self.commonInter.getdirsize()
        log.info("Start size is %s, End size is %s",str(startsize),str(endsize))
#         print "start size is "+str(startsize)+", end size is "+str(endsize)
        if endsize < 1024:
            return True
        else:
            return False
        pass
    
#     def judgetTest(self):
#         print "\n"
#         print "start record..."
#         self.deviceManage.startVideoRecording()
#         print "set storage size 30M..."
#         self.getSetStreamLimitResult(30)
#         print "wait 30 minite..."
#         sleep(60*30)
#         print "stop record..."
#         self.deviceManage.stopVideoRecording()
        
    
    def judgeSetStorage(self):
        result = self.getSetChunkSizeResult()
        if result==False:
            return None
        self.commonInter.clearStorageData()
        startsize = self.commonInter.getdirsize()
        if startsize!=0:
            return None
        self.deviceManage.startVideoRecording()
        result = self.getSetStreamLimitResult(30)
        #startsize = self.getdirsize()
        if result==False:
            self.deviceManage.stopVideoRecording()
#             print "set storage Filed!"
            return False
        print "Wait 5 minite"
        sleep(300)
        log.info("When stop record ,the storage size: %s" ,str(self.commonInter.getdirsize()))
        self.deviceManage.stopVideoRecording()
        sleep(61)
        size = self.commonInter.getdirsize()
        log.info("[First]Message Storage Size is %s",size)
#         print "[First]Message Storage Size is "+str(size)
        if size > 1024*1024*30:
            log.info("[First]Judge set storage function failed")
            return False
        else:
            log.info("[First]Set storage size function successful.")
            self.deviceManage.startVideoRecording()
            result = self.getSetStreamLimitResult(102400)
            if result == False:
                self.deviceManage.stopVideoRecording()
                log.info("[Second]Set storage Second Failed")
                return False
            sleep(300)
            self.deviceManage.stopVideoRecording()
            size = self.commonInter.getdirsize()
            log.info("[Second]Message Storage Size is %s", str(size))
            if size > 1024*1024*30:
                log.info("[Second] Judge set storage function success.")
                return True
            else:
                log.info("[Second]Judge set storage function false.")
                return False
        pass
    
    
    
#     def getdirsize(self):
#         size = 0L
# #         one_size = 0L
#         path = Config(ServerConfig).getFromConfig(storagePath, "path")
# #         print path
#         for root,dirs,files in os.walk(path):
# #             print sum([getsize(join(root, name)) for name in files])
#             size += sum([getsize(join(root, name)) for name in files])
# #         print "Size :%s" , size
#         print "Get Director Size(byt) : "
#         print size
#         return size
#     
#     def clearStorageData(self):
#         path = Config(ServerConfig).getFromConfig(storagePath, "path")
#         cmd = "sudo rm -rf %s*" % path
#         print cmd
#         commands.getoutput(cmd)


        
    def setVideoStorageKeepDays(self):
        deviceId = Config(CameraConfig).getFromConfigs(deleteDevice,"device-id")
        channelId = Config(ServerConfig).getFromConfig(streamControl, "channel-id")
        keepDays = Config(ServerConfig).getFromConfig(configControl, "keep-days")
        try:
            result = self.client.setStorageKeepDays(deviceId,channelId,int(keepDays))
            log.info("Set Storage keep %s day result: %s.",keepDays,result)
            return result
        except Exception,e:
            log.exception("%s",e)

    def setAvailSpace(self):
        reservedSpace = Config(ServerConfig).getFromConfig(configControl, "reservedSpace")
        try:
            result = self.client.setReservedSpace(int(reservedSpace))
            log.info("Set Reserved Space %s is %s.",reservedSpace,result)
            return result
        except Exception,e:
            log.exception("%s",e)
        
        
        