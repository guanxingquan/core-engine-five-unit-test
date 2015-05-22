'''
Created on 2015-5-11

@author: kaisquare
'''
from factory.StreamControlServerFactory import KaiUpClient

class test_KAIUP_LiveView():
    
    def __init__(self):
        self.stream = KaiUpClient()
        
    def test1_RTSP_URL(self):
        assert self.stream.RTSP_URL()
        
    def test2_RTMP_URL(self):
        assert self.stream.RTMP_URL()
        
    def test3_HLS_URL(self):
        assert self.stream.HLS_URL()
    
    def test4_JPEG_URL(self):
        assert self.stream.JPEG_URL()