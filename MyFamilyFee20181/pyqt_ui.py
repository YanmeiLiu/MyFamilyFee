import csv
import sys

import time

import os
from PyQt4 import QtGui, QtCore
import logger

import mysqloption

lg = logger.config_logger('Example')


class Example(QtGui.QMainWindow):
    global pbar, button_import

    def __init__(self):
        super(Example, self).__init__()

        # 设置大小
        self.setGeometry(300, 100, 700, 500)
        self.setWindowTitle('家庭收支理财小工具')

        # 连接数据库
        self.db, self.cur = mysqloption.connDB()
        self.initUI()
        self.searchGrid()
        # self.dataGrid()
        # self.showDialog()

    def initUI(self):
        # 新增选项
        createnew = QtGui.QAction('新增', self)
        createnew.setShortcut('Ctrl+N')
        createnew.setStatusTip('新增支出/收入')
        createnew.triggered.connect(self.create_new)
        # 导出数据
        exportdata = QtGui.QAction('导出', self)
        exportdata.setShortcut('')
        exportdata.setStatusTip('导出数据到csv文件')
        exportdata.triggered.connect(self.export_data)

        # 导入csv文件中数据
        importdata = QtGui.QAction('导入', self)
        importdata.setShortcut('')
        importdata.setStatusTip('导入csv文件中数据到数据库')
        importdata.triggered.connect(self.import_data)

        exitAction = QtGui.QAction('退出', self)  # 图标设置QtGui.QIcon('exit24.png')
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('退出程序')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        fileMenu.addAction(createnew)
        fileMenu.addAction(exportdata)
        fileMenu.addAction(importdata)
        fileMenu.addAction(exitAction)

        helpMenu = menubar.addMenu('帮助')

        toolbar = self.addToolBar('退出')
        toolbar.addAction(exitAction)

    def searchGrid(self):
        self.widget = QtGui.QWidget(self)
        # 水平布局
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)

        # 垂直布局
        self.horizontalLayout = QtGui.QHBoxLayout()

        self.name_label = QtGui.QLabel('姓名：')
        userlist = mysqloption.selectuser(self.cur)
        print(userlist)
        namelist = ['全部']

        for user in userlist:
            name = user[1]
            namelist.append(name)

        self.name_comboBox = QtGui.QComboBox()
        self.name_comboBox.addItems(namelist)

        self.horizontalLayout.addWidget(self.name_label)
        self.horizontalLayout.addWidget(self.name_comboBox)

        self.shouzhi_label = QtGui.QLabel('收支：', self.widget)
        self.shouzhi_radio1 = QtGui.QRadioButton('支出')
        self.shouzhi_radio2 = QtGui.QRadioButton('收入')
        self.horizontalLayout.addWidget(self.shouzhi_label)
        self.horizontalLayout.addWidget(self.shouzhi_radio1)
        self.horizontalLayout.addWidget(self.shouzhi_radio2)

        self.time_label = QtGui.QLabel('时间：')
        self.time_edit1 = QtGui.QLineEdit()
        self.time_edit2 = QtGui.QLineEdit()

        self.horizontalLayout.addWidget(self.time_label)
        self.horizontalLayout.addWidget(self.time_edit1)
        self.horizontalLayout.addWidget(self.time_edit2)

        self.search_button = QtGui.QPushButton('查询')
        self.search_button.clicked.connect(self.search_event)
        self.horizontalLayout.addWidget(self.search_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # 添加表头

        self.table = QtGui.QTableWidget(self.widget)
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        headerlabels = ['id', '收支', '姓名', '用途', '金额', '支付方式', '时间']
        self.table.setColumnCount(len(headerlabels))

        column_width = [60, 70, 80, 150, 60, 80, 160]
        for column in range(len(headerlabels)):
            self.table.setColumnWidth(column, column_width[column])

        self.table.setHorizontalHeaderLabels(headerlabels)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.verticalLayout.addWidget(self.table)
        result = mysqloption.search_data(self.cur)
        self.get_data(result)
        self.setCentralWidget(self.widget)

        # 添加表项

    def get_data(self, results):

        if len(results) == 0:
            self.table.setRowCount(2)
            self.led = QtGui.QLineEdit('暂无查询数据，请先添加！！')
            tishiyu = QtGui.QTableWidgetItem(self.led.text())
            self.table.setItem(1, 3, tishiyu)
        self.current_row = len(results)

        self.table.setRowCount(len(results))
        for i in range(len(results)):
            id = QtGui.QTableWidgetItem(str(i + 1))
            self.table.setItem(i, 0, id)
            shouzhi = QtGui.QTableWidgetItem(results[i]['shouzhi'])
            self.table.setItem(i, 1, shouzhi)
            name = QtGui.QTableWidgetItem(results[i]['name'])
            self.table.setItem(i, 2, name)
            product_name = QtGui.QTableWidgetItem(results[i]['product_name'])
            self.table.setItem(i, 3, product_name)

            money = QtGui.QTableWidgetItem(str(results[i]['money']))
            self.table.setItem(i, 4, money)

            payname = QtGui.QTableWidgetItem(results[i]['payname'])
            self.table.setItem(i, 5, payname)

            createtime_str = results[i]['createtime'].strftime("%Y-%m-%d %H:%M:%S")
            createtime = QtGui.QTableWidgetItem(createtime_str)
            # print(createtime)
            self.table.setItem(i, 6, createtime)

    def create_new(self):  # 新增数据

        data = self.showDialog()
        # print(data)
        # if data[0]:
        #     self.current_row += 1
        #
        #     self.table.insertRow(self.current_row-1)
        #     #   shouzhi,user_id,  product_name,money,payment_id, createtime

    def showhint(self):
        data = self.showDialog()
        print('data:' + data)
        hint_msg = QtGui.QMessageBox(self)
        hint_msg.setWindowTitle('警告')
        # hint_msg.setButtonText(hint_msg.Yes,QString("确定"))
        if data[0] != 1 and data[0] != 2:
            print('shouzhi：' + data[0])

            hint_msg.setText('收入or支出 请务必选择一个！')
            hint_msg.setStandardButtons(hint_msg.Yes)
            hint_msg.exec_()
        elif data[1] == '' or data[1] is None:

            hint_msg.setText('姓名未填写，请重新输入')
            hint_msg.setStandardButtons(hint_msg.Yes)
            hint_msg.exec_()
        elif data[2] == '' or data[2] is None:

            hint_msg.setText('用途未填写，请重新输入')
            hint_msg.setStandardButtons(hint_msg.Yes)
        elif data[3] == '' or data[3] is None:

            hint_msg.setText('金额未填写，请重新输入')
            hint_msg.setStandardButtons(hint_msg.Yes)
        elif data[4] == '' or data[4] is None:

            hint_msg.setText('支付方式未填写，请重新输入')
            hint_msg.setStandardButtons(hint_msg.Yes)
        elif data[5] == '' or data[5] is None:

            hint_msg.setText('时间未填写，请重新输入')
            hint_msg.setStandardButtons(hint_msg.Yes)

        else:
            pass

    def search_event(self):
        sender = self.sender()
        self.statusBar().showMessage('查询')
        name = self.name_comboBox.currentText()
        # print('name:' + name)
        shouzhi = ''
        if self.shouzhi_radio1.isChecked():
            shouzhi = '支出'
        elif self.shouzhi_radio2.isChecked():
            shouzhi = '收入'
        createtime1 = self.time_edit1.text()
        createtime2 = self.time_edit2.text()
        # print('shouzhi:' + shouzhi)
        print('paytime1:%s,paytime2:%s'%(createtime1,createtime2))
        result = mysqloption.search_data(self.cur, name, shouzhi,createtime1,createtime2)
        self.get_data(result)
        # print('result:'+result)

    def export_data(self):  # 导出数据到csv文件
        pass

    def import_data(self):  # 导入csv文件
        import_dialog = QtGui.QDialog(self)


        import_dialog.resize(380, 150)
        import_dialog.setWindowTitle('准备导入数据到数据库中')
        file_dialog = QtGui.QFileDialog()
        filepath1 = os.path.split(os.getcwd())[0]
        filename = file_dialog.getOpenFileName(self, '打开', filepath1)
        # 垂直盒子
        verticalLayout = QtGui.QVBoxLayout(import_dialog)

        # 水平盒子
        horizontalLayout = QtGui.QHBoxLayout(import_dialog)

        import_btn = QtGui.QPushButton('选择文件', import_dialog)
        import_btn.clicked.connect(file_dialog.getOpenFileName)
        filename_text = QtGui.QLineEdit(import_dialog)

        import_ok = QtGui.QPushButton('确认导入', import_dialog)
        import_ok.clicked.connect(self.doAction)

        pbar = QtGui.QProgressBar(import_dialog)

        horizontalLayout.addWidget(import_btn)
        horizontalLayout.addWidget(filename_text)
        horizontalLayout.addWidget(import_ok)
        verticalLayout.addLayout(horizontalLayout)

        verticalLayout.addWidget(pbar)


        filename_text.setText(filename)

        # sta = self.importtodb(filename)
        # if sta == 1:
        #     print('添加成功！')
        # if sta == 0:
        #     print('添加失败，请检查')
        import_dialog.exec_()

    def doAction(self):
        # 采用定时器激活进度条
        self.timer = QtCore.QBasicTimer()
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    # def openfile(self, filename=''):
    #
    #     file_dialog = QtGui.QFileDialog()
    #     filepath1 = os.path.split(os.getcwd())[0]
    #     filename = file_dialog.getOpenFileName(self, '打开', filepath1)
    #
    #     return filename

    def importtodb(self, filename):
        step = 0

        with open(filename) as f:
            f_csv = csv.reader(f)
            print('f_csv长度:' + len(f_csv))
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

                sta = mysqloption.insertsqlfrom_zhifubao(self.cur, self.db, user_id, payment_id,
                                                         jiaoyi_num, shanghudingdan_num, createtime, pay_time,
                                                         edit_time, jiaoyilaiyuan, jiaoyileixing, jiaoyiduifang,
                                                         product_name,
                                                         money, shouzhi, remark, zijinzhuangtai)
                step = step + 1
            if step >= 100:
                self.timer.stop()
                self.import_data.button_import.setText('已完成')
                return

            self.import_data.pbar.setValue(step)

    def import_progress(self):
        self.pbar = QtGui.QProgressBar(self)

        self.pbar.setGeometry(30, 40, 200, 25)
        # self.connect(, QtCore.SIGNAL('clicked()'), self.import_data)

    def showDialog(self, shouzhi='', user_id='', product_name='', money='', payment_id='', createtime=''):
        self.edit_dialog = QtGui.QDialog(self)
        self.edit_dialog.resize(300, 300)
        group = QtGui.QGroupBox('编辑用户消费信息', self.edit_dialog)

        group_layout = QtGui.QGridLayout(self.edit_dialog)
        # 收支

        shouzhis = [('支出', 1), ('收入', 2)]

        for i, content in enumerate(shouzhis):
            shouzhi_radioButton = QtGui.QRadioButton(content[0], group)
            if shouzhi != '' and content[1] == shouzhi:
                print('shouzhi:' + shouzhi)
                # shouzhi_radioButton.setChecked(True)

            group_layout.addWidget(shouzhi_radioButton, 1, i)

        # 姓名
        name_label = QtGui.QLabel('姓名:', group)
        name_comboBox = QtGui.QComboBox()
        userlist = mysqloption.selectuser(self.cur)
        namelist = ['']
        for i, user in enumerate(userlist):
            name_data = user[1]
            namelist.append(name_data)

        name_comboBox.addItems(namelist)
        # 设置默认项
        for i, user in enumerate(userlist):
            if user[0] == user_id:
                name_comboBox.setCurrentIndex(i)

        group_layout.addWidget(name_label, 2, 0)
        group_layout.addWidget(name_comboBox, 2, 1)

        # 用途输入框
        product_name_label = QtGui.QLabel('用途:', group)
        product_name_line = QtGui.QLineEdit(group)
        product_name_line.setText(product_name)
        group_layout.addWidget(product_name_label, 3, 0)
        group_layout.addWidget(product_name_line, 3, 1)
        # 金额
        money_label = QtGui.QLabel('金额:', group)
        money_line = QtGui.QLineEdit(group)
        money_line.setText(money)
        group_layout.addWidget(money_label, 4, 0)
        group_layout.addWidget(money_line, 4, 1)
        # 支付方式
        payname_label = QtGui.QLabel('支付方式:', group)
        paynamelist = mysqloption.selectpayment(self.cur)
        paylist = ['']
        for pay in paynamelist:
            payname_data = pay[1]
            paylist.append(payname_data)

        payname_comboBox = QtGui.QComboBox()
        payname_comboBox.addItems(paylist)
        # 设置默认项
        for i, pay in enumerate(paynamelist):

            if pay[0] == payment_id:
                payname_comboBox.setCurrentIndex(i)

        group_layout.addWidget(payname_label, 5, 0)
        group_layout.addWidget(payname_comboBox, 5, 1)

        # 时间
        createtime_label = QtGui.QLabel('时间:', group)
        createtime_line = QtGui.QLineEdit(group)
        createtime_line.setText(createtime)
        group_layout.addWidget(createtime_label, 6, 0)
        group_layout.addWidget(createtime_line, 6, 1)

        ok_button = QtGui.QPushButton('提交', self.edit_dialog)
        cancel_button = QtGui.QPushButton('取消', self.edit_dialog)

        ok_button.clicked.connect(self.showhint)
        ok_button.setDefault(True)
        cancel_button.clicked.connect(self.edit_dialog.reject)

        group.setLayout(group_layout)
        # group.setFixedSize(group.sizeHint())

        button_layout = QtGui.QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        dialog_layout = QtGui.QVBoxLayout()
        dialog_layout.addWidget(group)
        dialog_layout.addLayout(button_layout)
        self.edit_dialog.setLayout(dialog_layout)
        self.edit_dialog.setWindowTitle('')
        # edit_dialog.setFixedSize(edit_dialog.sizeHint())
        if self.edit_dialog.exec_():
            shouzhi_text = shouzhi_radioButton.text()
            print(shouzhi_text)

            for content in shouzhis:
                if content[0] == shouzhi_text:
                    shouzhi = content[1]

            name = name_comboBox.currentText()
            for user in userlist:
                if user[1] == name:
                    user_id = user[0]
            payname = payname_comboBox.currentText()
            for pay in paynamelist:
                if pay[1] == payname:
                    payment_id = pay[0]

            product_name = product_name_line.text()
            money = money_line.text()

            createtime = createtime_line.text()
            print(' shouzhi:%s,user_id:%s,  product_name:%s,money:%s,payment_id:%s, createtime:%s'
                  % (shouzhi, user_id, product_name, money, payment_id, createtime))
            return shouzhi, user_id, product_name, money, payment_id, createtime
        return None, None, None, None, None, None


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
