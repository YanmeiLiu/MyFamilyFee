"""
题目：将一个正整数分解质因数。例如：输入90,打印出90=2*3*3*5。
"""
from math import sqrt

num = 256
x = input('是否开始？是：1，否：0\n')
while(x):
    num = int(input('请输入一个整数：'))
    for i in range(2, num + 1):
        if num % i == 0:
            print(i)
            num = num / i





