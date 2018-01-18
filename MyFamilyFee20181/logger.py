#coding = utf8

import logging

import time


import readconfig
import logging.handlers

loggers = {}

# 日志文件
import os


def get_logger(name, **kwargs):
    global loggers
    # import pdb
    # pdb.set_trace()
    if loggers.get(name):
        return loggers.get(name)
    else:
        return config_logger(name, kwargs)

def config_logger(name):
    global loggers
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # 路径
    log_path = readconfig.log_path

    datetime = time.strftime('%Y-%m-%d', time.localtime())
    # print(datetime)
    file_path = os.path.join(log_path,'%s'%datetime)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    # name = 'log.log'
    file_name = os.path.join(file_path, '%s.log'%name)
    #输出到日志文件的格式
    formatter = logging.Formatter("%(asctime)s / %(name)s / %(levelname)s / %(message)s")
    #回滚日志设置
    rfh = logging.handlers.RotatingFileHandler(file_name,'a',1024*1024,10,'utf-8')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    rfh.setFormatter(formatter)
    logger.addHandler(rfh)
    logger.addHandler(sh)
    loggers[name] = logger
    return logger


# if __name__ == '__main__':
#     config_logger('makeupparams')