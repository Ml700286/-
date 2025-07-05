# coding:utf-8
from tkinter import *
from PIL import Image, ImageTk
import service, datautil, maintain2, notice2, house2, inspection2, account2

loginobj = None
adminid = 0


class AdminMainWin():
    def __init__(self):
        self.adminmainwin = Toplevel()
        self.adminmainwin.geometry('1401x808+0+0')
        self.adminmainwin.title('http://management/admin')
        self.adminmainwin.config(background='white')


        # 加载图像
        self.photo = ImageTk.PhotoImage(file='./image/adminmain.png')
        # 显示图像，使用anchor和place的参数来控制显示方式
        Label(self.adminmainwin, image=self.photo).place(x=0, y=0, anchor='nw')

        self.adminmainwin.resizable(False, False)

        # 设置左侧按钮
        lst = ['首 页', '管理员信息', '报修管理', '公告管理', '保安保洁', '业主信息', '房产信息']
        self.btn_lst = self.create_button(lst, self.adminmainwin)

        # 绑定事件
        self.btn_lst[1].config(command=AdminWin)
        self.btn_lst[2].config(command=maintain2.MainTainWin)
        self.btn_lst[3].config(command=notice2.Notice)
        self.btn_lst[4].config(command=inspection2.Inspection)
        self.btn_lst[5].config(command=account2.AccountWin)
        self.btn_lst[6].config(command=house2.HouseWin)
        x1, y1, width1, height1 = 20, 200, 40, 40
        # 小图标
        imagepath = ['./image/icon' + str(i + 1) + '.png' for i in range(len(lst))]
        imagelst = []
        for item in imagepath:
            image1 = PhotoImage(file=item)
            imagelst.append(image1)
        for item in imagelst:
            lab = Label(self.adminmainwin, image=item)
            lab.place(x=x1, y=y1, width=width1, height=height1)
            y1 += 60
        self.adminmainwin.bind('<Destroy>', self.close_adminwin)
        self.adminmainwin.mainloop()

    def close_adminwin(self, event):

        self.adminmainwin.destroy()
        loginobj.loginwin.deiconify()

    def create_button(self, lst, win):
        btn_lst = []
        x, y, width, height = 70, 190, 190, 60
        x1, y1, width1, height1 = 20, 200, 40, 40
        imagelst = []

        for i in range(len(lst)):
            image = PhotoImage(file=f'./image/icon{i + 1}.png')
            imagelst.append(image)

            btn = Button(win, bg='white', anchor='w', fg='#5B9BD5', text=lst[i], font=16, relief='flat')
            btn.place(x=x, y=y, width=width, height=height)
            y += 60
            btn_lst.append(btn)

        return btn_lst


class AdminWin:
    def __init__(self):
        self.adminwin = Toplevel()
        self.adminwin.overrideredirect(True)
        self.adminwin.title('http://www.management/admin')

        self.adminwin.geometry('1129x519+280+150')
        self.adminwin.config(background='white')
        image = PhotoImage(file='./image/adminfo.png')
        btnreturn = datautil.create_win(image, self.adminwin)
        btnreturn.config(command=self.close)

        Label(self.adminwin, text='搜索', font=16, bg='white').place(x=10, y=180, width=50, height=40)
        self.search = Entry(self.adminwin, font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.search.place(x=60, y=180, width=200, height=40)

        # 添加记录
        Button(self.adminwin, text='查询', bg='#5B9BD5', fg='white', font=16,
               relief='flat', command=self.query).place(x=270, y=180, width=60, height=40)

        # 创建TreeView
        lst = ['id', 'name', 'password', 'sex', 'age', 'phone', 'addr', 'memo']
        lst_name = ['序号', '用户名', '密码', '性别', '年龄', '手机号', '地址', '备注']
        self.tv = datautil.tv(self.adminwin, lst, lst_name)  # 使用 tv 函数创建 Treeview
        self.tv.place(x=10, y=230, width=1129, height=286)  # 设置宽度为1129
        # 自适应调整列宽
        for i, col in enumerate(lst):
            self.tv.column(col, minwidth=0, width=100, stretch=True)  # 初始宽度100,允许自适应

        # self.tv.bind('<Double-Button-1>', self.get_selected_item_data)
        self.query()
        self.adminwin.mainloop()

    def close(self):
        self.adminwin.destroy()

    def query(self):
        if self.search.get() == '':
            sql = 'select * from admins'
            result = service.query2(sql)
        else:
            sql = 'select * from admins where name like %s'
            result = service.query(sql, '%' + self.search.get() + '%')
        result = list(result)
        lst_result = []
        for item in result:
            item = list(item)
            item[2] = '******'
            if item[-1] == None:
                item[-1] = ''
            lst_result.append(item)
        # print(result)
        datautil.tv_data(self.tv, lst_result)
