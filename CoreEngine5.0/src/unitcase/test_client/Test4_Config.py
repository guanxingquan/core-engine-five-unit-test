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
        
    
    def test1_setStreamStorageLimitZero(self):
        '''
        Set device storage limit zero
        '''
        log.info("Set Storage Size 0M...")
#         self.commonInter.clearStorageData()
        
        result = self.configControl.judgeSetLimitZero()
        assert result
        log.info("Clear Recording Data...")
        self.commonInter.clearStorageData()
        
        
    def test2_setStorageLimitOtherSize(self):
        '''
        Set device storage limit 30M & 102400M
        '''
#         self.commonInter.clearStorageData()
        log.info("Set Storage Size 30M & 102400M...")
        result = self.configControl.judgeSetStorage()
        assert result
        log.info("Clear Recording Data...")
        self.commonInter.clearStorageData()
        
    