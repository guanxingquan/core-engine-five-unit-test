'''
Created on 2015-5-8

@author: kaisquare
'''

from factory.DeviceManagementServerFactory import DeviceManagementServerClient
from factory.MysqlDataVerifierFactory import MysqlDataVerifier
from basic.Constants import CameraConfig,onlineDevice,\
    KAIUP, timeStamp, globalParameter
from time import sleep
from basic.ConfigurationReader import Config
import time
from basic import LogUtil
log = LogUtil.getLog("Node_Start_Record")
class Start():
    
    def __init__(self):
        self.deviceManage = DeviceManagementServerClient()
        self.mysqlData = MysqlDataVerifier()
        
    
    def run_Record(self):
        Config(CameraConfig).writeToConfig(globalParameter, "snapshot-recording-enabled", True)
        Config(CameraConfig).writeToConfig(globalParameter, "cloud-recording-enabled", True)
        
        self.deviceManage.tryToAddDevice(onlineDevice)
        utc_time = time.strftime("%d%m%Y%H%M%S",time.gmtime(time.time()))
        Config(KAIUP).writeToConfig(timeStamp, "start", utc_time)
        log.info("Node Record Start Time is %s(UTC)",utc_time)
        sleep(60)
        isconnected = self.mysqlData.isConnected()
        return isconnected
    
if __name__=="__main__":
#     Start().run_Record()
    print "1"
    