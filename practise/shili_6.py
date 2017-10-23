"""
题目：斐波那契数列。
斐波那契数列（Fibonacci sequence），又称黄金分割数列，
指的是这样一个数列：0、1、1、2、3、5、8、13、21、34、……。
"""

def Fun(n):
    a,b = 0,1

    for i in range(n-1):
        a,b = b,a+b

    return a

if __name__ == '__main__':
    print(Fun(10))
