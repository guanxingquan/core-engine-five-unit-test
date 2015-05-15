'''
Created on 2015-4-21

@author: kaisquare
'''

from factory.DeviceManagementServerFactory import DeviceManagementServerClient
from factory.ConfigControlServiceFactory import ConfigControlServiceClient
from factory.ArbiterManagementFactory import ArbiterClient
from basic.GlobalFunction import CommonInter
from basic.ConfigurationReader import Config
from basic.Constants import ServerConfig,B_E_Time
import logging
from time import sleep
# import time

class TestStorage(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.log = logging.getLogger("TestStorage")
        self.deviceManage = DeviceManagementServerClient()
        self.configControl = ConfigControlServiceClient()
        self.arbiter = ArbiterClient()
        self.commonInter = CommonInter()
        self.log.debug("Init Server DeviceManagement: %s",self.deviceManage)
        self.log.debug("Init Server ConfigControl:%s",self.configControl)
        pass
    
    def test_VideoStorage(self):
        '''
        Test Video Storage
        '''
        self.log.info("Test video storage...")
        self.log.info("Clear storage space...")
        self.commonInter.clearStorageData()
        sleep(2)
        self.log.info("Judge space is Null...")
        size = self.commonInter.getdirsize()
        if size != 0:
            self.log.info("Init storage environment error,can't clear storage space.")
            return False
        self.log.info("Set echo video size...")
        result = self.configControl.getSetChunkSizeResult()
        if result:
            self.log.info("start video storage test...")
            self.deviceManage.runVideoStrategy()
            self.log.info("put test result:")
            for key in self.commonInter.analysisXML():
                self.log.info("key: %s,start: %s,dur: %s,fps:%s",key.tag,key.get('start'),key.get('dur'),key.get('fps'))
#                     log.info key.get("start")
        pass
    
    def test_ImageStorage(self):
        '''
        Test Image Storage
        '''
        self.log.info("Test Image Storage...")
        self.log.info("clear storage space...")
        self.commonInter.clearStorageData()
        self.log.info("Judge storage is null...")
        size = self.commonInter.getdirsize()
         
        if size==0:
            self.log.info("Start Image storage...")
            self.deviceManage.runPhotoStrategy()
            froms = Config(ServerConfig).getFromConfig(B_E_Time, "begin-utc")
            to = Config(ServerConfig).getFromConfig(B_E_Time, "end-utc")
            self.log.info("put image test result from %s to %s :",froms,to)
            self.log.info("This test Record list is:")
            for key in self.commonInter.analysisXML():
                self.log.info("KEY : %S ,Creat Time: %s",key.tag,key.get("start"))
        pass
        
#     def test_EventVideoStorage(self):
#         self.configControl.clearStorageData()
#         
#         size = self.configControl.getdirsize()
#         
#         if size == 0:
#             result = self.arbiter.sendEventToArbiter()
#             if result:
#                 for key in GlobalFunction().analysisXML():
#                     print key.tag
            