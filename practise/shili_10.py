"""
题目：暂停一秒输出，并格式化当前时间。
"""

import time
# now_time = time.localtime(time.time())


while True:
    now_time = time.strftime('%Y-%m-%d %H:%M:%S ', time.localtime(time.time()))
    print(now_time)
    time.sleep(2)

