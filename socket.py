#-*- coding: UTF-8 -*-
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet import reactor
import random
import string
import sys
import binascii
import time
#配置挡板地址
HOST='192.68.1.18'
#配置挡板端口
PORT='50000'
#配置挡板时间
wait=0
#配置挡板计时器
i=1
#配置挡板响应报文
#ASCII码响应报文
response_ascii='000646<?xml version="1.0" encoding="UTF-8"?><ebank><head><H_TRANS_CODE>bswils</H_TRANS_CODE><H_TRANS_SEQ>595913221414</H_TRANS_SEQ><H_TRANS_DATE>20180308</H_TRANS_DATE><H_CHANN_ID>001</H_CHANN_ID><H_ZPK_INDEX>500</H_ZPK_INDEX></head><date><acctno>6000000223</acctno><idtfno>513822199205226001</idtfno><idtftp>10</idtftp><recvac>62176052080000010</recvac><recvna>包商测试1500255757</recvna><brchna>包商银行</brchna><bankcd>0301</bankcd><tranam>10.0</tranam><crcycd>01</crcycd><charge>0</charge><passtp>Y</passtp><passfg>1</passfg><remark>asdfasdfasdfasd</remark></date></ebank>'
class twisted_mock(LineOnlyReceiver):
    def dataReceived(self,H_TRANS_CODE):
        rcv1=H_TRANS_CODE
        rcv=rcv1[71:77]
        print (rcv)
        print (rcv.find('bswils'))
        #判断请求报文交易码
        if(rcv.find('bswils')==0):
            senddate=response_ascii
            print (response_ascii)
        else:
            senddate='error request_ascii'
        #设置时间
        time.sleep(wait)
        #发送响应报文
        self.transport.write(senddate)
        #服务器主动断开连接，如果挡板要求长链接，注释此行
        self.transport.loseConnection()
        global i
        print ('[%d]:%s' % (i,rcv))
        i = i+1
    def getId(self):
        return str(self.transport.getPeer())
    def connectionLost(self):
        print ('user connected')
    def connectionLost(self,reason):
        print (self.transport.client,'disconnected')
factory = Factory()
factory.protocol = twisted_mock
reactor.listenTCP(50000,factory)
reactor.run()