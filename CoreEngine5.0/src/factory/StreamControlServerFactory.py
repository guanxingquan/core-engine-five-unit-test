# -*- coding: GBK -*-
'''
Created on 2014-6-18

@author: lizhinian
'''
from factory.DeviceManagementServerFactory import DeviceManagementServerClient
from factory.ConfigControlServiceFactory import ConfigControlServiceClient
from factory.MysqlDataVerifierFactory import MysqlDataVerifier
from CoreServices import StreamControlService
from basic.ConfigurationReader import Config
from basic import ThriftClient,LogUtil
from basic.Constants import Arbiter,deleteDevice,CameraConfig,ServerConfig,\
    streamControl, B_E_Time,videoType, KAIUP, mediaType, timeStamp, parameter,\
    Action
from uuid import uuid1
import time
from time import sleep
from basic.GlobalFunction import CommonInter


log = LogUtil.getLog("TestStreamControlServer")
class StreamControlServerClient():
    client = None 
    
    def __init__(self):
        host = Config(ServerConfig).getFromConfigs(Arbiter, "arbiter-server-host")
        port = Config(ServerConfig).getFromConfigs(Arbiter, "stream-control-server-port")
        try:
            self.client = ThriftClient.getThriftClient(host, port, StreamControlService)
        except Exception, e:
            log.error("StreamControlServer setup Error:%s",e)
            raise Exception("StreamControlServer setup error")
        self.commonInter = CommonInter()
    
    def tearDown(self):
        ThriftClient.closeThriftClient()
    
    def getDevicetUrl(self,types):
        
        log.debug("start to get %s URL test.",types)
        sessionId = str(uuid1())
        deviceId = Config(CameraConfig).getFromConfigs(deleteDevice, "device-id")
        ttl = Config(ServerConfig).getFromConfigs(streamControl, "ttl")
        urls = self.beginstream(sessionId,ttl,None,None,types)
        if len(urls)!=0:
            log.debug("type:%s,deviceId=%s,url=%s",types,deviceId,urls[0])
            value = self.commonInter.checkUrlISBools(urls[0],types,True)
            return value
        else:
            log.debug('msg: The Get Url is NULL,deviceID is %s',deviceId)
            log.info("BeginSession get Empty URL.")
            return False
    
         
    def beginstream(self,sessionId,ttl,beginTime,endTime,types):
        channelId = Config(ServerConfig).getFromConfigs(streamControl, "channel-id")
        deviceId = Config(CameraConfig).getFromConfigs(deleteDevice, "device-id")
        try:
            urls = self.client.beginStreamSession(sessionId, long(ttl), types,None,deviceId, channelId, beginTime, endTime)
            log.debug('\n Function beginstream: url list=%s \n Args is : %s , %s , %s, %s , %s , %s,%s,%s', urls,sessionId, ttl, types,None,deviceId, channelId, beginTime, endTime)
#             print '\n Function beginstream: url list=%s' , urls
            return urls
        except Exception,e:
            log.error('Error:%s',e)
            raise Exception('beginstream exception!')

    def keepSession(self):
        sessionId = str(uuid1())
        log.info("Keep Session is %s",sessionId)
#         print "Keep Session is " , sessionId
        types = Config(ServerConfig).getFromConfigs(videoType, "rtsp")
        ttl = Config(ServerConfig).getFromConfigs(streamControl, "ttl")
        urls = self.beginstream(sessionId,ttl, None, None, types)
        if len(urls) > 0 and self.commonInter.checkUrlISBools(url=urls[0],bools=True): 
            time.sleep(int(ttl)-30)
            try:            
                self.client.keepStreamSessionAlive(sessionId,120,None)
            except Exception,e:
                log.error('As a client to keepstreamsession:[%s] found Error:%s',sessionId,e)
                return None
            time.sleep(50)
            if self.commonInter.checkUrlISBools(url=urls[0],bools=True):
                sleep(100)
                if self.commonInter.checkUrlISBools(url=urls[0],bools=False):
                    log.debug("Keep Session Alive success.")
                    return True
                else:
                    log.debug("Keep Session Alive failed.")
                    return False
            else:
                log.debug("Keep Session Alive failed.")
                return False
        else:
            log.error("Keep Session Error:url false : %s",urls)
            return None

        
            
    def endSession(self):
       
        sessionId = str(uuid1())
        types = Config(ServerConfig).getFromConfigs(videoType, "rtsp")
        ttl = Config(ServerConfig).getFromConfigs(streamControl, "ttl")
        urls = self.beginstream(sessionId,ttl, None, None, types)
        if len(urls) > 0 and self.commonInter.checkUrlISBools(urls[0], True):
            try:    
                self.client.endStreamSession(sessionId)
            except Exception,e:
                log.error('As a Client to end SessionID:[%s] found Error:%s',sessionId,e)
                return None
            time.sleep(20)
            if self.commonInter.checkUrlISBools(urls[0], False):
                log.debug("Try to end sessionID:[%s] Success.",sessionId)
                return True
            else:
                log.debug("Try to end sessionID:[%s] Failed.",sessionId)
        else:
            log.error("End Session Error:url false : %s",urls)
            return None

    
    def Judge_getActiveStream(self):
#         sessionId = str(uuid1())
        beginTime = None
        endTime = None
        types = Config(ServerConfig).getFromConfigs(videoType, "rtsp")
        ttl = Config(ServerConfig).getFromConfigs(streamControl, "ttl")
        urlList = self.beginstream(str(uuid1()), ttl,beginTime, endTime, types)
        if len(urlList) > 0 and self.commonInter.checkUrlISBools(urlList[0], False): 
            log.debug("Firstly try to begin stream get url failed.")
            return None
        sleep(int(ttl)/2 - 40)
        urlList = self.beginstream(str(uuid1()), ttl, beginTime, endTime, types)
        if len(urlList) > 0 and self.commonInter.checkUrlISBools(urlList[0], False): 
            log.debug("Secound try to begin stream get url failed.")
            return None
        log.debug("Now there should have 2 activeClient record,is:")
        print "Now there should have 2 activeClient record,is:"
        ActiveStreamList_first = self.client.getActiveOutboundStreamList()
        for stream in ActiveStreamList_first:
            log.debug("Active Stream: %s ",stream)
            print "Active Stream: ",stream
        log.debug("     *****First client end*****    ")
        log.debug("wait %ss to let early record Failure",str(int(ttl) - int(ttl)/2 + 20))
        sleep(int(ttl) - int(ttl)/2 + 20)
        
        log.debug("Now there should have 1 active record,is:")
        print "Now there should have 1 active record,is:"
        ActiveStreamList_second = self.client.getActiveOutboundStreamList()
        for stream in ActiveStreamList_second:
            log.debug("Active Stream: %s",stream)
            print "Active Stream:",stream
    
    
    
    def Judge_getRecordVideo(self):
        assert ConfigControlServiceClient().getSetChunkSizeResult()
        self.commonInter.clearStorageData()
        
        DeviceManagementServerClient().runVideoStrategy()
        sleep(3)
        deviceId = Config(CameraConfig).getFromConfig(deleteDevice, "device-id")
        channelId = Config(ServerConfig).getFromConfig(streamControl,"channel-id")
        froms = Config(ServerConfig).getFromConfig(B_E_Time,"begin-utc")
        to = Config(ServerConfig).getFromConfig(B_E_Time,"end-utc")
        startTimestamp = time.strftime("%d%m%Y%H%M%S",time.gmtime(float(froms)))
        endTimestamp = time.strftime("%d%m%Y%H%M%S",time.gmtime(float(to)))
        log.debug("The theoretical results from %s to %s :",startTimestamp,endTimestamp)
        print "The theoretical results from ",startTimestamp," to ",endTimestamp,":"
        try:
            recordVideo = self.client.getRecordedVideoList(deviceId, channelId, startTimestamp, endTimestamp)
            log.info("recordVideo:%s",recordVideo)
            for video in recordVideo:
                print "  ",video
        except Exception,e:
            log.exception("%s",e)
        log.debug("Actual results:")
        print "Actual results:"
        for key in self.commonInter.analysisXML():
            print "KEY:",key.tag,"START:",key.get('start'),"DUR:",key.get('dur'),"FPS:",key.get('fps')
            log.info("key: %s,start: %s,dur: %s,fps:%s",key.tag,key.get('start'),key.get('dur'),key.get('fps'))
            
    
    def tryToGetStorageStatus(self):
        try:
            storageInfo = self.client.getStorageStatus()
            log.info("Storage Status lIST: %s",storageInfo)
            for storage in storageInfo:
                log.info("Storage Status: %s",storage)
        except Exception,e:
            log.debug("%s",e)

    def node_request_playBack(self):
        ''''''
        pass
    
    def getparame(self):
        '''
        Get KAIUP PLAYBACK Parameter : deviceId and channelId
        '''
        sessionId = str(uuid1())
        Config(KAIUP).writeToConfig(parameter, "sessionId", sessionId)
        (deviceId,channelId) = MysqlDataVerifier().getMap()
        Config(KAIUP).writeToConfig(parameter, "kaiup-device-id", deviceId)
        Config(KAIUP).writeToConfig(parameter, "kaiup-channel-id", channelId)
        startTimestamp = Config(KAIUP).getFromConfig(timeStamp, "start")
        endTimestamp = Config(KAIUP).getFromConfig(timeStamp, "end")
        return (sessionId,deviceId,channelId,startTimestamp,endTimestamp)
    
    def getKUPBeginStreamParame(self):
        '''
        Get KAIUP LIVEVIEW Parameter: ttl ,deviceId ,channelId
        '''
        sessionId = str(uuid1())
        ttl = Config(KAIUP).getFromConfig(parameter, "ttl")
        #Config(KAIUP).writeToConfig(parameter, "sessionId", sessionId)
        (deviceId,channelId) = MysqlDataVerifier().getMap()
        startTimestamp = None
        endTimestamp = None
        log.debug("%s %s %s %s %s %s",sessionId,ttl,deviceId,channelId,startTimestamp,endTimestamp)
        return (sessionId,ttl,deviceId,channelId,startTimestamp,endTimestamp)
        
    
    def kaiup_beginstream_url(self,media):
        (sessionId,ttl,deviceId,channelId,startTimestamp,endTimestamp) = self.getKUPBeginStreamParame()
        try:
            log.debug(" %s %s %s %s %s %s %s",type(sessionId), type(ttl), type(media), type(deviceId), type(channelId), type(startTimestamp), type(endTimestamp))
            log.debug(" %s %s %s %s %s %s %s",sessionId, ttl, media,  deviceId, channelId, startTimestamp, endTimestamp) 
            urls = self.client.beginStreamSession(sessionId, ttl, media, None, deviceId, channelId, startTimestamp, endTimestamp)
            if len(urls) == 0:
                log.debug("KAIUP Begin Stream return Null.")
                return None
            log.debug("%s",urls[0])
            return self.commonInter.checkUrlISBools(urls[0], media, True)
            pass
        except Exception,e:
            print e
        
        pass
    
    
    def kaiup_send_playback_request(self,sessionId,deviceId,channelId,startTimestamp,endTimestamp,media):
        try:
            result = self.client.requestStreamForPlayback(sessionId, deviceId, channelId, media, startTimestamp, endTimestamp)
            log.info("KAIUP request Stream get [%s]",result)    
            return result
            pass
        except Exception,e:
            log.exception(e)
            return False
    
    def kaiup_getrequestStatus(self,sessionId, deviceId, channelId, media, action, startTimestamp, endTimestamp):
        try:
            streamDetail = self.client.getRequestedStreamStatus(sessionId, deviceId, channelId, media, action, startTimestamp, endTimestamp)
            if len(streamDetail) <= 0:
                print "Client Responce None!"
                return None
            log.info("%s",streamDetail)
#             print streamDetail[0].progress
            return streamDetail[0].progress
        except Exception,e:
            log.exception(e)
            return False
        
    def kaiup_cancelRequest(self,sessionId, deviceId, channelId, media, fileTime):
        return self.client.cancelStreamForPlayback(sessionId, deviceId, channelId, media, fileTime)
    
    def kaiup_request_playBack_video(self):
        '''
        
        '''
        log.info("KAIUP request palyback video Test START...")
        media = Config(KAIUP).getFromConfig(mediaType, "video")
        (sessionId,deviceId,channelId,startTimestamp,endTimestamp) = self.getparame()
        result = self.kaiup_send_playback_request(sessionId, deviceId, channelId, startTimestamp, endTimestamp, media)
#         log.info()
        if result == False:
            return False
        action = Config(KAIUP).getFromConfig(Action, "play")
        progress = 0
        while progress < 100:
            progress = self.kaiup_getrequestStatus(sessionId, deviceId, channelId, media, action, startTimestamp, endTimestamp)
        log.info("KAIUP request palyback video Test END...")
        return True
        pass
    
    def node_request_playBack_video(self,types):
        '''
        '''
        sessionId = str(uuid1())
        beginTime = Config(KAIUP).getFromConfig(timeStamp, "start")
        endTime = Config(KAIUP).getFromConfig(timeStamp, "end")
        urls = self.beginstream(sessionId, None,beginTime, endTime, types)
        if len(urls)==0:
            log.debug("Node request playback from %s to %s get result:%s",beginTime,endTime,urls)
            return None
        for url in urls:
            self.commonInter.checkUrlISBools(url, types, True)
        
        