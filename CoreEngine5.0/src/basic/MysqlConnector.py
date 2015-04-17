'''
Created on 2014-6-19

@author: Administrator
'''
import MySQLdb
from basic.ConfigurationReader import Config
from Constants import Arbiter,ServerConfig
import logging

log = logging.getLogger("MysqlConnector")
def getConnection():
    global conn
    mhost = Config(ServerConfig).getFromConfigs(Arbiter, "mysql-host")
    mport = Config(ServerConfig).getFromConfigs(Arbiter, "mysql-port")
    muser = Config(ServerConfig).getFromConfigs(Arbiter, "mysql-user")
    mpasswd = Config(ServerConfig).getFromConfigs(Arbiter, "mysql-pwd")
    mdb = Config(ServerConfig).getFromConfigs(Arbiter, "mysql-database")
    log.debug("connect to MySQL at"+ mhost + mport + muser + mpasswd + mdb)
    conn= MySQLdb.connect(
                          host=mhost,
                          port=3306,
                          user=muser,
                          passwd=mpasswd,
                          db=mdb)
#     log.debug("connectted")
    return conn

def closeConnection():
    log.debug("close mysql connection")
    conn.close()

def test():
    con = getConnection()
    print "get client success"
    cur = con.cursor()
    sql="insert into configurations(name,value) values(%s,%s)"
    cur.execute(sql,('hadly','nihao mysql'))
    cur.close()
    con.commit()

if __name__ == '__main__':
    
    cur = getConnection().cursor()
    sql="insert into configurations(name,value) values(%s,%s)"
    cur.execute(sql,('hadly','nihao mysql'))
    
#     cur.close()
#     closeConnection()
    
    
    
    
    
