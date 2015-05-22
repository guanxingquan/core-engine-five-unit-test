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
    streamControl, B_E_Time,videoType, KAIUP, mediaType, timeStamp, \
    Action, imageType
from uuid import uuid1
import time
from time import sleep
from basic.GlobalFunction import CommonInter


log = LogUtil.getLog("TestStreamControlServer")

class Client():
    def __init__(self):
        self.stream = StreamControlServerClient()
        self.rtsp = None
        self.rtmp = None
        self.mjpeg = None
        self.hls = None
        self.jpeg = None
        self.role = None
        
    def RTSP_URL(self):
        return self.stream.beginstream_ROLE(self.rtsp, self.role)
    
    def RTMP_URL(self):
        return self.stream.beginstream_ROLE(self.rtmp, self.role)
    
    def HLS_URL(self):
        return self.stream.beginstream_ROLE(self.hls, self.role)
    
    def JPEG_URL(self):
        return self.stream.beginstream_ROLE(self.jpeg, self.role)
    
    def keepSession(self):
        return self.stream.keepSession(self.rtsp, self.role)
    
    def endSession(self):
        return self.stream.endSession(self.rtsp, self.role)
    
    def getActiveStream(self):
        return self.stream.Judge_getActiveStream(self.rtsp, self.role)
    
    def getStorageStatus(self):
        return self.stream.tryToGetStorageStatus()
    
    
class NodeClient(Client):
    
    def __init__(self):
        Client.__init__(self)
#         self.stream = StreamControlServerClient()
        self.rtsp = Config(ServerConfig).getFromConfig(videoType, "rtsp")
        self.rtmp = Config(ServerConfig).getFromConfig(videoType, "rtmp")
        self.mjpeg = Config(ServerConfig).getFromConfig(videoType, "mjpeg")
        self.hls = Config(ServerConfig).getFromConfig(videoType, "hls")
        self.jpeg = Config(ServerConfig).getFromConfig(imageType, "jpeg")
        self.role = "NODE"
    
    def MJPG_URL(self):
        return self.stream.beginstream_ROLE(self.mjpeg, self.role)
    
    def palyback_RTSP(self):
        return  self.stream.node_request_playBack(self.rtsp)
    
    def palyback_RTMP(self):
        return self.stream.node_request_playBack(self.rtmp)
    
    def playback_HLS(self):
        return self.stream.node_request_playBack(self.hls)
    
    def playback_JPEG(self):
        return self.stream.node_request_playBack(self.jpeg)
    
    def palyback_MJPEG(self):
        return self.stream.node_request_playBack(self.mjpeg)

    def getRecordVideoList(self):
        return self.stream.Judge_getRecordVideo()

class KaiUpClient(Client):
    
    def __init__(self):
        Client.__init__(self)
        self.rtsp = Config(KAIUP).getFromConfig(mediaType, "rtsp")
        self.rtmp = Config(KAIUP).getFromConfig(mediaType, "rtmp")
        self.hls = Config(KAIUP).getFromConfig(mediaType, "hls")
        self.jpeg = Config(KAIUP).getFromConfig(mediaType, "jpeg")
        self.video = Config(KAIUP).getFromConfig(mediaType, "video")
        self.image = Config(KAIUP).getFromConfig(mediaType, "image")
        self.role = "CLOUD"
    
    def kaiup_request_playBack_video(self):
        return self.stream.kaiup_request_playBack(self.video)
    
    def kaiup_request_playBack_Image(self):
        return self.stream.kaiup_request_playBack(self.image)
    
    def kaiup_stopped_request(self):
        return self.stream.kaiup_cancel_request(self.video)


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

    def keepSession(self,media,role):
        (sessionId, ttl,allowedClientIpAddresses,deviceId, channelId, startTimestamp, endTimestamp) = self.getLiveParame(role)
        (url,result) = self.request_beginstream_live(sessionId, ttl, media, allowedClientIpAddresses, deviceId, channelId, startTimestamp, endTimestamp)
        if result==None or result == False:
            log.debug("KEEP [%s] , when start session filed! || URL:[%s],RESULT:[%s]",sessionId,url,result)
            return False
            pass
        sleep(int(ttl)-30)
        self.client.keepStreamSessionAlive(sessionId,120,None)
        sleep(50)
        if self.commonInter.checkUrlISBools(url,media,True):
            sleep(100)
            if self.commonInter.checkUrlISBools(url,media,False):
                log.info("Keep Session Alive success.")
                return True
            else:
                log.info("Keep Session Alive failed.Maybe keep time more than 120s")
                return False
        else:
            log.info("Keep Session Alive failed.keep session no Effect!")
            return False
        
    def endSession(self,media,role):
        (sessionId, ttl,allowedClientIpAddresses,deviceId, channelId, startTimestamp, endTimestamp) = self.getLiveParame(role)
        (url,result) = self.request_beginstream_live(sessionId, ttl, media, allowedClientIpAddresses, deviceId, channelId, startTimestamp, endTimestamp)
        if result==None or result == False:
            log.debug("END [%s] , when start session filed! || URL:[%s],RESULT:[%s]",sessionId,url,result)
            return False
            pass
        self.client.endStreamSession(sessionId)
        sleep(20)
        if self.commonInter.checkUrlISBools(url,media,False):
            log.debug("Try to end sessionID:[%s] Success.",sessionId)
            return True
        else:
            log.debug("Try to end sessionID:[%s] Failed.",sessionId)
            return False
        
    
    def Judge_getActiveStream(self,media,role):
        ''''''
        ttl = Config(ServerConfig).getFromConfigs(streamControl, "ttl")
        first_begin = self.beginstream_ROLE(media, role) #20s
        if first_begin != True:
            log.info("ACTIVE Stream , when start begining first filed!")
            return False
        sleep(40)
        second_begin = self.beginstream_ROLE(media, role) #20s
        if second_begin != True:
            log.info("ACTIVE Stream , when start begining second filed!")
            return False
        
        log.debug("Now there should have 2 activeClient record,is:")
        print "Now there should have 2 activeClient record,is:"
        ActiveStreamList_first = self.client.getActiveOutboundStreamList()
        for stream in ActiveStreamList_first:
            log.debug("Active Stream: %s ",stream)
            print "Active Stream: ",stream
        log.debug("     *****First Request end*****    ")
        log.debug("wait %ss to let early record Failure",str(int(ttl)-20-40-20))
        sleep(int(ttl)-20-40-20)
        log.debug("Now there should have 1 active record,is:")
        print "Now there should have 1 active record,is:"
        ActiveStreamList_second = self.client.getActiveOutboundStreamList()
        for stream in ActiveStreamList_second:
            log.debug("Active Stream: %s",stream)
            print "Active Stream:",stream
        return True
    
    
    
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
                print storage
        except Exception,e:
            log.debug("%s",e)
        
    def getLiveParame(self,role):
        sessionId = str(uuid1())
        ttl = Config(ServerConfig).getFromConfigs(streamControl, "ttl")
        allowedClientIpAddresses = None
        if role=="NODE":
            deviceId = Config(CameraConfig).getFromConfigs(deleteDevice, "device-id")
            channelId = Config(ServerConfig).getFromConfigs(streamControl, "channel-id")
        if role=="CLOUD":
            (deviceId,channelId) = MysqlDataVerifier().getMap()
        startTimestamp = None
        endTimestamp = None
        return (sessionId, long(ttl),allowedClientIpAddresses,deviceId, channelId, startTimestamp, endTimestamp)
    
    def node_request_playBack(self,media):
        '''
        '''
        resultset = []
        (sessionId,ttl,allowedClientIpAddresses,deviceId, channelId, startTimestamp, endTimestamp) = self.get_Node_playBack_parame()
        urls = self.client.beginStreamSession(sessionId, ttl, media, allowedClientIpAddresses, deviceId, channelId, startTimestamp, endTimestamp)
        self.client.keepStreamSessionAlive(sessionId,len(urls)*30,None)
        if len(urls)==0:
            log.debug("Node request playback from %s to %s get result:%s",startTimestamp,endTimestamp,urls)
            return None
        for url in urls:
            resultset.append(self.commonInter.checkUrlISBools(url, media, True))
        print resultset
        return resultset
    
    def get_Node_playBack_parame(self):
        (sessionId,ttl,allowedClientIpAddresses,deviceId, channelId, node_startTime, node_endTime) = self.getLiveParame("NODE")
        node_startTime = Config(KAIUP).getFromConfig(timeStamp, "start")
        node_endTime = Config(KAIUP).getFromConfig(timeStamp, "end")
        log.debug("%s %s %s %s %s %s %s",sessionId, ttl, allowedClientIpAddresses, deviceId, channelId, node_startTime, node_endTime)
        return (sessionId,ttl,allowedClientIpAddresses,deviceId, channelId, node_startTime, node_endTime)
    
    
    def get_KaiUP_PlayBack_parame(self):
        '''
        Get KAIUP PLAYBACK Parameter : deviceId and channelId
        '''
        sessionId = str(uuid1())
#         Config(KAIUP).writeToConfig(parameter, "sessionId", sessionId)
        (deviceId,channelId) = MysqlDataVerifier().getMap()
#         Config(KAIUP).writeToConfig(parameter, "kaiup-device-id", deviceId)
#         Config(KAIUP).writeToConfig(parameter, "kaiup-channel-id", channelId)
        startTimestamp = Config(KAIUP).getFromConfig(timeStamp, "start")
        endTimestamp = Config(KAIUP).getFromConfig(timeStamp, "end")
        return (sessionId,deviceId,channelId,startTimestamp,endTimestamp)
    
    def beginstream_ROLE(self,media,role):
        (sessionId,ttl,allowedClientIpAddresses,deviceId,channelId,startTimestamp,endTimestamp) = self.getLiveParame(role)
        (url,result) = self.request_beginstream_live(sessionId, ttl, media, allowedClientIpAddresses, deviceId, channelId, startTimestamp, endTimestamp)
        return result
    
    def request_beginstream_live(self,sessionId, ttl, media, allowedClientIpAddresses, deviceId, channelId, startTimestamp, endTimestamp):
        urls = self.client.beginStreamSession(sessionId, ttl, media, allowedClientIpAddresses, deviceId, channelId, startTimestamp, endTimestamp)
        if len(urls) == 0:
            log.info("KAIUP Begin Stream return Null.")
            return None
        log.debug("%s",urls[0])
        return (urls[0],self.commonInter.checkUrlISBools(urls[0], media, True))
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
        streamDetails = self.client.getRequestedStreamStatus(sessionId, deviceId, channelId, media, action, startTimestamp, endTimestamp)
        return len(streamDetails),streamDetails
        
    def kaiup_getrequestStatus_By_Status(self,streamDetails,status):
        streams = [stream for stream in streamDetails if "group0" in stream.url and stream.status==status]
        if status == "ready":
            streams = [stream for stream in streamDetails if "group0" not in stream.url]
        return len(streams),streams
        
        
    def kaiup_cancelRequest(self,sessionId, deviceId, channelId, media, fileTime):
        return self.client.cancelStreamForPlayback(sessionId, deviceId, channelId, media, fileTime)
    
    
    def kaiup_request_playBack(self,media):
        '''
        '''
        log.info("KAIUP request palyback %s Test START...",media)
#         
        (sessionId,deviceId,channelId,startTimestamp,endTimestamp) = self.get_KaiUP_PlayBack_parame()
        result = self.kaiup_send_playback_request(sessionId, deviceId, channelId, startTimestamp, endTimestamp, media)
        if result == False:
            return False
        action = Config(KAIUP).getFromConfig(Action, "play")
        isOver = True
        while isOver:
            total,TotalStream = self.kaiup_getrequestStatus(sessionId, deviceId, channelId, media, action, startTimestamp, endTimestamp)
            completed,CompletedStream = self.kaiup_getrequestStatus_By_Status(TotalStream, "completed")
            ready,ReadyStream = self.kaiup_getrequestStatus_By_Status(TotalStream, "ready")
            cancel,CancelStream = self.kaiup_getrequestStatus_By_Status(TotalStream, "stopped")
            upload,UploadingStream = self.kaiup_getrequestStatus_By_Status(TotalStream, "uploading")
            log.debug("Total Stream: %s ,Already Completed: %s, Wait to Upload: %s, Cancel(Stopped): %s",total,completed,ready,cancel)
            log.debug("Uploading Stream detail: %s",UploadingStream)
            isOver = False if total==completed+cancel else True
            if isOver:
                sleep(60)
        log.info("KAIUP request palyback %s Test END...",media)
        return True
        pass

    def kaiup_cancel_request(self,media):
        log.info("KAIUP Cancel request palyback %s Test START...",media)
        (sessionId,deviceId,channelId,startTimestamp,endTimestamp) = self.get_KaiUP_PlayBack_parame()
        result = self.kaiup_send_playback_request(sessionId, deviceId, channelId, startTimestamp, endTimestamp, media)
        if result == False:
            return False
        action = Config(KAIUP).getFromConfig(Action, "play")
        
#         ready,ReadyStream = self.kaiup_getrequestStatus_By_Status(streamDetails, "ready")
        noupload = True
        UploadingStream = None
        while noupload:
            total,streamDetails = self.kaiup_getrequestStatus(sessionId, deviceId, channelId, media, action, startTimestamp, endTimestamp)
            completed,CompletedStream = self.kaiup_getrequestStatus_By_Status(streamDetails, "completed")
            upload,UploadingStream = self.kaiup_getrequestStatus_By_Status(streamDetails, "uploading")
            noupload = False if upload==1 or total==completed else True
            if noupload:
                sleep(30)
        fileTime = [stream.froms for stream in UploadingStream]
        log.debug("upload stream:%s,fileTime:%s",UploadingStream,fileTime)
        result = self.kaiup_cancelRequest(sessionId, deviceId, channelId, media, fileTime)
        log.debug("kaiup cancel request [%s, %s, %s ,%s, %s] result:%s",sessionId, deviceId, channelId, media, fileTime,result)
        sleep(5)
        total,streamDetails = self.kaiup_getrequestStatus(sessionId, deviceId, channelId, media, action, startTimestamp, endTimestamp)
#         log.debug("%s",streamDetails)
        cancel,CancelStream = self.kaiup_getrequestStatus_By_Status(streamDetails, "stopped")
        log.debug("Should have one record status is stopped : %s",CancelStream)
        if cancel==1:
            return True
        return False
        
        
        
    
        