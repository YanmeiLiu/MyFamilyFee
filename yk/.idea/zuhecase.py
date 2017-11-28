# coding = utf-8

import openpyxl
business = ['video_cutlimit','toutiaofeed']
is_iqiyi = ['true','false']
is_video_page = ['true','false']
categoryid = [1,2]
qypid = ['02023221010000000000']
#统计有多少种组合
blen = len(business)
ilen = len(is_iqiyi)
vlen = len(is_video_page)
clen = len(categoryid)
qlen = len(qypid)
case_num = blen*ilen*vlen*clen*qlen
print('总共有%d条测试用例'%(case_num))


lw = openpyxl.load_workbook('yk_test.xlsx')
sheet = lw.get_sheet_by_index(3)

for n in range(1,case_num):
    for b in business:
        # print('business=%s'%b)
        for i in is_iqiyi:
            # print('is_iqiyi=%s'%i)
            for v in is_video_page:
                # print('is_video_page=%s'%v)
                for c in categoryid:
                    # print('categoryid=%s'%c)
                    for q in qypid:
                        # print('qypid=%s'%q)
                        params = {
                            'business': b, \
                            'is_iqiyi': i, \
                            'is_video_page': v, \
                            'categoryid': c, \
                            'qypid': q}
                        print(params)
                        cs.cell(n, 1).value = params
                        print('write success')

lw.save('lw.xlsx')





