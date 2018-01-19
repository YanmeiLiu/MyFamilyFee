# coding = utf-8

# author : liuyanmei

# date : 2018-1-2
import csv
import tkinter
import tkinter.ttk

import logger
import sys
import mysqloption
import tkinter.messagebox
import optionExcel
import tkinter.filedialog

lg = logger.config_logger('MainWindow')


class MainWindow(object):
    def __init__(self, width=680, height=300):
        self.width = width
        self.heigth = height

        self.root = tkinter.Tk()
        # 固定窗口的大小不可变
        self.root.resizable(width=False, height=False)
        self.root.title('家庭收支记账单')
        self.center()
        self.menu_data()
        # 连接数据库
        self.db, self.cur = mysqloption.connDB()
        self.initUI()
        self.root.mainloop()

    def initUI(self):
        # 容器，用来放置查询条件
        search_frame = tkinter.Frame(self.root)
        treeframe = tkinter.LabelFrame(self.root)

        search_frame.grid(row=0, column=0)
        treeframe.grid(row=1, column=0)

        # 查询条件，姓名
        self.namelable = tkinter.Label(search_frame, text='姓名：')
        self.namelable.grid(row=0, column=0, pady=6)
        self.name = tkinter.StringVar()
        userlist = mysqloption.selectuser(self.cur)
        # print(userlist)
        namelist = []
        idlist = []
        for user in userlist:
            # print(user)
            id = user[0]
            name = user[1]
            namelist.append(name)
            idlist.append(id)

        self.nameChosen = tkinter.ttk.Combobox(search_frame, width=18, textvariable=self.name, value=idlist)
        self.nameChosen['values'] = namelist
        # self.nameChosen.current(0)
        self.nameChosen.grid(row=0, column=1, pady=6)

        # 根据收支查询
        modes = ['支出','收入']
        #通过self.shouzhi.get()来获取其的状态, 其状态值为int类型,勾选为1,未勾选为0
        self.shouzhi = tkinter.StringVar()
        # 设置默认选中
        # self.shouzhi.set(1)
        for i, mode in enumerate(modes):
            self.shouzhiCheckbutton = tkinter.Radiobutton(search_frame, text=mode, variable=self.shouzhi,value=mode)
            self.shouzhiCheckbutton.grid(row=0, column=i + 2)


        #查询时间
        self.createtimelabel = tkinter.Label(search_frame,text='时间:')
        self.createtimelabel1= tkinter.Label(search_frame,text='~')
        self.createtime1 = tkinter.ttk.Entry(search_frame,width=10)
        self.createtime2 = tkinter.ttk.Entry(search_frame,width =10)
        self.createtimelabel.grid(row=0,column=5)
        self.createtime1.grid(row=0,column=6)
        self.createtimelabel1.grid(row=0,column=7)
        self.createtime2.grid(row=0,column=8)


        # 查询按钮
        self.button = tkinter.StringVar()
        self.button_search = tkinter.Button(search_frame, text='查询', width=10)
        self.button_search.grid(row=0, column=9, pady=6, padx=10)
        self.button_search.bind("<Button-1>", self.buttonListener4)

        self.tree = tkinter.ttk.Treeview(treeframe, show='headings')  # 表格 show='headings'即隐藏首列#
        # 设置了height=18  滚动条失效
        # self.tree = ttk.Treeview(treeframe,height=18, show='headings')
        self.vbar = tkinter.ttk.Scrollbar(treeframe, orient="vertical", command=self.tree.yview)
        # 定义树形结构与滚动条
        self.vbar.set(0.5, 1)

        self.tree.configure(yscroll=self.vbar.set)
        self.tree.bind('<<TreeviewSelect>>')

        self.tree["columns"] = ('id', '收入/支出', '姓名', '用途', '金额', '支付方式', '时间')
        self.tree.column("id", width=70, anchor='center')
        self.tree.column("收入/支出", width=80, anchor='center')  # 表示列,不显示
        self.tree.column('姓名', width=100, anchor='center')
        self.tree.column('用途', width=120, anchor='center')
        self.tree.column('金额', width=80, anchor='center')
        self.tree.column('支付方式', width=80, anchor='center')
        self.tree.column('时间', width=130, anchor='center')
        # 显示表头
        self.tree.heading("id", text="id")
        self.tree.heading("收入/支出", text="收入/支出")
        self.tree.heading('姓名', text='姓名')
        self.tree.heading('用途', text='用途')
        self.tree.heading('金额', text='金额')
        self.tree.heading('支付方式', text='支付方式')
        self.tree.heading('时间', text='时间')
        self.tree.grid(row=0, column=0, sticky="nsw")
        self.vbar.grid(row=0, column=1, sticky="ns")

        search = '1'
        if search != 'ButtonPress':
            results = self.get_data()
            self.show_tree(results)


    def get_data(self):
        results = mysqloption.search_data(self.cur)
        return results

    # 主界面展示数据
    def show_tree(self, results):

        # 先清空原来显示的数据，再插入显示更新的数据
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        if len(results) == 0:
            self.tree.insert("", "end", values=("", "", "", "暂无查询数据！"))
        # 插入更新的数据
        for i, result in enumerate(results):
            self.tree.insert("", "end", values=(
                i + 1, result['shouzhi'], result['name'], result['product_name'], result['money'], result['payname'],
                result['createtime']))
            # self.tree.grid(row=i,column=0)
            # self.tree.update()

    def menu_data(self):
        menubar = tkinter.Menu(self.root)

        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="新增", command=self.new_data)
        filemenu.add_command(label="导出", command=self.export_data)
        filemenu.add_command(label="导入", command=self.import_data)
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=self.root.quit)

        menubar.add_cascade(label="关于数据", menu=filemenu)

        helpmenu = tkinter.Menu(menubar, tearoff=0)

        helpmenu.add_command(label="关于")

        helpmenu.add_separator()

        helpmenu.add_command(label="使用方法")

        menubar.add_cascade(label="帮助", menu=helpmenu)

        self.root.config(menu=menubar)

    def center(self):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = int((ws - self.width) / 2)
        y = int((hs - self.heigth) / 2)
        weizhi = '%dx%d+%d+%d' % (self.width, self.heigth, x, y)
        self.root.geometry(weizhi)

    # 弹窗新增消费信息
    def new_data(self):

        self.top = tkinter.Toplevel(self.root)
        self.top.geometry('650x300')
        self.top.title('新增消费数据')
        self.top.resizable(width=False, height=False)
        # 连接数据库
        self.db, self.cur = mysqloption.connDB()
        # 收入支出选择
        modes = [('支出', '1'), ('收入', '2')]
        self.shouzhi = tkinter.IntVar()
        self.shouzhi.set(1)
        for i, mode in enumerate(modes):
            self.shouzhiRadiobutton = tkinter.Radiobutton(self.top, text=modes[i][0], variable=self.shouzhi,
                                                          value=modes[i][1])
            self.shouzhiRadiobutton.grid(row=0, column=i + 1)

        # 姓名下拉框
        self.namelable = tkinter.Label(self.top, text='姓      名：')
        self.namelable.grid(row=1, column=0, pady=6)
        self.name = tkinter.StringVar()
        userlist = mysqloption.selectuser(self.cur)
        # print(userlist)
        namelist = []
        idlist = []
        for user in userlist:
            # print(user)
            id = user[0]
            name = user[1]
            namelist.append(name)
            idlist.append(id)

        self.nameChosen = tkinter.ttk.Combobox(self.top, width=18, textvariable=self.name, value=idlist)
        self.nameChosen['values'] = namelist
        self.nameChosen.current(0)
        self.nameChosen.grid(row=1, column=1, pady=6)

        # 用途输入框
        self.dowhatlable = tkinter.Label(self.top, text='用      途：')
        self.dowhatlable.grid(row=3, column=0, pady=6)
        self.dowhat = tkinter.StringVar()
        self.dowhatEntered = tkinter.ttk.Entry(self.top, width=20, textvariable=self.dowhat)
        self.dowhatEntered.grid(row=3, column=1, pady=6)

        # 金额输入框
        self.moneylable = tkinter.Label(self.top, text='金      额：')
        self.moneylable.grid(row=4, column=0, pady=6)
        self.money = tkinter.StringVar()
        self.moneyEntered = tkinter.ttk.Entry(self.top, width=20, textvariable=self.money)
        self.moneyEntered.grid(row=4, column=1, pady=6)
        # 收入支出时间
        self.paytime = tkinter.Label(self.top, text='消费时间：')
        self.paytime.grid(row=5, column=0, pady=6, ipadx=5)
        self.paytimevalue = tkinter.StringVar()
        self.paytimeEntered = tkinter.ttk.Entry(self.top, width=20, textvariable=self.paytime)
        self.paytimeEntered.grid(row=5, column=1, pady=6)

        # 支付方式复选框
        self.paymentlable = tkinter.Label(self.top, text='支付方式：')
        self.paymentlable.grid(row=6, column=0, pady=6, ipadx=5)
        picks = mysqloption.selectpayment(self.cur)
        # print(picks)
        self.vars = []
        self.payment = tkinter.IntVar()
        # self.payment.set(1)
        for i, pick in enumerate(picks):
            self.paymentCheckButton = tkinter.Checkbutton(self.top, text=picks[i][1], variable=self.payment,
                                                          onvalue=picks[i][0],
                                                          offvalue=picks[i][1])
            # print(self.paymentCheckButton)
            self.paymentCheckButton.grid(row=6, column=i + 1, ipadx=10)
            self.vars.append(self.payment)

        self.button = tkinter.StringVar()
        self.button.set('提交')

        self.button_ok = tkinter.Button(self.top, textvariable=self.button, width=10)
        self.button_ok.grid(row=7, column=2, pady=6, padx=10)
        self.button_ok.bind("<Button-1>", self.buttonListener1)

        self.button_cancel = tkinter.Button(self.top, text="清空", width=10)
        self.button_cancel.grid(row=7, column=3, pady=6)
        self.button_cancel.bind("<Button-1>", self.buttonListener2)

    def buttonListener1(self, event):  # 创建事件，调用另外一个函数的功能，

        shouzhi = self.shouzhi.get()
        # print('shouzhi', type(shouzhi), shouzhi)

        name = self.nameChosen.get()  # 获取text_agentno文本框里的值
        dowhat = self.dowhatEntered.get()
        # print('dowhat的类型',type(dowhat))
        money = self.moneyEntered.get()
        # print("money",type(money))
        payment_id = self.payment.get()
        # print(type(payment_id))
        user_id = mysqloption.selectuserbyname(self.cur, name)
        # print("user_id",type(user_id))
        # createtime = time.strftime('%Y-%m-%d', time.localtime())
        paytime = self.paytimeEntered.get()
        # print('createtime的类型%s'%createtime, type(createtime))
        # print('user_id:%s, payment_id:%s, dowhat:%s, paytime:%s, money:%s,shouzhi:%s'%(user_id, payment_id, dowhat, paytime, money,shouzhi))
        #
        if shouzhi != 1 and shouzhi != 2:
            tkinter.messagebox.showwarning('警告', '收入or支出 请务必选择一个！')
            # self.button_ok.bind('<ButtonRelease-1>')
        elif dowhat is None or dowhat == '':
            tkinter.messagebox.showwarning('警告', '用途请务必填写清楚！')
        elif money is None or money == '':
            tkinter.messagebox.showwarning('警告', '消费金额请务必填写！')
        elif payment_id == 0:
            tkinter.messagebox.showwarning('警告', '请务必选择支付方式！')
        elif paytime == '':
            tkinter.messagebox.showwarning('警告', '消费时间请务必填写！')
        else:
            sta = mysqloption.insert_sql(self.cur, self.db, user_id, payment_id, dowhat, paytime, money, shouzhi)
            if sta == 1:
                tkinter.messagebox.showinfo('提示', '添加成功！如需再次添加，请先点击【清空】按钮')
            if sta == 0:
                tkinter.messagebox.showinfo('提示', '添加失败，请检查')

    def buttonListener2(self, event):  # 创建第二个事件，清空输入框
        self.shouzhi.set(1)
        self.nameChosen.current(0)
        self.dowhatEntered.delete('0', 'end')
        self.moneyEntered.delete('0', 'end')
        self.paytimeEntered.delete('0', 'end')
        self.payment.set('0')

    def buttonListener3(self,result):  # 创建第三个事件，导出结果到excel中

        # result = mysqloption.search_data(self.cur)
        OE = optionExcel.OptionExcel(result)
        OE.CreateExcel()

    def export_data(self):
        self.export_message = \
            tkinter.messagebox.askyesno('导出数据', '确认导出数据到excel文件吗？请注意保存路径是D:\study\MyFamilyFee20181\caseresult_path')

        if self.export_message:
            results = self.get_data()
            OE = optionExcel.OptionExcel(results)
            OE.CreateExcel()

    def import_data(self):

        self.import_message = \
            tkinter.filedialog.askopenfilename()
        print(self.import_message)
        if self.import_message =='':
            lg.info('取消导入文件')
        else:
            with open(self.import_message) as f:
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

                    sta = mysqloption.insertsqlfrom_zhifubao(self.cur, self.db, user_id, payment_id,
                                                             jiaoyi_num, shanghudingdan_num, createtime, pay_time,
                                                             edit_time, jiaoyilaiyuan, jiaoyileixing, jiaoyiduifang,
                                                             product_name,
                                                             money, shouzhi, remark, zijinzhuangtai)
                    if sta == 1:
                        print('添加成功！')
                    if sta == 0:
                        print('添加失败，请检查')



    def buttonListener5(self,event):
        pass

    def buttonListener4(self,event):  # 查询按钮触发的事件

        name = self.nameChosen.get()
        shouzhi = self.shouzhi.get()
        createtime1 = self.createtime1.get()
        createtime2 = self.createtime2.get()
        self.root.update()
        lg.info('姓名:%s,收支:%s，时间：%s~%s' % (name, shouzhi,createtime1,createtime2))
        if shouzhi == '支出' or shouzhi == '收入':
            result = mysqloption.search_data(self.cur, name, shouzhi,createtime1,createtime2)
        else:
            result = mysqloption.search_data(self.cur, name,createtime1,createtime2)

        self.show_tree(result)
        return result
if __name__ == '__main__':
    mw = MainWindow()
