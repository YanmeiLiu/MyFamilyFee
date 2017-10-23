"""
题目：输入某年某月某日，判断这一天是这一年的第几天？
程序分析：以3月5日为例，应该先把前两个月的加起来，然后再加上5天即本年的第几天
特殊情况，闰年且输入月份大于2时需考虑多加一天：
"""


# 先判断闰年



def IsRunNian(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 100 == 0 and year % 400 == 0):
        print('%s是闰年！' % year)
        return True
    else:
        print('%s不是闰年！' % year)


def IsNum(ymd):

    y, m, d = (int(y) for y in ymd.split('-'))
    sum_day = 0
    # print(y, m, d)
    dict_1 = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if IsRunNian(y):
        for i in range(1, m):
            sum_day = sum_day+dict_1[i]
        total_day = sum_day+d+1
        print('%s是%d的第%d天' % (ymd, y, total_day))

    else:
        for i in range(1, m):
            sum_day = sum_day + dict_1[i]
        total_day = sum_day + d
        print('%s是%d的第%d天' % (ymd, y, total_day))



if __name__ == '__main__':
    ymd = input('请您输入年月日（参照格式yyyy-mm-dd）:')
    IsNum(ymd)

