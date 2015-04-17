
from factory.MysqlDataVerifierFactory import MysqlDataVerifier

def test_deleteOnline():
    MysqlDataVerifier().cleanDeviceInfo()