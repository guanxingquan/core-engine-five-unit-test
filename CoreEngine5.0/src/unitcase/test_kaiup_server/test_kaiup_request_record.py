'''
Created on 2015-5-11

@author: kaisquare
'''
from factory.StreamControlServerFactory import StreamControlServerClient
class kaiupServerClient():
    
    def __init__(self):
        self.stream = StreamControlServerClient()
        
    def test_getplayback(self):
        '''
        KAIUP PLAY BACK
        '''
        self.stream.kaiup_request_playBack_video()
    