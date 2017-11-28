# coding = utf-8
import readConfig
from common import optionexcel, getresponse, zuhecase


class RunAll(object):
    def __init__(self):
        pass

    def funRun(self):
        # 读取测试用例，用例中有名称，参数，期望值
        fileName = zuhecase.CreateExcel()

        # fileName = 'yk_test.xlsx'
        oe = optionexcel.OptionExcel(fileName)
        caselist = oe.getExcelData(oe.excelFile)
        exceldatalist = oe.getParams(oe.excelFile)  # 返回的是[{}]
        for case in caselist:
            caseID = case['id']
            caseexpect = case['expect']
            param = {}
            param['business'] = case['business']
            param['is_iqiyi'] = case['is_iqiyi']
            param['is_video_page'] = case['is_video_page']
            param['categoryid'] = case['categoryid']
            param['qypid'] = case['qypid']
            print('runall第%d条用例开始执行'%caseID)

            rc = readConfig.ReadConfig()
            host = rc.geturl('host')
            proxies = {'http': host}
            url = rc.geturl('url')




            gp = getresponse.GetResponse()

            dp = gp.download(url,proxies,param)
            #去除空格
            dp_s = dp.strip()

            if caseexpect == dp_s:
                theresult = u'通过'

            else:
                theresult = u'未通过'

            # 将结果写回到excel文件中

            oe.writeExcel(oe.excelFile, theresult, dp, caseID)

if __name__ == '__main__':
    zhixing = RunAll()
    zhixing.funRun()
