# coding = utf-8
import codecs
import os
import configparser

proPath = os.path.split(os.path.realpath(__file__))[0]
# common_path = os.path.join(proPath, 'common')
result_path = os.path.join(proPath, 'result')
config_path = os.path.join(proPath, 'config.ini')


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

    def geturl(self, name):
        value = self.cp.get('http', name)
        # print(value)
        return value



if __name__ == '__main__':
    rc = ReadConfig()
    rc.geturl('host')
