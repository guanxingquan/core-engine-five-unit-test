'''
Created on 2015-4-17

@author: gaunxingquan
'''
from factory.StreamControlServerFactory import StreamControlServerClient
from basic import LogUtil
# from time import sleep
log = LogUtil.getLog("TestStreamServer")

class TestStream(object):
    '''
    Test StreamServer
    '''

    def __init__(self):
        '''
        Init server
        '''
        self.streamControl = StreamControlServerClient()

    
    def test1_keepSession(self):
        '''
        Keep Session
        '''
        log.info("Test keepsession function start...")
        result = self.streamControl.keepSession()
        if result==None:
            print "URL Exception."
            return False
        assert result
        log.info("Test keepsession function end...")
        pass
    
    def test2_endSession(self):
        '''
        End Session
        '''
        log.info("Test endsession function start...")
        result = self.streamControl.endSession()
        if result==None:
            print "URL Wrong"
            return False
        assert result
        log.info("Test endsession function end...")
        pass
     
 
    def test3_activeStream(self):
        '''
        Active Stream List
        '''
        print "Test ActiveStreamList..."
        self.streamControl.Judge_getActiveStream()
        print "Test End"
         
         
    def test4_recordList(self):
        '''
        Recording List
        '''
        print "Test getRecordingList"
        self.streamControl.Judge_getRecordVideo()
        print "Test End"
     
     
    def test5_getStorageStatus(self):
        '''
        Storage Status
        '''
        print "put out the Storage Status: "
        self.streamControl.tryToGetStorageStatus()
        print "\n"
         
     
        