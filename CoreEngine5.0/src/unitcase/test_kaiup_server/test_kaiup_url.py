'''
Created on 2015-5-11

@author: kaisquare
'''
from factory.StreamControlServerFactory import StreamControlServerClient
from basic.ConfigurationReader import Config
from basic.Constants import KAIUP, mediaType

class test_KAIUP_LiveView():
    
    def __init__(self):
        self.stream = StreamControlServerClient()
        
    def test1_RTSP_URL(self):
        media = Config(KAIUP).getFromConfig(mediaType, "rtsp")
        assert self.stream.kaiup_beginstream_url(media)
        
    def test2_RTMP_URL(self):
        media = Config(KAIUP).getFromConfig(mediaType, "rtsp")
        assert self.stream.kaiup_beginstream_url(media)
        
    def test3_HLS_URL(self):
        media = Config(KAIUP).getFromConfig(mediaType, "rtsp")
        assert self.stream.kaiup_beginstream_url(media)
    
    def test4_JPEG_URL(self):
        media = Config(KAIUP).getFromConfig(mediaType, "rtsp")
        assert self.stream.kaiup_beginstream_url(media)