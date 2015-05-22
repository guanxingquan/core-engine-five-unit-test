'''
Created on 2015-5-11

@author: kaisquare
'''

from factory.StreamControlServerFactory import KaiUpClient

class test_Kai_Stop():
    
    def __init__(self):
        self.stream = KaiUpClient()
        pass
    
    def test_kaiup_stopped(self):
        assert self.stream.kaiup_stopped_request()
        
