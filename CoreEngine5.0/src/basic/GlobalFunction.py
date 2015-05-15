'''
Created on 2015-4-27

@author: guanxingquan
'''
from xml.etree import ElementTree as ET
from basic.ConfigurationReader import Config
from basic.Constants import ServerConfig,storagePath,B_E_Time
import os
import commands
from os.path import getsize, join
from basic import LogUtil
# import time
log = LogUtil.getLog("AnalusisXMLS")
class CommonInter(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.path = Config(ServerConfig).getFromConfig(storagePath, "path")
        pass
    
    def analysisXML(self):
        keyList = []
        start = Config(ServerConfig).getFromConfig(B_E_Time, "begin-utc").split('.')[0]
        end = Config(ServerConfig).getFromConfig(B_E_Time, "end-utc").split('.')[0]
        for xmlfile in self.xmlList():
            par = ET.parse(xmlfile)
            for channel in par.getiterator('ch-0'):
                for key in  channel.getchildren():
                    if key.get('start') >= start and key.get("start") < end:
                        keyList.append(key)
        return keyList
    
    def xmlList(self):
        xmlList = [] 
        for root,dirs,files in os.walk(self.path):
            for name in files:
                if name == "storage.xml":
                    xmlList.append(os.path.join(root,name))
                    pass
#         print xmlList
        return xmlList
        pass
    
    def getdirsize(self):
        size = 0L
#         one_size = 0L
#         print path
        for root,dirs,files in os.walk(self.path):
#             print sum([getsize(join(root, name)) for name in files])
            size += sum([getsize(join(root, name)) for name in files])
#         print "Size :%s" , size
        log.info("Get Director Size(byt) : %s",size)
#         print "Get Director Size(byt) : ",size
        return size
    
    def clearStorageData(self):
        log.info("Remove start , the storage size is %s",self.getdirsize())
        cmd = "sudo rm -rf %s*" % self.path
#         print cmd
        log.info(cmd)
        commands.getoutput(cmd)
    
    def judgeURL(self,url,types):
        log.debug("message: url:%s || type:%s",url,types)
        MJPEG = "http/mjpeg"
        JPEG = "http/jpeg"
        RTMP = "rtmp/h264"
        if types==MJPEG:
            cmd = ("(ffmpeg -f mjpeg -i %s -y test.mp4 > out.log 2>&1 &);sleep 30;ls -l test.* | awk '{print $5}'" % url)
        elif types==JPEG:
            cmd = ("(ffmpeg -f mjpeg -i %s -y test.jpg > out.log 2>&1 &);sleep 20;ls -l test.* | awk '{print $5}'" % url)
        elif types==RTMP:
            cmd = ("(./rtmpdump -o test.mp4 -r %s -v > out.log 2>&1 &);sleep 30;ls -l test.* | awk '{print $5}'" % url)
            pass
        else:
            cmd = ("(ffmpeg -i %s -vcodec copy -acodec copy -an -f mp4 -y test.mp4 > out.log 2>&1 &);sleep 20;ls -l test.* | awk '{print $5}'" % url)
        (status,output) = commands.getstatusoutput(cmd)
        log.debug("Debug: status is %s , output is %s",status,output)
        booleans = status==0 and output!=''
        log.debug("boolean: %s ",booleans)
        if status!=0 and output=='':
            log.error("Command error:[%s].",cmd)
            return None
        else:
            if "No such file or directory"  in output:
                log.debug("URL[%s] is false,No video produce,Output information:%s",url,output)
                self.clearFFmpegdata()
                return False
                pass
            else:
#                 sec_size = commands.getoutput("sleep 3;ls -l test.mp4 | awk '{print $5}'")
                log.debug("URL[%s] is true,Have %s size mp4 file produce",url,output)
                self.clearFFmpegdata()
                return True
#         return False  ;sleep 20;ls -l test.mp4 | awk '{print $5}'
        pass
    
    
    def clearFFmpegdata(self):
        cmd1 = "rm -f test.* out.log"
        cmd2 = "(ps -ef | grep ffmpeg | awk '{print $2}' | xargs kill -9)"
        try:
            commands.getstatusoutput(cmd1)
            commands.getstatusoutput(cmd2)
        except Exception,e:
            log.exception("exception:%s",e)
        
    def checkUrlISBools(self,url,types,bools):
        if bools == self.judgeURL(url,types):
            return True
        return False



