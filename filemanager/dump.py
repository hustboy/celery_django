#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import threading
# import logging
# import socket
import ftplib

import time,datetime
import os


# def setInterval(interval, times = -1):
#     # This will be the actual decorator,
#     # with fixed interval and times parameter
#     def outer_wrap(function):
#         # This will be the function to be
#         # called
#         def wrap(*args, **kwargs):
#             stop = threading.Event()
#
#             # This is another function to be executed
#             # in a different thread to simulate setInterval
#             def inner_wrap():
#                 i = 0
#                 while i != times and not stop.isSet():
#                     stop.wait(interval)
#                     function(*args, **kwargs)
#                     i += 1
#
#             t = threading.Timer(0, inner_wrap)
#             t.daemon = True
#             t.start()
#             return stop
#         return wrap
#     return outer_wrap
#
#
# class PyFTPclient:
#     def __init__(self, host, port, login, passwd,logfile, monitor_interval = 30):
#         self.host = host
#         self.port = port
#         self.login = login
#         self.passwd = passwd
#         self.monitor_interval = monitor_interval
#         self.ptr = None
#         self.max_attempts = 15
#         self.waiting = True
#         self.logfile=logfile
#
#
#     def DownloadFile(self, dst_filename, local_filename = None):
#         res = ''
#         if local_filename is None:
#             local_filename = dst_filename
#
#         with open(local_filename, 'w+b') as f:
#             self.ptr = f.tell()
#
#             @setInterval(self.monitor_interval)
#             def monitor():
#                 if not self.waiting:
#                     i = f.tell()
#                     if self.ptr < i:
#                         self.logfile.debug("%d  -  %0.1f Kb/s" % (i, (i-self.ptr)/(1024*self.monitor_interval)))
#                         self.ptr = i
#                     else:
#                         ftp.close()
#
#
#             def connect():
#                 ftp.connect(self.host, self.port)
#                 ftp.login(self.login, self.passwd)
#                 # optimize socket params for download task
#                 ftp.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
#                 ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 75)
#                 ftp.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
#
#             ftp = ftplib.FTP()
#             ftp.set_debuglevel(2)
#             ftp.set_pasv(True)
#
#             connect()
#             ftp.voidcmd('TYPE I')
#             dst_filesize = ftp.size(dst_filename)
#
#             mon = monitor()
#             while dst_filesize > f.tell():
#                 try:
#                     connect()
#                     self.waiting = False
#                     # retrieve file from position where we were disconnected
#                     res = ftp.retrbinary('RETR %s' % dst_filename, f.write) if f.tell() == 0 else \
#                               ftp.retrbinary('RETR %s' % dst_filename, f.write, rest=f.tell())
#
#                 except:
#                     self.max_attempts -= 1
#                     if self.max_attempts == 0:
#                         mon.set()
#                         self.logfile.exception('')
#                         raise
#                     self.waiting = True
#                     self.logfile.info('waiting 30 sec...')
#                     time.sleep(30)
#                     self.logfile.info('reconnect')
#
#
#             mon.set() #stop monitor
#             ftp.close()
#
#             if not res.startswith('226 Transfer complete'):
#                 self.logfile.error('Downloaded file {0} is not full.'.format(dst_filename))
#                 # os.remove(local_filename)
#                 return None
#
#
#
#             return 1


# if __name__ == "__main__":
    #        logging.basicConfig(filename='/var/log/dreamly.log',format='%(asctime)s %(levelname)s: %(message)s',level=logging.DEBUG)
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #                     datefmt='%a, %d %b %Y %H:%M:%S',
    #                     filename=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'ftplog.txt',
    #                     filemode='w')
    # obj = PyFTPclient('10.26.2.36', 21, 'wh1cx2', 'aqyqZBT#27')


def delgsfile(nodename, ip, username, password,logfile,timeout):
    ftp = ftplib.FTP()  # 设置变量
    ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect(ip, 21)  # 连接的ftp sever和端口
    ftp.login(username, password)  # 连接的用户名，密码
    ftp.getwelcome()  # 打印出欢迎信息
    your_list = []

    # ftp.dir() 命令会列出目录中的文件
    ftp.dir("\Images\\Nodea", your_list.append)
    for x in your_list:
        filename = x.split()[0:9]
        d1 = datetime.datetime.today()
        print(d1)
        print(filename)
        d2 = datetime.datetime.strptime(filename[5] + '-' + filename[6] + '-' + '2018', "%b-%d-%Y")

        # 或者filename = x.split("\t")[列的起始值:列的终止值]
        if (d1 - d2).days > timeout:
            print(filename)

            ftp.delete(os.path.basename("\Images\\Nodea\\" + filename[8]))
        else:
            logfile.info(nodename + "keep on " + filename[8])

    your_list = []
    ftp.dir("\Images\\Nodeb", your_list.append)
    for x in your_list:
        filename = x.split()[0:9]
        d1 = datetime.datetime.today()
        print(d1)
        print(filename)

        d2 = datetime.datetime.strptime(filename[5] + '-' + filename[6] + '-' + '2018', "%b-%d-%Y")

        # 或者filename = x.split("\t")[列的起始值:列的终止值]
        if (d1 - d2).days > timeout:
            print(filename)

            ftp.delete(os.path.basename("\Images\\Nodeb\\" + filename[8]))
        else:
            logfile.info(nodename + "keep on " + filename[8])

    logfile.info('--------------------------------------------------------------------------------------')
    ftp.close()

def delbscfile(nodename, ip, username, password, logfile,timeout):
    ftp = ftplib.FTP()  # 设置变量
    ftp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
    ftp.connect(ip, 21)  # 连接的ftp sever和端口
    ftp.login(username, password)  # 连接的用户名，密码
    ftp.getwelcome()  # 打印出欢迎信息
    your_list = []

    # ftp.dir() 命令会列出目录中的文件
    ftp.dir("\Images\\Nodea", your_list.append)
    for x in your_list:
        filename = x.split()[0:8]
        d1 = datetime.datetime.today()
        print(d1)
        print(filename)
        if filename[0].find('-') == -1:
            d2 = datetime.datetime.strptime(filename[0], "%m/%d/%Y")

        else:
            d2 = datetime.datetime.strptime(filename[0], "%m-%d-%y")

        # 或者filename = x.split("\t")[列的起始值:列的终止值]
        if (d1 - d2).days > timeout:
            print(filename)
            print(filename[3].split('.')[0])
            ftp.delete(os.path.basename("\Images\\Nodea\\" + filename[3]))
        else:


            logfile.info(nodename + "keep on " + filename[3])

    your_list = []
    ftp.dir("\Images\\Nodeb", your_list.append)
    for x in your_list:
        filename = x.split()[0:8]
        d1 = datetime.datetime.today()
        print(d1)
        print(filename)
        if filename[0].find('-') == -1:
            d2 = datetime.datetime.strptime(filename[0], "%m/%d/%Y")

        else:
            d2 = datetime.datetime.strptime(filename[0], "%m-%d-%y")

        # 或者filename = x.split("\t")[列的起始值:列的终止值]
        if (d1 - d2).days > timeout:
            print(filename)
            print(filename[3].split('.')[0])
            ftp.delete(os.path.basename("\Images\\Nodeb\\" + filename[3]))
        else:
            logfile.info(nodename + "keep on " + filename[3])
    logfile.info('--------------------------------------------------------------------------------------')
    ftp.close()
    # 不确定 是不是第5列到第8列的信息, 需要自己再确定一下.



