# coding:utf-8
from tkinter import *
from tkinter.messagebox import *
from PIL import ImageTk
import service, datautil, maintain, notice, house, inspection, account

loginobj = None
adminid = 0


class AdminMainWin:  # 管理员界面
    def __init__(self):
        self.adminmainwin = Toplevel()
        self.adminmainwin.geometry('1401x808+0+0')
        self.adminmainwin.title('http://management/admin')
        self.adminmainwin.config(background='white')

        # 加载图像
        self.photo = ImageTk.PhotoImage(file='./image/adminmain.png')
        # 显示图像，使用anchor和place的参数来控制显示方式
        Label(self.adminmainwin, image=self.photo).place(x=0, y=0, anchor='nw')

        # 设置窗口属性
        self.adminmainwin.resizable(False, False)

        # 设置左侧按钮
        lst = ['首 页', '管理员信息', '报修管理', '公告管理', '保安保洁', '业主信息', '房产信息']
        self.btn_lst = self.create_button(lst, self.adminmainwin)

        # 绑定事件
        self.btn_lst[1].config(command=AdminWin)
        self.btn_lst[2].config(command=maintain.MainTainWin)
        self.btn_lst[3].config(command=notice.Notice)
        self.btn_lst[4].config(command=inspection.Inspection)
        self.btn_lst[5].config(command=account.AccountWin)
        self.btn_lst[6].config(command=house.HouseWin)
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
        self.adminwin.config(background='white')
        self.adminwin.geometry('1129x519+280+150')
        image = PhotoImage(file='./image/adminfo.png')

        # 返回按钮
        btnreturn = datautil.create_win(image, self.adminwin)  # 按钮对象被赋给了一个变量
        btnreturn.config(command=self.close)
        Label(self.adminwin, text='搜索', font=16, bg='white').place(x=10, y=180, width=50, height=40)
        self.search = Entry(self.adminwin, font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.search.place(x=60, y=180, width=200, height=40)

        # 添加记录
        Button(self.adminwin, text='查询', bg='#5B9BD5', fg='white', font=16,
               relief='flat', command=self.query).place(x=270, y=180, width=60, height=40)
        Button(self.adminwin, text='+添加记录', bg='green', font=16,
               fg='white', relief='flat', command=AddAdmin).place(x=340, y=180, width=100, height=40)
        Button(self.adminwin, text='编辑', bg='orange', font=16,
               fg='white', relief='flat', command=ModifyAdmin).place(x=450, y=180, width=60, height=40)
        Button(self.adminwin, text='删除', bg='red', font=16,
               fg='white', relief='flat', command=self.delete).place(x=520, y=180, width=60, height=40)
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

    def delete(self):
        if self.tv.focus():
            if adminid != 1:
                showwarning('警告', '非超级管理员不能删除其他管理员')
                return

            iid = self.tv.focus()
            item = self.tv.item(iid)
            values = item.get('values')
            id = values[0]
            if id == adminid:
                showinfo('警告', '超级管理员不能删除自己')
            else:
                answer = askyesno('提示', '确定要删除吗?')
                if answer:
                    sql = 'delete from  admins where id=%s'
                    result = service.exec(sql, id)
                    if result > 0:
                        showinfo('提示', '管理员信息删除成功')
                        self.query()
                    else:
                        showerror('警告', '删除管理员信息失败')
        else:
            showwarning('警告', '请选择一条要删除的数据')

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


class AddAdmin:
    def __init__(self):
        self.addadminwin = Toplevel()
        self.addadminwin.overrideredirect(True)

        self.addadminwin.geometry('1129x519+280+150')
        image = PhotoImage(file='./image/modify.png')

        btnreturn = datautil.create_win(image, self.addadminwin)
        btnreturn.config(command=self.close)
        # 添加项
        Label(self.addadminwin, text='姓名*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.37,
                                                                                     anchor='w', width=60, height=40)
        self.adminname = Entry(self.addadminwin, font=16, highlightbackground='#aaaaaa', highlightthickness=1,
                               relief='flat')
        self.adminname.place(relx=0.07, rely=0.44, width=300, height=40)
        # 密码
        Label(self.addadminwin, text='密码*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.57,
                                                                                     anchor='w', width=60, height=40)
        self.password = Entry(self.addadminwin, show='*', font=16, highlightbackground='#aaaaaa',
                              highlightthickness=1, relief='flat')
        self.password.place(relx=0.07, rely=0.62, width=300, height=40)
        # 确认密码
        Label(self.addadminwin, text='确认密码*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.78,
                                                                                         anchor='w', width=100,
                                                                                         height=40)
        self.conpassword = Entry(self.addadminwin, show='*', font=16, highlightbackground='#aaaaaa',
                                 highlightthickness=1, relief='flat')
        self.conpassword.place(relx=0.07, rely=0.82, width=300, height=40)
        # 性别
        Label(self.addadminwin, text='性别*', font=16, anchor='w', bg='white').place(relx=0.37, rely=0.38,
                                                                                     anchor='w', width=60, height=40)
        self.genderv = IntVar()
        self.gender1 = Radiobutton(self.addadminwin, variable=self.genderv, text='男', value=1, bg='white')
        self.gender1.place(relx=0.37, rely=0.46, anchor='w', width=50, height=40)
        self.gender2 = Radiobutton(self.addadminwin, variable=self.genderv, text='女', value=0, bg='white')
        self.gender2.place(relx=0.47, rely=0.46, anchor='w', width=50, height=40)
        # 年龄
        Label(self.addadminwin, text='年龄*', font=16, anchor='w', bg='white').place(relx=0.37, rely=0.58,
                                                                                     anchor='w', width=60, height=40)
        self.age = Entry(self.addadminwin, font=16, highlightbackground='#aaaaaa', highlightthickness=1,
                         relief='flat')
        self.age.place(relx=0.37, rely=0.66, anchor='w', width=300, height=40)
        # 手机号
        Label(self.addadminwin, text='手机号*', font=16, anchor='w', bg='white').place(relx=0.37, rely=0.78,
                                                                                       anchor='w', width=100,
                                                                                       height=40)
        self.phone = Entry(self.addadminwin, font=16, highlightbackground='#aaaaaa', highlightthickness=1,
                           relief='flat')
        self.phone.place(relx=0.37, rely=0.86, anchor='w', width=300, height=40)
        # 地址
        Label(self.addadminwin, text='地址*', font=16, anchor='w', bg='white').place(relx=0.67, rely=0.38,
                                                                                     anchor='w', width=60, height=40)
        self.addr = Entry(self.addadminwin, font=16, highlightbackground='#aaaaaa', highlightthickness=1,
                          relief='flat')
        self.addr.place(relx=0.67, rely=0.46, anchor='w', width=300, height=40)
        # 备注
        Label(self.addadminwin, text='备注', font=16, anchor='w', bg='white').place(relx=0.67, rely=0.58, anchor='w',
                                                                                    width=60, height=40)
        self.memo = Text(self.addadminwin, font=16, highlightbackground='#aaaaaa', highlightthickness=1,
                         relief='flat')
        self.memo.place(relx=0.67, rely=0.69, anchor='w', width=300, height=70)
        # 保存按钮
        Button(self.addadminwin, text='保存', bg='#5B9BD5', fg='white', font=16, command=self.insertadmin).place(
            relx=0.91, rely=0.90, anchor='center', width=60, height=40)
        self.addadminwin.mainloop()

    def insertadmin(self):
        if self.adminname.get() == '' or self.password.get() == '':
            showwarning('警告', '用户名或密码不允许为空!')
            return False
        sql = 'select * from admins where name=%s'
        result = service.query(sql, self.adminname.get())
        if len(result) > 0:
            showwarning('警告', '管理员名重复')
            return False
        if self.conpassword.get() != self.password.get():
            showwarning('警告', '确定密码和密码不一致')
            return False
        sql = 'insert into admins (name,password,sex,age,phone,addr,memo)values (%s,%s,%s,%s,%s,%s,%s)'
        values = (self.adminname.get(), self.password.get(), '男' if self.genderv.get() == 1 else '女',
                  self.age.get(), self.phone.get(), self.addr.get(),
                  self.memo.get('0.0', END))
        result = service.exec(sql, values)
        if result > 0:
            showinfo('提示', '新增管理员成功！')
            self.addadminwin.destroy()

        else:
            showerror('错误', '新增管理员失败！')

    def close(self):
        self.addadminwin.destroy()


class ModifyAdmin:
    def __init__(self):
        sql = 'select name,password ,sex,age,phone ,addr,memo from admins where id=%s'
        result = service.query(sql, adminid)
        self.modifyadminwin = Toplevel()
        self.modifyadminwin.overrideredirect(True)
        self.modifyadminwin.geometry('1129x519+280+150')
        image = PhotoImage(file='./image/adminfo.png')

        # 计算新的宽度和高度，保持比例不变
        new_width = self.modifyadminwin.winfo_width()
        height = image.height() * (new_width / image.width())

        # 创建一个新的 PhotoImage 对象，设置新的宽度和高度
        new_image = PhotoImage(width=new_width, height=int(height), file='./image/adminfo.png')

        btnreturn = datautil.create_win(image, self.modifyadminwin)
        btnreturn.config(command=self.close)
        # 添加项
        Label(self.modifyadminwin, text='姓名*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.37,
                                                                                        anchor='w', width=60, height=40)
        self.adminname = Entry(self.modifyadminwin, font=16, highlightbackground='#aaaaaa', highlightthickness=1,
                               relief='flat')
        self.adminname.place(relx=0.07, rely=0.44, width=300, height=40)
        self.adminname.insert(0, result[0][0])
        # 密码
        Label(self.modifyadminwin, text='密码*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.57,
                                                                                        anchor='w', width=60, height=40)
        self.password = Entry(self.modifyadminwin, show='*', font=16, highlightbackground='#aaaaaa',
                              highlightthickness=1, relief='flat')
        self.password.place(relx=0.07, rely=0.62, width=300, height=40)
        self.password.insert(0, result[0][1])
        # 确认密码
        Label(self.modifyadminwin, text='确认密码*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.78,
                                                                                            anchor='w', width=100,
                                                                                            height=40)
        self.conpassword = Entry(self.modifyadminwin, show='*', font=16, highlightbackground='#aaaaaa',
                                 highlightthickness=1, relief='flat')
        self.conpassword.place(relx=0.07, rely=0.82, width=300, height=40)
        self.conpassword.insert(0, result[0][1])
        Label(self.modifyadminwin, text='性别*', font=16, anchor='w', bg='white').place(relx=0.37, rely=0.38,
                                                                                        anchor='w', width=60, height=40)
        self.genderv = IntVar()
        self.genderv.set(1 if result[0][2] == '男' else 0)
        self.gender1 = Radiobutton(self.modifyadminwin, variable=self.genderv, text='男', value=1, bg='white')
        self.gender1.place(relx=0.37, rely=0.46, anchor='w', width=50, height=40)
        self.gender2 = Radiobutton(self.modifyadminwin, variable=self.genderv, text='女', value=0, bg='white')
        self.gender2.place(relx=0.47, rely=0.46, anchor='w', width=50, height=40)
        # 年龄
        Label(self.modifyadminwin, text='年龄*', font=16, anchor='w', bg='white').place(relx=0.37, rely=0.58,
                                                                                        anchor='w', width=60, height=40)
        self.age = Entry(self.modifyadminwin, font=16, highlightbackground='#aaaaaa', highlightthickness=1,
                         relief='flat')
        self.age.place(relx=0.37, rely=0.66, anchor='w', width=300, height=40)
        self.age.insert(0, result[0][3])
        # 手机号
        Label(self.modifyadminwin, text='手机号*', font=16, anchor='w', bg='white').place(relx=0.37, rely=0.78,
                                                                                          anchor='w', width=100,
                                                                                          height=40)
        self.phone = Entry(self.modifyadminwin, font=16, highlightbackground='#aaaaaa', highlightthickness=1,
                           relief='flat')
        self.phone.place(relx=0.37, rely=0.86, anchor='w', width=300, height=40)
        self.phone.insert(0, result[0][4])
        # 地址
        Label(self.modifyadminwin, text='地址*', font=16, anchor='w', bg='white').place(relx=0.67, rely=0.38,
                                                                                        anchor='w', width=60, height=40)
        self.addr = Entry(self.modifyadminwin, font=16, highlightbackground='#aaaaaa', highlightthickness=1,
                          relief='flat')
        self.addr.place(relx=0.67, rely=0.46, anchor='w', width=300, height=40)
        self.addr.insert(0, result[0][5])
        # 备注
        Label(self.modifyadminwin, text='备注', font=16, anchor='w', bg='white').place(relx=0.67, rely=0.58, anchor='w',
                                                                                       width=60, height=40)
        self.memo = Text(self.modifyadminwin, font=16, highlightbackground='#aaaaaa', highlightthickness=1,
                         relief='flat')
        self.memo.place(relx=0.67, rely=0.69, anchor='w', width=300, height=70)
        self.memo.insert('0.0', '' if result[0][6] == None else result[0][6])
        # 保存按钮
        Button(self.modifyadminwin, text='保存', bg='#5B9BD5', fg='white', font=16, command=self.modifyadmin).place(
            relx=0.91, rely=0.90, anchor='center', width=60, height=40)
        self.modifyadminwin.mainloop()

    def modifyadmin(self):
        if self.adminname.get() == '' or self.password.get() == '':
            showwarning('警告', '管理员名称或密码不允许为空')
            return False
        sql = 'select id from admins where name=%s and id!=%s'
        result = service.query(sql, self.adminname.get(), adminid)
        if len(result):
            showwarning('警告', '管理员名称重复！')
            return False
        if self.conpassword.get() != self.password.get():
            showwarning('警告', '密码与确认密码不一致')
            return False
        sex = '男' if self.genderv.get() == 1 else '女'

        sql = 'update admins set name=%s,password=%s,sex=%s,age=%s,phone=%s,addr=%s,memo=%s where id=%s'
        values = (self.adminname.get(), self.password.get(), sex,
                  self.age.get(), self.phone.get(), self.addr.get(), self.memo.get('0.0', END), adminid)
        result2 = service.exec(sql, values)
        if result2 > 0:
            showinfo('提示', '修改管理员信息成功')
            self.close()
        else:
            showerror('错误', '修改管理员信息失败')

    def close(self):
        self.modifyadminwin.destroy()

# AdminMainWin()
