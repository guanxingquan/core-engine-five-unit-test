#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#



from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import logging

log = logging.getLogger("ThriftClient")
def getThriftClient(host,port,service):
    '''
    
    :param host:
    :param port:
    :param service:
    '''
    global transport 
    #print "[begin]----------------build a thrift client"
    # Make socket
    transport = TSocket.TSocket(host, port)
#     transport.setTimeout(10000)
    # Buffering is critical. Raw sockets are very slow
#     transport = TTransport.TBufferedTransport(transport)
    transport = TTransport.TFramedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
    client = service.Client(protocol)
    transport.open()
    return client
  
  
def closeThriftClient():
    #print "[end]----------------now close the thrift client"

    transport.close()
