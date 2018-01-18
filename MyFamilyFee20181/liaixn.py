
import csv

import os

import mysqloption

filepath1 = os.path.split(os.getcwd())[0]
filepath2 = os.path.split(os.getcwd())[1]
filepath = os.path.join(filepath1, filepath2)
filename = os.path.join(filepath, 'zfb-python1.csv')

print(filename)
# 连接数据库
db,cur = mysqloption.connDB()

with open(filename) as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    # print(headers)
    # ['交易号\商户订单号\交易创建时间\付款时间\最近修改时间\交易来源地\类型\交易对方\
    # 商品名称\金额（元）\收/支\交易状态\服务费（元）\成功退款（元）\备注\资金状态]

    for row in f_csv:
        jiaoyi_num = row[0]
        shanghudingdan_num = row[1]
        createtime = row[2]
        pay_time = row[3]
        edit_time = row[4]
        jiaoyilaiyuan = row[5]
        jiaoyileixing = row[6]
        jiaoyiduifang = row[7]
        product_name = row[8]
        money = row[9]
        shouzhi = row[10]
        remark = row[14]
        zijinzhuangtai = row[15]



        user_id = 1
        payment_id = 3
        print(user_id, payment_id,
                           jiaoyi_num, shanghudingdan_num, createtime, pay_time,
                           edit_time, jiaoyilaiyuan, jiaoyileixing, jiaoyiduifang,
                            money, shouzhi, remark, zijinzhuangtai)

        sta = mysqloption.insertsqlfrom_zhifubao(cur, db, user_id, payment_id,
                           jiaoyi_num, shanghudingdan_num, createtime, pay_time,
                           edit_time, jiaoyilaiyuan, jiaoyileixing, jiaoyiduifang,product_name,
                            money, shouzhi, remark, zijinzhuangtai)
        if sta == 1:
            print('添加成功！')
        if sta == 0:
            print('添加失败，请检查')



