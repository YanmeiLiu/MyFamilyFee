# coding = utf-8
# author : liuyanmei
# date : 2018-1-2

import pymysql

import readconfig
import logger


def connDB():  # 连接数据库
    lg = logger.config_logger('connDB')
    lg.info('开始连接数据库')
    rc = readconfig.ReadConfig()

    host = rc.get_mysql('host')
    port = int(rc.get_mysql('port'))
    user = rc.get_mysql('user')
    password = rc.get_mysql('password')
    database = rc.get_mysql('db')
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, db=database, charset='utf8')
        lg.info('已成功连接数据库')
    except Exception as e:
        print(e)
        lg.info('数据库访问失败')

    cur = conn.cursor()
    return (conn, cur)


def insert_sql(cur, conn, shouzhi, user_id, product_name, money, payment_id, createtime):
    lg = logger.config_logger('insert_sql')
    lg.info('准备插入数据')
    sql = "insert into pay_info(shouzhi,user_id,  product_name,money,payment_id, createtime) values('%d','%d','%s','%s','%s','%s')" % (
        shouzhi, user_id, product_name, money, payment_id, createtime)
    try:
        sta = cur.execute(sql)
        conn.commit()
        lg.info('数据已入库')
    except:
        conn.rollback()
    return sta


# 导入支付宝数据
def insertsqlfrom_zhifubao(cur, conn, user_id, payment_id,
                           jiaoyi_num, shanghudingdan_num, createtime, pay_time,
                           edit_time, jiaoyilaiyuan, jiaoyileixing, jiaoyiduifang,product_name,
                            money, shouzhi, remark, zijinzhuangtai):
    aa = 0
    lg = logger.config_logger('insertsqlfrom_zhifubao')
    lg.info('准备插入数据')
    sql_zhifubao = "insert into pay_info(user_id,payment_id,jiaoyi_num,shanghudingdan_num, createtime , " \
                   "pay_time ,edit_time ,jiaoyilaiyuan ,jiaoyileixing ,jiaoyiduifang ," \
                   "product_name ,money  ,shouzhi  ,remark,zijinzhuangtai) " \
                   "values('%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                   % (user_id, payment_id, jiaoyi_num, shanghudingdan_num, createtime, pay_time, edit_time,
                      jiaoyilaiyuan, jiaoyileixing, jiaoyiduifang,product_name, money, shouzhi, remark, zijinzhuangtai)
    try:
        aa = cur.execute(sql_zhifubao)
        print(aa)
        conn.commit()
        lg.info('数据已入库')
    except:
        conn.rollback()
    return aa


# 根据查询条件（姓名、收支）查询数据
def search_data(cur, name='', shouzhi=''):
    lg = logger.config_logger('search_data')
    lg.info('准备查询数据')
    sql = "SELECT u.name ,p.payname,pay.product_name,pay.createtime,pay.money ,pay.shouzhi as '收支'\
       FROM user_info u,payment_info p, pay_info pay \
       WHERE u.id=pay.user_id AND p.id=pay.payment_id "
    i = 1
    if name != '' and name != '全部':
        sql = sql + "and u.name='%s'" % (name)
        i = 0

    if shouzhi != '':
        if i == 0:
            sql = sql + "and pay.shouzhi='%s'" % (shouzhi)
            i = 0
        else:
            sql = sql + "and pay.shouzhi='%s';" % (shouzhi)
            i = 1

    lg.info(sql)
    try:
        cur.execute(sql)
        fet_results = cur.fetchall()

        results = []

        for row in fet_results:

            result = {'name': row[0], \
                      'payname': row[1], \
                      'product_name': row[2], \
                      'createtime': row[3], \
                      'money': row[4], \
                      'shouzhi': row[5], \
                      }
            if result['shouzhi'] == 1:
                result['shouzhi'] = '支出'
            if result['shouzhi'] == 2:
                result['shouzhi'] = '收入'
            results.append(result)

        lg.info('查询完数据')

    except:
        import traceback
        traceback.print_exc()
        print("Error :unable to fetchall data")
    return results


def selectuser(cur):
    sql = "SELECT * FROM user_info ;"
    # user_name = []
    try:
        cur.execute(sql)
        users = cur.fetchall()

    except:
        import traceback
        traceback.print_exc()
        print("Error :unable to fetchall data")

    return users


def selectuserbyname(cur, name):
    sql = "SELECT id FROM user_info where name ='%s'" % name
    try:
        cur.execute(sql)
        datas = cur.fetchall()
        for data in datas:
            id = data[0]


    except:
        import traceback
        traceback.print_exc()
        print("Error :unable to fetchall data")

    return id


def selectpayment(cur):
    sql = "SELECT * FROM payment_info ;"
    # payment_list = []
    try:
        cur.execute(sql)
        payments = cur.fetchall()

    except:
        import traceback
        traceback.print_exc()
        print("Error :unable to fetchall data")

    return payments


def update_sql():
    pass


def connClose(conn, cur):  # 关闭所有连接
    cur.close()
    conn.close()
    lg = logger.config_logger('connClose')
    lg.info('断开与数据库的连接')


if __name__ == '__main__':
    conn, cur = connDB()
    # myp.insert_sql()
    # hh = select_sql(cur)
    # print(hh)
    # print(selectuser(cur))
    # print(selectpayment(cur))
    # id = selectuserbyname(cur, name='刘艳美')
    #
    # user_id = 1
    # payment_id = 1
    # product_name = 'tre'
    # createtime = '2018-1-3'
    # money = 12
    # shouzhi = 2
    # insert_sql(cur, conn, user_id, payment_id, product_name, createtime, money, shouzhi)
    # # print(type(id))
    # connClose(conn, cur)
    name = '刘艳美'
    shouzhi = 1
    resu = search_data(cur, name, shouzhi)
    print(len(resu))
