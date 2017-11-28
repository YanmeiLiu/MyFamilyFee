#coding = utf-8

import logging
import threading
import  time

import os

import readConfig


class Log(object):

    def __init__(self):
        global log_path, result_path
        proPath = readConfig.proPath

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)

        log_path = os.path.join(proPath, 'log')
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        dt = time.strftime('%Y%m%d%H%M%S',time.localtime())
        fh = logging.FileHandler(os.path.join(log_path,dt+'.log'))
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s] [%(lineno)d] [%(levelname)s] [%(filename)s] [%(message)s]')

        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        self.logger.addHandler(sh)
        self.logger.addHandler(fh)


class MyLog(threading.Thread):
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log(self):

        if MyLog.log is None :
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log