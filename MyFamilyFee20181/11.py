from tkinter import *

root = Tk()
# 将一字符串与Checkbutton的值绑定，每次点击Checkbutton，将打印出当前的值
v = StringVar()


def callCheckbutton():
    print(v.get())


Checkbutton(root,
            variable=v,
            text='checkbutton value',
            onvalue='python on',  # 设置On的值
            offvalue='tkinter off',  # 设置Off的值
            command=callCheckbutton).pack()
v.set('tkinter off')
root.mainloop()