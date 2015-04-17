'''
Created on 2014-6-19

@author: Administrator
'''
import ConfigParser
import os

configPath = ".." + os.path.sep + ".." + os.path.sep + "configs" + os.path.sep

class Config():
    config = None
    def __init__(self,filename):
        #open file
        self.config = ConfigParser.ConfigParser()
        self.configFile = configPath + filename
        cfgfile = open(self.configFile,'r')
        self.config.readfp(cfgfile)

    def getConfig(self):
        return self.config
    
    def getFromConfig(self, section, key):
        return self.config.get(section, key)
        
    def getFromConfigs(self, section, key):
        return self.config.get(section, key)
    
    def writeToConfig(self, section, key, value):
        self.config.set(section, key, value)
        self.config.write(open(self.configFile,'w'))
