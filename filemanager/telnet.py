#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,time,sys,logging
os.environ["TERM"]="vt100"
import pexpect
import re
import configparser
from hashlib import md5, sha1
from zlib import crc32
import datetime

# logging.basicConfig(level=logfile.DEBUG,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'applog.txt',
#                 filemode='w')
#
# bscip = {'BSC33': '10.26.3.129', 'BSC42': '10.26.2.37', 'BSC45': '10.26.3.182', 'BSC45': '10.26.3.182',
#       'BSC49': '10.26.3.185', 'BSC55': '10.26.2.51', 'BSC56': '10.26.2.54', 'BSC60': '10.26.2.57',
#       'BSC67': '10.26.2.45', 'BSC79': '10.26.2.40', 'BSC88': '10.26.2.36'}
# bscip1 = {'BSC79': '10.26.2.40', 'BSC88': '10.26.2.36'}
# bscusername='wh1cx2'
# bscpassword='aqyqZBT#27'
# gsap1ip={'GS42': '10.26.3.163', 'GS43': '10.26.3.170', 'GS48': '10.26.3.176'}
# gsap1username='admineric'
# gsap1password='aqyqZBT#07'
# gsap2ip={'GS42': '10.25.254.35', 'GS43': '10.25.254.38', 'GS48': '10.25.254.41'}
# gsap1username='administrator'
# gsap1password='aqyqZBT#23'
config=configparser.ConfigParser()
config.read("DumpRecord.ini")



def bscdump (nodename,ip,username,password,fout,logfile,configfile):
    child = pexpect.spawn('telnet '+ip)
    loginprompt = '\x03>'

    child.logfile_read = fout
    child.expect('login name:')
    child.send(username+'\r')
    child.expect_exact('password:')
    child.send(password+'\r')
    child.expect('Windows NT Domain:')
    child.send('\r')
    child.expect(loginprompt)
    child.sendline('mml sybue;\r')
    index=child.expect([loginprompt, pexpect.EOF, pexpect.TIMEOUT])
    if (index == 0):
        child.sendline('mml sybfp:file;\r')
        index = child.expect(['SYSTEM BACKUP FILES', pexpect.EOF, pexpect.TIMEOUT])
        if(index==0):
            time.sleep(10)
            child.sendline('mml sybup:file=relfsw3;\r')
            index = child.expect(['TEST AND RELOCATION OF STORES IN PROGRESS', pexpect.EOF, pexpect.TIMEOUT])
            if (index == 0):
                time.sleep(60)

                i=10
                while ( i>0):
                    child.sendline('mml sybfp:file;\r')
                    index = child.expect(['SYSTEM BACKUP FILES', 'FUNCTION BUSY',pexpect.EOF, pexpect.TIMEOUT])
                    if index == 0:

                        break

                    elif index == 1:

                        i -= 1
                        time.sleep(60)
                    else:
                        logfile.info(nodename + 'dump not successed')
                        child.close(force=True)
                        return
                time.sleep(10)
                child.sendline('mml sytuc;\r')
                index = child.expect(['COMMAND EXECUTED', pexpect.EOF, pexpect.TIMEOUT])
                if (index == 0):
                    time.sleep(10)
                    child.sendline('mml sybui;\r')
                    index = child.expect(['EXECUTED', pexpect.EOF, pexpect.TIMEOUT])
                    if (index == 0):
                        child.sendline('copy /y k:\\fms\\data\\cpf\\relvolumsw\\relfsw0\\*.* K:\\ftpvol\\relfsw0\r')
                        index = child.expect(['copied', pexpect.EOF, pexpect.TIMEOUT],
                                             timeout=600)
                        if (index == 0):
                            time.sleep( 10)
                            child.sendline('burbackup -o\r')
                            index = child.expect(['[y=yes, n=no]?\x03:', pexpect.EOF, pexpect.TIMEOUT])
                            if (index == 0):
                                time.sleep(5)
                                child.sendline('y\r')
                                index = child.expect(['Continuing with partition backup please wait', pexpect.EOF, pexpect.TIMEOUT])
                                if (index == 0):
                                    time.sleep(60)
                                    burstring = child.before

                                    p = re.compile(r'[\w]+\.[di]+', re.M)
                                    # p = re.compile(r'[\w]+\.[zip]+', re.M)
                                    configfile.set(nodename.upper(), 'dumpa',p.findall(burstring.decode())[0].replace('ddi', 'zip'))
                                    configfile.set(nodename.upper(), 'dumpb',p.findall(burstring.decode())[1].replace('ddi', 'zip'))
                                    configfile.write(open("DumpRecord.ini", "w"))
                                    child.close(force=True)
                                    logfile.info(nodename + 'dump successed')
                                    return
                                else:
                                    logfile.info(nodename + 'dump not successed')
                                    child.close(force=True)
                                    return
                            else:
                                logfile.info(nodename + 'dump not successed')
                                child.close(force=True)
                                return

                        else:
                            logfile.info(nodename + 'dump not successed')
                            child.close(force=True)
                            return

                    else:
                        logfile.info(nodename + 'dump not successed')
                        child.close(force=True)
                        return

                else:
                    logfile.info(nodename + 'dump not successed')
                    child.close(force=True)
                    return
            else:
                logfile.info(nodename + 'dump not successed')
                child.close(force=True)
                return
        else:
            logfile.info(nodename + 'dump not successed')
            child.close(force=True)
            return
    else:
        # 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出.
        logfile.info(nodename + 'dump not successed')
        child.close(force=True)
        return


def gsap1dump (nodename,ip,username,password,fout,logfile,configfile):
    child = pexpect.spawn('telnet '+ip)
    loginprompt = '\x03>'

    child.logfile_read = fout
    child.expect('login name:')
    child.send(username+'\r')
    child.expect_exact('password:')
    child.send(password+'\r')
    child.expect('Windows NT Domain:')
    child.send('\r')
    child.expect(loginprompt)
    child.sendline('mml sybue;\r')
    index=child.expect([loginprompt, pexpect.EOF, pexpect.TIMEOUT])
    if (index == 0):
        child.sendline('mml sybfp:file;\r')
        index = child.expect(['SYSTEM BACKUP FILES', pexpect.EOF, pexpect.TIMEOUT])
        if(index==0):
            time.sleep(10)
            child.sendline('mml sybup:file=relfsw2;\r')
            index = child.expect(['TEST AND RELOCATION OF STORES IN PROGRESS', pexpect.EOF, pexpect.TIMEOUT])
            if (index == 0):
                time.sleep(60)

                i=10
                while ( i>0):
                    child.sendline('mml sybfp:file;\r')
                    index = child.expect(['SYSTEM BACKUP FILES', 'FUNCTION BUSY',pexpect.EOF, pexpect.TIMEOUT])
                    if index == 0:

                        break

                    elif index == 1:

                        i -= 1
                        time.sleep(60)
                    else:
                        logfile.info(nodename + 'dump not successed')
                        child.close(force=True)
                        return
                time.sleep(10)
                child.sendline('mml sytuc;\r')
                index = child.expect(['COMMAND EXECUTED', pexpect.EOF, pexpect.TIMEOUT])
                if (index == 0):
                    time.sleep(10)
                    child.sendline('mml sybui;\r')
                    index = child.expect(['EXECUTED', pexpect.EOF, pexpect.TIMEOUT])
                    if (index == 0):
                        child.sendline('copy /y l:\\fms\\data\\cpf\\relvolumsw\\relfsw0\\*.* g:\\ftpvol\\relfsw0\r')
                        index = child.expect(['copied', pexpect.EOF, pexpect.TIMEOUT],
                                             timeout=600)
                        if (index == 0):
                            time.sleep(5)
                            child.sendline('burbackup -o\r')
                            index = child.expect(['[y=yes, n=no]?\x03:', pexpect.EOF, pexpect.TIMEOUT])
                            if (index == 0):
                                time.sleep(5)
                                child.sendline('y\r')
                                index = child.expect(['Continuing with partition backup please wait', pexpect.EOF, pexpect.TIMEOUT])
                                if (index == 0):
                                    time.sleep(60)
                                    burstring = child.before

                                    p = re.compile(r'[\w]+\.[di]+', re.M)
                                    # p = re.compile(r'[\w]+\.[zip]+', re.M)
                                    configfile.set(nodename.upper(), 'dumpa',p.findall(burstring.decode())[0].replace('ddi', 'zip'))
                                    configfile.set(nodename.upper(), 'dumpb',p.findall(burstring.decode())[1].replace('ddi', 'zip'))
                                    configfile.write(open("DumpRecord.ini", "w"))
                                    child.close(force=True)
                                    logfile.info(nodename + 'dump successed')
                                    return
                                else:
                                    logfile.info(nodename + 'dump not successed')
                                    child.close(force=True)
                                    return
                            else:
                                logfile.info(nodename + 'dump not successed')
                                child.close(force=True)
                                return

                        else:
                            logfile.info(nodename + 'dump not successed')
                            child.close(force=True)
                            return

                    else:
                        logfile.info(nodename + 'dump not successed')
                        child.close(force=True)
                        return

                else:
                    logfile.info(nodename + 'dump not successed')
                    child.close(force=True)
                    return
            else:
                logfile.info(nodename + 'dump not successed')
                child.close(force=True)
                return
        else:
            logfile.info(nodename + 'dump not successed')
            child.close(force=True)
            return
    else:
        # 匹配到了 pexpect.EOF 或 pexpect.TIMEOUT，表示超时或者 EOF，程序打印提示信息并退出.
        logfile.info(nodename + 'dump not successed')
        child.close(force=True)
        return


def gsap2dump (nodename,ip,username,password,fout,logfile,configfile):
    child = pexpect.spawn('telnet '+ip)
    loginprompt = '\x03>'

    child.logfile_read = fout
    child.expect('login name:')
    child.send(username+'\r')
    child.expect_exact('password:')
    child.send(password+'\r')
    child.expect('Windows NT Domain:')
    child.send('\r')
    child.expect(loginprompt)

    child.sendline('burbackup -o\r')
    index = child.expect(['[y=yes, n=no]?\x03:', pexpect.EOF, pexpect.TIMEOUT])
    if (index == 0):
        time.sleep(5)
        child.sendline('y\r')
        index = child.expect(['Continuing with partition backup please wait', pexpect.EOF, pexpect.TIMEOUT])
        if (index == 0):
            time.sleep(60)
            burstring = child.before

            p = re.compile(r'[\w]+\.[di]+', re.M)

            # p = re.compile(r'[\w]+\.[zip]+', re.M)
            configfile.set(nodename.upper(), 'dumpa', p.findall(burstring.decode())[0].replace('ddi', 'zip'))
            configfile.set(nodename.upper(), 'dumpb', p.findall(burstring.decode())[1].replace('ddi', 'zip'))
            configfile.write(open("DumpRecord.ini", "w"))
            child.close(force=True)
            logfile.info(nodename + 'dump successed')
            return
        else:
            logfile.info(nodename + 'dump not successed')
            child.close(force=True)
            return
    else:
        logfile.info(nodename + 'dump not successed')
        child.close(force=True)
        return



def ftpap1dump(nodename,ip,username,password,fout,logfile,dumpdir,configfile):

    child = pexpect.spawn('lftp ' + username+':'+password+'@'+ip)
    loginprompt = '/>'
    if 'bsc' in nodename :
        cpdir=dumpdir+'/cpdump/'+nodename
    else:
        cpdir = dumpdir + '/cpdump/' + nodename[:6]
    os.mkdir(cpdir)
    apdir= dumpdir+'/apdump/'

    child.logfile_read = fout

    child.expect('>')
    child.sendline('lcd '+apdir+'\r')
    index = child.expect(["lcd ok".encode('utf8'), pexpect.EOF, pexpect.TIMEOUT])
    if (index == 0):
        # time.sleep(5)
        nodeafile=configfile[nodename.upper()]['dumpa']
        nodebfile = configfile[nodename.upper()]['dumpb']
        child.sendline('mirror /ftpvol/relfsw0/ '+cpdir+'\r')
        # child.sendline('ls\r')
        index = child.expect(["transferred".encode('utf8'), pexpect.EOF, pexpect.TIMEOUT], timeout=3600)
        if (index == 0):
            time.sleep(5)
            child.sendline('pget /images/nodea/'+nodeafile + '\r')
            index = child.expect(["transferred".encode('utf8'),"The system cannot find the file specified", pexpect.EOF, pexpect.TIMEOUT], timeout=3600)
            if (index == 0):
                time.sleep(5)
                child.sendline('pget /images/nodeb/' + nodebfile + '\r')
                index = child.expect(["transferred".encode('utf8'), pexpect.EOF, pexpect.TIMEOUT], timeout=3600)
                if (index == 0):
                    child.close(force=True)
                    logfile.info(nodename+'ftpdump successed')

                else:
                    logfile.info(nodename + 'ftpdump not successed')
                    child.close(force=True)

            elif(index==1):

                time.sleep(5)
                child.sendline('pget /images/nodeb/' + nodeafile + '\r')
                index = child.expect(["transferred".encode('utf8'), pexpect.EOF, pexpect.TIMEOUT], timeout=3600)
                if (index == 0):
                    time.sleep(5)
                    child.sendline('pget /images/nodea/' + nodebfile + '\r')
                    index = child.expect(["transferred".encode('utf8'), pexpect.EOF, pexpect.TIMEOUT], timeout=3600)
                    if (index == 0):
                        child.close(force=True)
                        logfile.info(nodename + 'ftpdump successed')

                    else:
                        logfile.info(nodename + 'ftpdump not successed')
                        child.close(force=True)


                else:
                    logfile.info(nodename + 'ftpdump not successed')
                    child.close(force=True)


            else:
                logfile.info(nodename + 'ftpdump not successed')
                child.close(force=True)


        else:
            logfile.info(nodename+'ftpdump not successed')
            child.close(force=True)



    else:
        logfile.info(nodename+'ftpdump not successed')
        child.close(force=True)
    return



def ftpap2dump(nodename,ip,username,password,fout,logfile,dumpdir,configfile):
    child = pexpect.spawn('lftp ' + username + ':' + password + '@' + ip)
    loginprompt = '/>'

    apdir = dumpdir + '/apdump/'

    child.logfile_read = fout

    child.expect('>')
    child.sendline('lcd ' + apdir + '\r')
    index = child.expect(["lcd ok".encode('utf8'), pexpect.EOF, pexpect.TIMEOUT])
    if (index == 0):
        nodeafile = configfile[nodename.upper()]['dumpa']
        nodebfile = configfile[nodename.upper()]['dumpb']
        child.sendline('pget /images/nodea/' + nodeafile + '\r')
        index = child.expect(["transferred".encode('utf8'), "The system cannot find the file specified", pexpect.EOF, pexpect.TIMEOUT],timeout=3600)
        if (index == 0):
            time.sleep(5)
            child.sendline('pget /images/nodeb/' + nodebfile + '\r')
            index = child.expect(["transferred".encode('utf8'), pexpect.EOF, pexpect.TIMEOUT], timeout=3600)
            if (index == 0):
                child.close(force=True)
                logfile.info(nodename + 'ftpdump successed')
            else:
                logfile.info(nodename + 'ftpdump not successed')
                child.close(force=True)
        elif (index == 1):
            time.sleep(5)
            child.sendline('pget /images/nodeb/' + nodeafile + '\r')
            index = child.expect(["transferred".encode('utf8'), pexpect.EOF, pexpect.TIMEOUT], timeout=3600)
            if (index == 0):
                time.sleep(5)
                child.sendline('pget /images/nodea/' + nodebfile + '\r')
                index = child.expect(["transferred".encode('utf8'), pexpect.EOF, pexpect.TIMEOUT], timeout=3600)
                if (index == 0):
                    child.close(force=True)
                    logfile.info(nodename + 'ftpdump successed')
                else:
                    logfile.info(nodename + 'ftpdump not successed')
                    child.close(force=True)

            else:
                logfile.info(nodename + 'ftpdump not successed')
                child.close(force=True)

        else:
            logfile.info(nodename + 'ftpdump not successed')
            child.close(force=True)

    else:
        logfile.info(nodename + 'ftpdump not successed')
        child.close(force=True)

    return

def getMd5(filename): #计算md5
    mdfive = md5()
    with open(filename, 'rb') as f:
        mdfive.update(f.read())
    return mdfive.hexdigest()

def getSha1(filename): #计算sha1
    sha1Obj = sha1()
    with open(filename, 'rb') as f:
        sha1Obj.update(f.read())
    return sha1Obj.hexdigest()

def getCrc32(filename): #计算crc32
    with open(filename, 'rb') as f:
        return crc32(f.read())


def checkmd5(mgwdir,md5filerecord):
    dirlist = os.listdir(mgwdir + '/d/configuration/cv/')

    for item in dirlist:
        if item.find('Au_CX') != -1:
            md5dir = item
            break


    md5file = open(mgwdir + '/d/configuration/cv/' + md5dir + '/md5checksums', 'r')
    for line in md5file:
        otherfile=line.split()

        if otherfile[1]==getMd5(mgwdir + '/d/configuration/cv/' + md5dir + '/'+otherfile[0]):
            md5filerecord.writelines('文件: '+mgwdir + '/d/configuration/cv/' + md5dir + '/'+otherfile[0]+"\n")
            md5filerecord.writelines('大小:'+str(os.path.getsize(mgwdir + '/d/configuration/cv/' + md5dir + '/'+otherfile[0]))+'字节'+"\n")

            ctime = datetime.datetime.fromtimestamp((os.path.getmtime(mgwdir + '/d/configuration/cv/' + md5dir + '/' + otherfile[0])))
            mtime= ctime.strftime("%Y年%d月%d日, %H:%M:%S")
            md5filerecord.writelines('修改时间:' + mtime+"\n")

            md5filerecord.writelines('MD5:' +getMd5(mgwdir + '/d/configuration/cv/' + md5dir + '/'+otherfile[0])+"\n")
            md5filerecord.writelines('SHA1:' + getSha1(mgwdir + '/d/configuration/cv/' + md5dir + '/' + otherfile[0])+"\n")
            md5filerecord.writelines('CRC32:' + str(getCrc32(mgwdir + '/d/configuration/cv/' + md5dir + '/' + otherfile[0]))+"\n")

            md5filerecord.writelines("\n")

    return



def ftpmgwdump(nodename,ip,username,password,fout,logfile,dumpdir,md5file):

    child = pexpect.spawn('lftp ' + username+':'+password+'@'+ip)
    loginprompt = '/>'
    mgwdir=dumpdir+'/mgwdump/'+nodename
    os.mkdir(mgwdir)


    child.logfile_read = fout

    child.expect('>')
    child.sendline('ls\r')
    index = child.expect([loginprompt, pexpect.EOF, pexpect.TIMEOUT])
    if (index == 0):
        # time.sleep(5)
        child.sendline('mirror / '+mgwdir+'\r')
        index = child.expect(["transferred".encode('utf8'), pexpect.EOF, pexpect.TIMEOUT], timeout=3600)
        if (index == 0):
            time.sleep(5)




            child.close(force=True)
            logfile.info(nodename+'ftpdump successed')
        else:
            logfile.info(nodename+'ftpdump not successed')
            child.close(force=True)
    else:
        logfile.info(nodename+'ftpdump not successed')
        child.close(force=True)



    checkmd5(dumpdir + '/mgwdump/'+nodename, md5file)
    return


def FileSize(path):
  size = 0
  for root , dirs, files in os.walk(path, True):
    size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    #目录下文件大小累加
    return size






