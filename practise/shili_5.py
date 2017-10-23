"""
题目：输入三个整数x,y,z，请把这三个数由小到大输出。
使用序列[]的sort()
"""

xulie = []
for i in range(3):
    i = int(input('请输入整数：'))
    xulie.append(i)
print(xulie)

# xulie.sort()
result = sorted(xulie)
print(result)


