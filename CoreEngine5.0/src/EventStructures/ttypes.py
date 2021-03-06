#
# Autogenerated by Thrift Compiler (0.8.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class EventDetails:
  """
  Detailed Event Information
  (1) id - Unique identifier of this event
  (2) data - Additional details about the event; JSON formatted string.
             Format depends on event type.
             e.g. if event type is PERIMETER_BREACH, info might
             be coordinates; if event type is SPEED_LIMIT_BREACH,
             info might be the speed and location.
  (3) type - the type of event
  (4) time - the timestamp in "dd/MM/yyyy hh:mm:ss" format
  (5) deviceId - the device from which this event comes
  (6) channelId - the channel of device from which this event comes
  (7) binaryData - the binary data associated with this device (blob), e.g. a snapshot from camera that detected motion

  Attributes:
   - id
   - data
   - type
   - time
   - deviceId
   - channelId
   - binaryData
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'id', None, None, ), # 1
    (2, TType.STRING, 'data', None, None, ), # 2
    (3, TType.STRING, 'type', None, None, ), # 3
    (4, TType.STRING, 'time', None, None, ), # 4
    (5, TType.STRING, 'deviceId', None, None, ), # 5
    (6, TType.STRING, 'channelId', None, None, ), # 6
    (7, TType.STRING, 'binaryData', None, None, ), # 7
  )

  def __init__(self, id=None, data=None, type=None, time=None, deviceId=None, channelId=None, binaryData=None,):
    self.id = id
    self.data = data
    self.type = type
    self.time = time
    self.deviceId = deviceId
    self.channelId = channelId
    self.binaryData = binaryData

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.id = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.data = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.type = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.time = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.STRING:
          self.deviceId = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.STRING:
          self.channelId = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.STRING:
          self.binaryData = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('EventDetails')
    if self.id is not None:
      oprot.writeFieldBegin('id', TType.STRING, 1)
      oprot.writeString(self.id)
      oprot.writeFieldEnd()
    if self.data is not None:
      oprot.writeFieldBegin('data', TType.STRING, 2)
      oprot.writeString(self.data)
      oprot.writeFieldEnd()
    if self.type is not None:
      oprot.writeFieldBegin('type', TType.STRING, 3)
      oprot.writeString(self.type)
      oprot.writeFieldEnd()
    if self.time is not None:
      oprot.writeFieldBegin('time', TType.STRING, 4)
      oprot.writeString(self.time)
      oprot.writeFieldEnd()
    if self.deviceId is not None:
      oprot.writeFieldBegin('deviceId', TType.STRING, 5)
      oprot.writeString(self.deviceId)
      oprot.writeFieldEnd()
    if self.channelId is not None:
      oprot.writeFieldBegin('channelId', TType.STRING, 6)
      oprot.writeString(self.channelId)
      oprot.writeFieldEnd()
    if self.binaryData is not None:
      oprot.writeFieldBegin('binaryData', TType.STRING, 7)
      oprot.writeString(self.binaryData)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
