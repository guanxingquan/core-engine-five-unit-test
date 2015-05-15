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
    
    def getDeviceConnection(self,deviveId):
        sql = "select event_type from device_events where device_id = %s order by time desc limit 0,1"
        result = self.executeSql(sql,deviveId)
        return result
#     
    def kaiup_getmap(self,deviceId,deviceKey):
        sql = "select * from channel_device_map a join devices b on (a.kup_device_id = b.id) where a.node_device_id = %s and device_key=%s"
        result = self.executeSql(sql,deviceId,deviceKey)
        return result
    
    def cleanDeviceInfo(self, deviceId):
        cur =self.con.cursor()

        sq = "delete from stream_relays where device_id=%s"
        sql = "delete from stream_sessions where device_id = %s"
        sql0 = "delete from rs_device where id=%s ;"
        sql1 = "delete from device_events where device_id=%s ;"
        sql2 = "delete from ds_device where id=%s ;"
        sql3 = "delete from devices where id=%s ;"
        
        num = cur.execute(sq,deviceId)
        num = cur.execute(sql,deviceId)
        num = cur.execute(sql0,deviceId)
        num = cur.execute(sql1, deviceId)
        num = cur.execute(sql2, deviceId)
        num = cur.execute(sql3, deviceId)
        
        self.con.commit()
        result = cur.fetchall()
        return result

        