#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import threading
# import logging
# import socket
import ftplib

import time,datetime
import os





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



