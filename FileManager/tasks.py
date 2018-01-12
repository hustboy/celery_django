from filemanager.celery import app
import configparser
from filemanager.telnet import bscdump,gsap2dump,gsap1dump,ftpap1dump,ftpap2dump,ftpmgwdump,FileSize
from filemanager.dump import delbscfile,delgsfile
import logging
from django.conf import settings
import time,datetime
import os
import xlsxwriter
import pexpect

config=configparser.ConfigParser()

#DumpRecord.ini.ini可以是一个不存在的文件，意味着准备新建配置文件。
config.read("IpConfig.ini")
dumprecord=configparser.ConfigParser()

#DumpRecord.ini.ini可以是一个不存在的文件，意味着准备新建配置文件。
dumprecord.read("DumpRecord.ini")
LOG_DIR = os.path.join(settings.MEDIA_ROOT, "logs/")

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

@app.task
def add(x, y):
    logyy = Logger(LOG_DIR + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'dumplog.txt', logging.ERROR,
                    logging.DEBUG)
    logyy.info('一个info信息')
    # logyy.info(LOG_DIR + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'dumplog.txt')
    # print(LOG_DIR + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'dumplog.txt')
    #
    # fp=open(LOG_DIR + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'rrrr.txt', 'w')
    # fp.write('fdghjg')
    # fp.close()


    print(x, y)
    return x + y


@app.task
def deloldfile(x):
    deldump = Logger(LOG_DIR + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'deldumplog.txt', logging.ERROR,
                     logging.DEBUG)


    for key, value in bscip.items():
        delbscfile(key, value, bscusername, bscpassword,deldump,timeout=x)
    for key, value in gsap1ip.items():
        delgsfile(key, value, gsap1username, gsap1password,deldump,timeout=x)
    for key, value in gsap2ip.items():
        delgsfile(key, value, gsap2username, gsap2password,deldump,timeout=x)

    # delfile('BSC88', '10.26.2.36', 'wh1cx2', 'aqyqZBT#27', logdel)
    return x



@app.task
def dodump(x):
    logdump = Logger(LOG_DIR + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'dodumplog.txt', logging.ERROR,
                    logging.DEBUG)
    fout = open(LOG_DIR+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'log.txt', 'wb')

    for key, value in bscip.items():
        bscdump(key, value, bscusername, bscpassword, fout,logdump,dumprecord)
    for key, value in gsap1ip.items():
        gsap1dump(key, value, gsap1username, gsap1password,fout, logdump,dumprecord)
    for key, value in gsap2ip.items():
        gsap2dump(key, value, gsap2username, gsap2password, fout,logdump,dumprecord)

    # for key, value in bscip.items():
    #     if 'bsc88' in key:
    #         bscdump(key, value, bscusername, bscpassword, fout,logdump,dumprecord)
    fout.close()
    return x



@app.task
def ftpdump(x):
    logftp = Logger(LOG_DIR + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'ftpdumplog.txt', logging.ERROR,
                    logging.DEBUG)
    fout = open(LOG_DIR + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'log.txt', 'wb')
    dumpdir='/mnt/usb/'+'妙墩备份'+time.strftime("%Y%m%d", time.localtime())



    os.mkdir(dumpdir)
    os.mkdir(dumpdir+'/cpdump')
    os.mkdir(dumpdir + '/apdump')
    os.mkdir(dumpdir + '/mgwdump')

    for key, value in bscip.items():
        ftpap1dump(key, value, bscusername, bscpassword,fout,logftp,dumpdir,dumprecord)


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

        ftpap1dump(key, value, gsap1username, gsap1password,fout,logftp,dumpdir,dumprecord)
        cpfilesize = FileSize(dumpdir + '/cpdump/' + key[:6])
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

    for key, value in gsap2ip.items():
        ftpap2dump(key, value, gsap1username, gsap1password, fout, logftp, dumpdir, dumprecord)


    fp = open(dumpdir + '/mgwdump/md5check.txt', 'w')
    for key, value in gmip.items():
        ftpmgwdump(key, value, gmusername, gmpassword, fout, logftp, dumpdir,fp)
    fp.close()
    fout.close()
    return x





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





