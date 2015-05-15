'''
Created on 2015-4-21

@author: kaisquare
'''

from factory.ConfigControlServiceFactory import ConfigControlServiceClient
from basic import LogUtil,GlobalFunction

log = LogUtil.getLog("TestConfig")

class TestConfigControl(object):
    '''
    Test ConfigControlServer Function
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.configControl = ConfigControlServiceClient()
        self.commonInter = GlobalFunction.CommonInter()
        log.info("Init Config Control Server...")
        
    def test1_setKAIUP(self):
        '''
        Set KAIUP Server
        '''
        result = self.configControl.setKaiUpServer()
        assert result
        
    def test2_setChunkSize(self):
        '''
        Set Chunk Size 
        '''
        log.info("Set Chunk Size...")
        result = self.configControl.getSetChunkSizeResult()
        assert result
    
    def test3_setKeepDays(self):
        '''
        Set Keep Days
        '''
        log.info("Set Keep Days...")
        result = self.configControl.setVideoStorageKeepDays()
        assert result
    
    def test4_setAvailSpace(self):
        '''
        Set Avail Space
        '''
        log.info("Set Avail Space...")
        result = self.configControl.setAvailSpace()
        assert result
        