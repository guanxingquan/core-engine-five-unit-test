'''
Created on 2015-4-17

@author: gaunxingquan
'''
from factory.StreamControlServerFactory import StreamControlServerClient
from basic import LogUtil
from basic.ConfigurationReader import Config
from basic.Constants import ServerConfig,videoType,imageType
# from time import sleep
log = LogUtil.getLog("TestLiveView")

class TestLiveView(object):
    '''
    Test camera live view is normal
    '''

    def __init__(self):
        '''
        Init server
        '''
        self.streamControl = StreamControlServerClient()

    
    def test1_RTSP_URL(self):
        '''
        Test RTSP/H264 URL
        '''
        TYPE = Config(ServerConfig).getFromConfig(videoType, "rtsp")
        result = self.streamControl.getDevicetUrl(TYPE)
        log.info("Message :%s   Result : %s",TYPE,result)
        assert result
        pass
    
    def test2_RTMP_URL(self):
        '''
        Test RTMP/H264 URL
        '''
        TYPE = Config(ServerConfig).getFromConfig(videoType, "rtmp")
        result = self.streamControl.getDevicetUrl(TYPE)
        log.info("Message :%s   Result : %s",TYPE,result)
        assert result
        pass
    
    def test3_MJPEG_URL(self):
        '''
        Test HTTP/MJPEG URL
        '''
        TYPE = Config(ServerConfig).getFromConfig(videoType, "mjpeg")
        result = self.streamControl.getDevicetUrl(TYPE)
        log.info("Message :%s   Result : %s",TYPE,result)
        assert result
        pass
    
    def test4_HLS_URL(self):
        '''
        Test HTTP/H264 URL
        '''
        TYPE = Config(ServerConfig).getFromConfig(videoType, "hls")
        result = self.streamControl.getDevicetUrl(TYPE)
        log.info("Message :%s   Result : %s",TYPE,result)
        assert result
        pass
    
    def test5_JPEG_URL(self):
        '''
        Test HTTP/JPEG URL(Snapshot)
        '''
        TYPE = Config(ServerConfig).getFromConfig(imageType, "jpeg")
        result = self.streamControl.getDevicetUrl(TYPE)
        log.info("Message :%s   Result : %s",TYPE,result)
        assert result
        pass