from tkinter import *
from tkinter.messagebox import *

import service, datautil


class AccountWin():
    def __init__(self):
        self.id = 0
        self.accountwin = Toplevel()
        self.accountwin.overrideredirect(True)
        image = PhotoImage(file='./image/account.png')
        # self.adminwin.title('http://www.management/admin')
        self.accountwin.geometry('1129x519+280+150')
        self.accountwin.config(background='white')
        btnreturn = datautil.create_win(image, self.accountwin)
        btnreturn.config(command=self.close)
        Label(self.accountwin, text='搜索', font=16, bg='white').place(x=10, y=180, width=50, height=40)
        self.search = Entry(self.accountwin, font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.search.place(x=60, y=180, width=200, height=40)

        # 添加记录
        Button(self.accountwin, text='查询', bg='#5B9BD5', fg='white', font=16,
               relief='flat', command=self.query).place(x=270, y=180, width=60, height=40)
        Button(self.accountwin, text='+添加记录', bg='green', font=16,
               fg='white', relief='flat', command=lambda: MondifyAccountWin(False, 0)).place(x=340, y=180, width=100,
                                                                                             height=40)
        Button(self.accountwin, text='编辑', bg='orange', font=16,
               fg='white', relief='flat', command=lambda: MondifyAccountWin(True, self.id)).place(x=450, y=180,
                                                                                                  width=60, height=40)
        Button(self.accountwin, text='删除', bg='red', font=16,
               fg='white', relief='flat', command=self.delete).place(x=520, y=180, width=60, height=40)
        # 创建TreeView
        lst = ['ownerid', 'username', 'password', 'carid']
        lst_name = ['序号', '用户名', '密码', '车牌号', ]

        self.tv = datautil.tv(self.accountwin, lst, lst_name)  # 使用 tv 函数创建 Treeview
        self.tv.place(x=10, y=230, width=1129, height=286)  # 设置宽度为1129
        # 自适应调整列宽
        for i, col in enumerate(lst):
            self.tv.column(col, minwidth=0, width=100, stretch=True)  # 初始宽度100,允许自适应

        self.tv.bind('<Double-Button-1>', self.get_selected_item_data)
        self.query()
        self.accountwin.mainloop()

    def get_selected_item_data(self, event):
        iid = self.tv.focus()
        if iid:
            item = self.tv.item(iid)
            values = item.get('values')
            self.id = values[0]
        else:
            self.id = 0

    def close(self):
        self.accountwin.destroy()

    def query(self):
        if self.search.get() == '':
            sql = 'select * from custom_account'
            result = service.query2(sql)
        else:
            sql = 'select * from custom_account where username like %s'
            result = service.query(sql, '%' + self.search.get() + '%')
        result = list(result)
        result_lst = []
        for item in result:
            item = list(item)
            item[2] = '****'
            result_lst.append(item)
        datautil.tv_data(self.tv, result_lst)

    def delete(self):
        if self.tv.focus():
            answer = askyesno('提示', '确定要删除业主信息吗?')
            if answer:
                sql = 'delete from custom_account where ownerid=%s'
                result = service.exec(sql, self.id)
                if result > 0:
                    showinfo('提示', '业主信息删除成功')
                else:
                    showerror('错误', '业主信息删除失败')

        else:
            showwarning('警告', '请先选择一条要删除的数据')


class MondifyAccountWin:
    def __init__(self, modify, id):
        self.modify = modify
        self.id = id
        self.modifyaccountwin = Toplevel()

        self.modifyaccountwin.geometry('1129x519+280+150')
        self.modifyaccountwin.overrideredirect(True)
        self.modifyaccountwin.config(background='white')
        image = PhotoImage(file='./image/modifyaccount.png')
        btnreturn = datautil.create_win(image, self.modifyaccountwin)
        btnreturn.config(command=self.close)
        # 用户名
        Label(self.modifyaccountwin, text='用户名*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.37,
                                                                                            anchor='w', width=80,
                                                                                            height=40)
        self.username = Entry(self.modifyaccountwin, font=16, highlightbackground='#aaaaaa',
                              highlightthickness=1, relief='flat')
        self.username.place(relx=0.07, rely=0.43, width=300, height=40)
        # 密码
        Label(self.modifyaccountwin, text='密码*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.57,
                                                                                          anchor='w', width=100,
                                                                                          height=40)
        self.pwd = Entry(self.modifyaccountwin, show='*', font=16, highlightbackground='#aaaaaa',
                         highlightthickness=1, relief='flat')
        self.pwd.place(relx=0.07, rely=0.62, width=300, height=40)
        # 确认密码
        Label(self.modifyaccountwin, text='确认密码*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.78,
                                                                                              anchor='w', width=100,
                                                                                              height=80)
        self.compwd = Entry(self.modifyaccountwin, show='*', font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.compwd.place(relx=0.07, rely=0.82, width=300, height=40)
        # 业主编号
        Label(self.modifyaccountwin, text='业主编号*', font=16, anchor='w', bg='white').place(relx=0.42, rely=0.38,
                                                                                              anchor='w', width=80,
                                                                                              height=40)
        self.ownerid = Entry(self.modifyaccountwin, font=16, highlightbackground='#aaaaaa',
                             highlightthickness=1, relief='flat')
        self.ownerid.place(relx=0.42, rely=0.46, anchor='w', width=300, height=40)
        # 车牌号
        Label(self.modifyaccountwin, text='车牌号*', font=16, anchor='w', bg='white').place(relx=0.42, rely=0.58,
                                                                                            anchor='w', width=80,
                                                                                            height=40)
        self.carno = Entry(self.modifyaccountwin, font=16, highlightbackground='#aaaaaa',
                           highlightthickness=1, relief='flat')
        self.carno.place(relx=0.42, rely=0.66, anchor='w', width=300, height=40)
        # 保存按钮
        btn_save = Button(self.modifyaccountwin, text='保存', bg='#5B9BD5', fg='white', font=16)
        btn_save.place(
            relx=0.66, rely=0.87, anchor='center', width=60, height=40)
        if self.modify and self.id != 0:
            sql = 'select * from custom_account where ownerid=%s'
            result = service.query(sql, self.id)
            if len(result) > 0:
                self.ownerid.insert(0, result[0][0])
                self.username.insert(0, result[0][1])
                self.pwd.insert(0, result[0][2])
                self.compwd.insert(0, result[0][2])
                self.carno.insert(0, result[0][3])
                self.ownerid.config(state=DISABLED)
            btn_save.config(command=self.update)
        elif self.modify == False and self.id == 0:
            btn_save.config(command=self.insert)
        else:
            showinfo('提示', '请先选择一条要修改的数据')
        self.modifyaccountwin.mainloop()

    def update(self):
        username = self.username.get()
        pwd = self.pwd.get()
        compwd = self.compwd.get()
        owerid = self.ownerid.get()
        carno = self.carno.get()
        if username == '' or pwd == '' or compwd == '' or owerid == '' or carno == '':
            showwarning('警告', '*为必填项')
            return False
        if compwd != pwd:
            showwarning('警告', '*为必填项')
            return False
        sql = 'update custom_account set username=%s,`password`=%s,carid=%s where ownerid=%s'
        result = service.exec(sql, (username, pwd, carno, owerid))
        if result > 0:
            showinfo('提示', '修改业主信息成功')
            self.modifyaccountwin.destroy()
        else:
            showerror('错误', '修改业主信息失败')

    def insert(self):
        username = self.username.get()
        pwd = self.pwd.get()
        compwd = self.compwd.get()
        owerid = self.ownerid.get()
        carno = self.carno.get()
        if username == '' or pwd == '' or compwd == '' or owerid == '' or carno == '':
            showwarning('警告', '*为必填项')
            return False
        if compwd != pwd:
            showwarning('警告', '*为必填项')
            return False
        sql = 'insert into custom_account values (%s,%s,%s,%s)'
        result = service.exec(sql, (owerid, username, pwd, carno))
        if result > 0:
            showinfo('提示', '新增业主信息成功')
            self.modifyaccountwin.destroy()
        else:
            showerror('错误', '新增业主信息失败')

    def close(self):
        self.modifyaccountwin.destroy()
