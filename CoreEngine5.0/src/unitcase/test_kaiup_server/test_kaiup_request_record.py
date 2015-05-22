'''
Created on 2015-5-11

@author: kaisquare
'''
from factory.StreamControlServerFactory import KaiUpClient
class test_kaiupServerClient():
    
    def __init__(self):
        self.stream = KaiUpClient()
        
    def test_getplayback_video(self):
        '''
        KAIUP PLAY BACK
        '''
        self.stream.kaiup_request_playBack_video()
    
    def test_playback_image(self):
        self.stream.kaiup_request_playBack_Image()
    
