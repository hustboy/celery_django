from django.test import TestCase

# Create your tests here.

from filemanager.telnet import bscdump,gsap2dump,gsap1dump
from filemanager.dump import delbscfile,delgsfile
import logging
import pexpect


import time,datetime
import os

class Logger:
    def __init__(self, path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


bscip={'whbsc88':'10.26.2.36'}

bscusername='wh1cx2'
bscpassword='aqyqZBT#27'

#
# LOG_DIR = os.path.join(settings.MEDIA_ROOT, "logs/")

# logftp = Logger(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'ftpdumplog.txt', logging.ERROR,
#                 logging.DEBUG)
# fout = open('/home/chenxi/PycharmProjects/filemanager/media/logs' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'log.txt', 'wb')
# dumpdir='/mnt/usb/'+'妙墩备份'+time.strftime("%Y-%m", time.localtime())
# os.mkdir(dumpdir)
# os.mkdir(dumpdir+'/cpdump')
# os.mkdir(dumpdir + '/apdump')
# os.mkdir(dumpdir + '/mgwdump')
#
# for key, value in bscip.items():
#     ftpcpapdump(key, value, bscusername, bscpassword,fout,logftp,dumpdir)
#
# fout.close()


# child = pexpect.spawn('telnet '+'10.26.2.36')
# loginprompt = '\x03>'
#
# child.logfile_read = fout
# child.expect('login name:')
# child.send(bscusername+'\r')
# child.expect_exact('password:')
# child.send(bscpassword+'\r')
# child.expect('Windows NT Domain:')
# child.send('\r')
# child.expect(loginprompt)
# child.sendline('dir\r')
# child.expect(loginprompt)
# print(child.before)
#
# child.close(force=True)
# fout.close()
import re
import configparser


# s1="WHGS48AP1A:Save all disk information and runtime parameter data to file \\WHGS48AP1A\C$\acs\data\BUR\WHGS48AP1A_20171203_120811.ddi completedSave all disk information and runtime parameter data to file \\WHGS48AP1B\C$\acs\data\BUR\WHGS48AP1B_20171203_120811.ddi completedContinuing with partition backup please waitTrying 10.26.3.163...Connected to 10.26.3.163."
#
#
# p = re.compile(r'[\w]+\.[di]+',re.M)
#
# filename=p.findall(s1)
#
# print(p.findall(s1)[0].replace('ddi','zip'))
# config=configparser.ConfigParser()
# config.read("DumpRecord.ini")
#
# fout = open('/home/chenxi/PycharmProjects/filemanager/media/logs/' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'log.txt', 'wb')
#
#
# child = pexpect.spawn('telnet '+'10.26.2.54')
# loginprompt = '\x03>'
#
# child.logfile_read = fout
# child.expect('login name:')
# child.send(bscusername+'\r')
# child.expect_exact('password:')
# child.send(bscpassword+'\r')
# child.expect('Windows NT Domain:')
# child.send('\r')
# child.expect(loginprompt)
# child.send('k:\r')
# child.expect(loginprompt)
# child.send('cd \\images\\nodea\r')
# child.expect(loginprompt)
# child.send('dir\r')
# child.expect(loginprompt)
# burstring=child.before
#
# p = re.compile(r'[\w]+\.[di]+', re.M)
# config.set('whbsc56'.upper(), 'dumpa', p.findall(burstring.decode())[0].replace('ddi', 'zip'))
# config.set('whbsc56'.upper(), 'dumpb', p.findall(burstring.decode())[1].replace('ddi', 'zip'))
# config.write(open("DumpRecord.ini", "w"))
# child.close(force=True)
# fout.close()
# config=configparser.ConfigParser()
#
# #DumpRecord.ini.ini可以是一个不存在的文件，意味着准备新建配置文件。
# config.read("DumpRecord.ini")
#
#
# # LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
# config.set('whbsc88'.upper(), 'dumpb',"aaaaaa")
# config.write(open("DumpRecord.ini", "w"))

config=configparser.ConfigParser()

#DumpRecord.ini.ini可以是一个不存在的文件，意味着准备新建配置文件。
config.read("IpConfig.ini")


# LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

# bscip={}
# for key in config['BSCIP']:
#     bscip[key] = config['BSCIP'][key]
# bscusername=config['BSCUSER']['username']
# bscpassword=config['BSCUSER']['password']
# gsap1ip={}
# for key in config['GSAP1IP']:
#     gsap1ip[key] = config['GSAP1IP'][key]
# gsap1username=config['GSAP1USER']['username']
# gsap1password=config['GSAP1USER']['password']
# gsap2ip={}
# for key in config['GSAP2IP']:
#     gsap2ip[key] = config['GSAP2IP'][key]
# gsap2username=config['GSAP2USER']['username']
# gsap2password=config['GSAP2USER']['password']
#
# config1=configparser.ConfigParser()
# config1.read("DumpRecord.ini")
# logdump = Logger('/home/chenxi/PycharmProjects/filemanager/media/logs/' +time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'ftpdumplog.txt', logging.ERROR,logging.DEBUG)
# fout = open('/home/chenxi/PycharmProjects/filemanager/media/logs/' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'log.txt', 'wb')
#
# for key, value in bscip.items():
#     print(key)
#     if 'bsc60' in key:
#         print(key)
#         delbscfile(key, value, bscusername, bscpassword, logdump,timeout=0)
#
# fout.close()
from hashlib import md5, sha1
from zlib import crc32
import sys
# def getMd5(filename): #计算md5
#     mdfive = md5()
#     with open(filename, 'rb') as f:
#         mdfive.update(f.read())
#     return mdfive.hexdigest()
#
# def getSha1(filename): #计算sha1
#     sha1Obj = sha1()
#     with open(filename, 'rb') as f:
#         sha1Obj.update(f.read())
#     return sha1Obj.hexdigest()
#
# def getCrc32(filename): #计算crc32
#     with open(filename, 'rb') as f:
#         return crc32(f.read())
# print(getMd5('/mnt/usb/妙墩备份20171208/mgwdump/whgm17/d/configuration/cv/Au_CXP9018138%2_R177A04_171206_0400/softwareinformation.xml'))
# print('{:8} {}'.format('sha1:', getSha1('/mnt/usb/妙墩备份20171208/mgwdump/whgm17/d/configuration/cv/Au_CXP9018138%2_R177A04_171206_0400/softwareinformation.xml')))
# print('{:8} {:x}'.format('crc32:', getCrc32('/mnt/usb/妙墩备份20171208/mgwdump/whgm17/d/configuration/cv/Au_CXP9018138%2_R177A04_171206_0400/softwareinformation.xml')))
# def getMd5(filename): #计算md5
#     mdfive = md5()
#     with open(filename, 'rb') as f:
#         mdfive.update(f.read())
#     return mdfive.hexdigest()
#
# def getSha1(filename): #计算sha1
#     sha1Obj = sha1()
#     with open(filename, 'rb') as f:
#         sha1Obj.update(f.read())
#     return sha1Obj.hexdigest()
#
# def getCrc32(filename): #计算crc32
#     with open(filename, 'rb') as f:
#         return crc32(f.read())
#
#
# def checkmd5(mgwdir,md5filerecord):
#     dirlist = os.listdir(mgwdir + '/d/configuration/cv/')
#
#     for item in dirlist:
#         if item.find('Au_CX') != -1:
#             md5dir = item
#             break
#
#
#     md5file = open(mgwdir + '/d/configuration/cv/' + md5dir + '/md5checksums', 'r')
#     for line in md5file:
#         otherfile=line.split()
#         print(otherfile[0])
#         if otherfile[1]==getMd5(mgwdir + '/d/configuration/cv/' + md5dir + '/'+otherfile[0]):
#             md5filerecord.writelines('文件: '+mgwdir + '/d/configuration/cv/' + md5dir + '/'+otherfile[0]+"\n")
#             md5filerecord.writelines('大小:'+str(os.path.getsize(mgwdir + '/d/configuration/cv/' + md5dir + '/'+otherfile[0]))+'字节'+"\n")
#
#             ctime = datetime.datetime.fromtimestamp((os.path.getmtime(mgwdir + '/d/configuration/cv/' + md5dir + '/' + otherfile[0])))
#             mtime= ctime.strftime("%Y年%d月%d日, %H:%M:%S")
#             md5filerecord.writelines('修改时间:' + mtime+"\n")
#
#             md5filerecord.writelines('MD5:' +getMd5(mgwdir + '/d/configuration/cv/' + md5dir + '/'+otherfile[0])+"\n")
#             md5filerecord.writelines('SHA1:' + getSha1(mgwdir + '/d/configuration/cv/' + md5dir + '/' + otherfile[0])+"\n")
#             md5filerecord.writelines('CRC32:' + str(getCrc32(mgwdir + '/d/configuration/cv/' + md5dir + '/' + otherfile[0]))+"\n")
#
#             md5filerecord.writelines("\n")
#
#
#
#     md5file.close()
#
#
# fp = open('/mnt/usb/妙墩备份20171208/mgwdump/md5check.txt', 'w')
#
#
# checkmd5('/mnt/usb/妙墩备份20171208/mgwdump/whgm17',fp)
# fp.close()




import xlsxwriter

# workbook = xlsxwriter.Workbook('headers_footers.xlsx')
# # preview = 'Select Print Preview to see the header and footer'
# worksheet=workbook.add_worksheet()
# # data = ('Foo', 'Bar', 'Baz')
# data=('省份地市', '备份与拷出日期','设备厂家',	'网元','备份方式与频率','备份拷出频率','备份拷出文件校验有效性',	'备份拷出文件有效性校验是否通过','备份拷出人','备份拷出审核人','拷出备份文件有效性检验（MD5校验码，比对文件大小）/月','月度有效性校验是否通过')
# row = 0
# col = 0
# # Write the data to a sequence of cells.
# worksheet.write_row(row,col, data)
# worksheet.set_column(0, 11, 30)
# row+=1
# data=('湖北省','2017-12-4','爱立信','WHGS42','CP自动/日,AP自动/周','月','CP：915,820,544（字节）AP1A：1,827，841,342（字节）AP1B:1,833,444,592（字节',	'是'	,'','刘凯轶','','')
# worksheet.write_row(row,col, data)
#
# workbook.close()

# from filemanager.telnet import FileSize
# ftpdata = time.strftime("%Y-%m-%d", time.localtime())
# workbook = xlsxwriter.Workbook('MSC备份与拷出记录表-武汉大区(妙墩）.xlsx')
#
# worksheet = workbook.add_worksheet()
#
# data = ('省份地市', '备份与拷出日期', '设备厂家', '网元', '备份方式与频率', '备份拷出频率', '备份拷出文件校验有效性', '备份拷出文件有效性校验是否通过', '备份拷出人', '备份拷出审核人',
#         '拷出备份文件有效性检验（MD5校验码，比对文件大小）/月', '月度有效性校验是否通过')
# row = 0
# col=0
#
# # Write the data to a sequence of cells.
# worksheet.write_row(row,col, data)
# worksheet.set_column(0, 11, 30)
#
#
# print('/mnt/usb/妙墩备份20171209' + '/cpdump/' + 'whbsc33')
# cpfilesize = FileSize('/mnt/usb/妙墩备份20171209' + '/cpdump/' + 'whbsc33')
#
# ap1afilesize = os.path.getsize('/mnt/usb/妙墩备份20171209' + '/apdump/' + 'WHBSC33AP1A_20171208_173508.zip')
# ap1bfilesize = os.path.getsize('/mnt/usb/妙墩备份20171209' + '/apdump/' + 'WHBSC33AP1B_20171208_173508.zip')
#
# row += 1
# data = ('湖北省', ftpdata, '爱立信', 'WHGS42', 'CP自动/日,AP自动/周', '月',
#         'CP：' + str(cpfilesize) + '（字节）AP1A：' + str(ap1afilesize) + '（字节）AP1B:' + str(ap1bfilesize) + '（字节',
#         '是', '', '刘凯轶', '', '')
# print(data)
#
# worksheet.write_row(row,col, data)
#
#
# workbook.close()





import configparser
from filemanager.telnet import bscdump,gsap2dump,gsap1dump,ftpap1dump,ftpap2dump,ftpmgwdump,FileSize
from filemanager.dump import delbscfile,delgsfile
import logging

import time,datetime
import os
import xlsxwriter
config=configparser.ConfigParser()

#DumpRecord.ini.ini可以是一个不存在的文件，意味着准备新建配置文件。
config.read("IpConfig.ini")
dumprecord=configparser.ConfigParser()

#DumpRecord.ini.ini可以是一个不存在的文件，意味着准备新建配置文件。
dumprecord.read("DumpRecord.ini")
LOG_DIR = os.path.join('/home/chenxi/PycharmProjects/filemanager/media/', "logs/")

# LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

bscip={}
for key in config['BSCIP']:
    bscip[key] = config['BSCIP'][key]
bscusername=config['BSCUSER']['username']
bscpassword=config['BSCUSER']['password']
gsap1ip={}
for key in config['GSAP1IP']:
    gsap1ip[key] = config['GSAP1IP'][key]
gsap1username=config['GSAP1USER']['username']
gsap1password=config['GSAP1USER']['password']
gsap2ip={}
for key in config['GSAP2IP']:
    gsap2ip[key] = config['GSAP2IP'][key]
gsap2username=config['GSAP2USER']['username']
gsap2password=config['GSAP2USER']['password']

gmip={}
for key in config['GMIP']:
    gmip[key] = config['GMIP'][key]
gmusername=config['GMUSER']['username']
gmpassword=config['GMUSER']['password']

logftp = Logger(LOG_DIR + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'ftpdumplog.txt', logging.ERROR,
                logging.DEBUG)
fout = open(LOG_DIR + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'log.txt', 'wb')
dumpdir='/mnt/usb/'+'妙墩备份'+time.strftime("%Y%m%d", time.localtime())



# os.mkdir(dumpdir)
# os.mkdir(dumpdir+'/cpdump')
# os.mkdir(dumpdir + '/apdump')
# os.mkdir(dumpdir + '/mgwdump')

# for key, value in bscip.items():
#     ftpap1dump(key, value, bscusername, bscpassword,fout,logftp,dumpdir,dumprecord)


ftpdata=time.strftime("%Y-%m-%d", time.localtime())
workbook = xlsxwriter.Workbook(dumpdir+'/MSC备份与拷出记录表-武汉大区(妙墩）.xlsx')

worksheet = workbook.add_worksheet()

data = ('省份地市', '备份与拷出日期', '设备厂家', '网元', '备份方式与频率', '备份拷出频率', '备份拷出文件校验有效性', '备份拷出文件有效性校验是否通过', '备份拷出人', '备份拷出审核人',
        '拷出备份文件有效性检验（MD5校验码，比对文件大小）/月', '月度有效性校验是否通过')
row=0
col=0
# Write the data to a sequence of cells.
worksheet.write_row(row, col, data)
worksheet.set_column(row, 11, 30)

for key, value in gsap1ip.items():
    print(key)
    if 'gs42' in key:
        # ftpap1dump(key, value, gsap1username, gsap1password,fout,logftp,dumpdir,dumprecord)
        cpfilesize=FileSize(dumpdir + '/cpdump/' + key[:6])
        if 'AP1A' in dumprecord[key.upper()]['dumpa']:
            ap1afilesize=os.path.getsize(dumpdir + '/apdump/' + dumprecord[key.upper()]['dumpa'])
            ap1bfilesize = os.path.getsize(dumpdir + '/apdump/' + dumprecord[key.upper()]['dumpb'])
        else:
            ap1afilesize=os.path.getsize(dumpdir + '/apdump/' + dumprecord[key.upper()]['dumpb'])
            ap1bfilesize = os.path.getsize(dumpdir + '/apdump/' + dumprecord[key.upper()]['dumpa'])
        print('湖北省', ftpdata, '爱立信', 'WHGS42', 'CP自动/日,AP自动/周', '月',
              'CP：'+str(cpfilesize)+'（字节）AP1A：'+str(ap1afilesize)+'（字节）AP1B:'+str(ap1bfilesize)+'（字节', '是', '', '刘凯轶', '', '')
        data = ('湖北省', ftpdata, '爱立信', 'WHGS42', 'CP自动/日,AP自动/周', '月',
                'CP：'+str(cpfilesize)+'（字节）AP1A：'+str(ap1afilesize)+'（字节）AP1B:'+str(ap1bfilesize)+'（字节', '是', '', '刘凯轶', '', '')
        print(data)
        row+=1
        worksheet.write_row(row, col, data)

workbook.close()

# for key, value in gsap2ip.items():
#     ftpap1dump(key, value, gsap1username, gsap1password, fout, logftp, dumpdir, dumprecord)
#
#
#
#
#
#
# for key, value in gsap2ip.items():
#     ftpap2dump(key, value, gsap2username, gsap2password,fout,logftp,dumpdir,dumprecord)
#
# fp = open(dumpdir + '/mgwdump/md5check.txt', 'w')
# for key, value in gmip.items():
#     ftpmgwdump(key, value, gmusername, gmpassword, fout, logftp, dumpdir,fp)
# fp.close()
fout.close()
