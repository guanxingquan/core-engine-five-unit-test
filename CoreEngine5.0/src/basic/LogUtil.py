# -*- coding: GBK -*-
'''
Created on 2014-6-23

@author: Administrator
'''
import logging
import os

logging.basicConfig(level=logging.DEBUG,
                format='[%(asctime)s] %(filename)s(%(funcName)s:%(lineno)d)[%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                #filename='python-unittest.log',
                filemode='w')

#################################################################################################
#Console output configuration
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# forma = logging.Formatter('[%(asctime)s] %(message)s')
# console.setFormatter(forma)
# logging.getLogger('').addHandler(console)
#################################################################################################


formatter = logging.Formatter('[%(asctime)s] %(filename)s(%(funcName)s:%(lineno)d)[%(levelname)s] %(message)s')
logPath=".." + os.path.sep + ".." + os.path.sep + "scripts" + os.path.sep + "log" + os.path.sep
logPaths = "/home/node/importDemo/scripts/log"
#################################################################################################
#DEBUG and the above level output
debug = logging.FileHandler(logPath + "core-test-debug.log","w")
debug.setLevel(logging.DEBUG)
debug.setFormatter(formatter)
logging.getLogger('').addHandler(debug)
#################################################################################################
forma = logging.Formatter('[%(asctime)s]   %(message)s')
#################################################################################################
#INFO and the above level output
info = logging.FileHandler(logPath + "core-test-info.log","w")
#Will only print INFO and the above level log, such as ERROR log. Will not print DEBUG log.
info.setLevel(logging.INFO)
info.setFormatter(forma)
logging.getLogger('').addHandler(info)
#################################################################################################


def getLog(logger):
    return logging.getLogger(logger)

def debug(msg):
    logging.debug(msg)
    
def info(msg):
    logging.info(msg)
    
def error(msg):
    logging.error(msg)    

if __name__ == '__main__':
    debug("nihao")
