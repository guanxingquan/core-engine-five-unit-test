'''
Created on 2014-6-20

@author: Administrator
'''
from Constants import deviceName
from basic import MysqlConnector
from basic.ConfigurationReader import Config
from basic.Constants import CameraConfig

class Mysql(object):
    
    con = None
    def __init__(self):
        '''
        Constructor
        '''
        self.con = MysqlConnector.getConnection()
    
    def executeSql(self, sql, *params):
        cur =self.con.cursor()
        num = cur.execute(sql,params)
        self.con.commit()
        result = cur.fetchall()
        return result
    
    def getModel(self):
        sql = "select id,name from device_models"
        result = self.executeSql(sql)
        return result
    
    def getDevicesList(self):
        sql = "select * from devices"
        result = self.executeSql(sql)
        return result
        pass
    
    def getAskDevicesList(self,models):
        sql = "select * from devices where "
        result = self.executeSql(sql)
        return result
       
    def getDeviceByName(self):
        sql = "select * from devices where name=%s ;"
        addedDeviceName = Config(CameraConfig).getFromConfig(deviceName, "addedDeviceName")
        result = self.executeSql(sql, addedDeviceName)
        return result
    
    def getDeviceById(self,Id):
        sql = "select * from devices where id=%s ;"
        result = self.executeSql(sql, Id)
        return result
    
    def getDsDeviceById(self, deviceId):
        sql = "select * from ds_device where id=%s ;"
        result = self.executeSql(sql, deviceId)
        return result
    def getDeviceConnection(self):
        sql = "select * from device_events where device_id = %s"
#     def getDsServerInfo(self,deviceId):
#         sql = "select * from ds_server_info where id=(select server_id from ds_device_info where id=%s) ;"
#         result = self.executeSql(sql,deviceId)
#         return result
#     
#     def getRsServerInfo(self,deviceId):
#         sql = "select * from rs_server_info where id=(select server_id from rs_device_info where id=%s) ;"
#         result = self.executeSql(sql,deviceId)
#         return result

#     def getStreamSessionInfoBySessionId(self,sessionId):
#         sql = "select * from stream_session_info where id=%s"
#         result = self.executeSql(sql,sessionId)
#         return result
#         pass
#     
    def cleanDeviceInfo(self, deviceId):
        cur =self.con.cursor()
        sql = "delete from rs_device where id=%s ;"
        sql1 = "delete from device_events where device_id=%s ;"
        sql2 = "delete from ds_device where id=%s ;"
        sql3 = "delete from devices where id=%s ;"
         
        num = cur.execute(sql,deviceId)
        num = cur.execute(sql1, deviceId)
        num = cur.execute(sql2, deviceId)
        num = cur.execute(sql3, deviceId)
        self.con.commit()
        result = cur.fetchall()
        return result
#             
#     def getChannelDeviceMap(self):
#         sql = "select * from channel_device_map;"
#         result = self.executeSql(sql)
#         return result
#         
#     def getStreamSessionInfo(self, deviceId):
#         sql = "select * from stream_session_info where device_id=%s ;"
#         result = self.executeSql(sql, deviceId)
#         return result
#         
#     def getConfigurationsInfo(self,name,value):
#         sql = "select * from configurations where name=%s and value=%s ;"
#         result = self.executeSql(sql,name,value)
#         return result
#         
        