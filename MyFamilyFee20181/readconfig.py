# coding = utf-8

# date :2017.12.8
# user :liuyanmei

# explain :从config.ini文件中读取数据

import codecs
import configparser

import time
import os


#以下是文件的存储文件夹
work_path = os.getcwd()
proPath=os.path.abspath(work_path)
print(proPath)

config_path = os.path.join('D:\study\MyFamilyFee20181', 'config.ini')
caseresult_path =os.path.join(proPath,'caseresult_path')
os.path.join(proPath,'log')

log_path = os.path.join(proPath,'log')
if not os.path.exists(log_path):
    os.mkdir(log_path)
if not os.path.exists(caseresult_path):
    os.mkdir(caseresult_path)

#以下是文件的文件名，不包括后缀
filename = time.strftime('%Y%m%d-%H%M%S',time.localtime())


class ReadConfig(object):
    def __init__(self):
        """
        打开配置文件，读取其中的数据放到data中，因为txt文件的前三行是bom，要去掉，
        然后以二进制的格式 以write方式打开文件，写入数据，
        """
        fd = open(config_path)
        data = fd.read()

        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(config_path, 'w')
            file.write(data)
            file.close()
        fd.close()

        self.cp = configparser.ConfigParser()
        self.cp.read(config_path)

    def get_mysql(self, name):
        value = self.cp.get('mysql', name)
        return value
