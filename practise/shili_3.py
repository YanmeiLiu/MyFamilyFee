"""
题目：一个整数，它加上100后是一个完全平方数，再加上168又是一个完全平方数，请问该数是多少？
1、x+100 = n*n n*n+168 = m*m  求出m和n就能知道x的值 x = n*n-100 = m*m-168-n*n
2、m*m - n*n = 168
3、（m+n）*（m-n）=168  因为结果是偶数，那么至少其中一个数是偶数，不可能全是奇数
4、i=m+n j=m-n
5、m=(i+j)/2  n=(i-j)/2  推导出：i和j 不可能一奇数一偶数，因为m和n是整数
6、根据3和5 得出i和j都是偶数，大于等于2，j大于等于2，那么i的取值范围就是 range(2,168/2+1)
"""
for i in range(2,85):
    for j in range(2,85):
        chengji = i*j
        if chengji == 168 and i > j and i%2 ==0 and (i+j)%2 ==0 and (i-j)%2 ==0 :
            # print(i,j)
            m = (i+j)/2
            n = (i-j)/2
            # tmp = (m,n)

            x = n*n - 100
            print("这个数可能是：%d"%x)
            print('(m,n)的取值是(%d,%d)' % (m, n))

