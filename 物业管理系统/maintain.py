from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import Combobox
import service, datautil


class MainTainWin:
    def __init__(self):
        self.id = 0
        self.maintainwin = Toplevel()
        self.maintainwin.overrideredirect(True)
        image = PhotoImage(file='./image/maintain.png')
        # self.adminwin.title('http://www.management/admin')

        self.maintainwin.geometry('1129x519+280+150')
        self.maintainwin.config(background='white')

        btnreturn = datautil.create_win(image, self.maintainwin)
        btnreturn.config(command=self.close)
        Label(self.maintainwin, text='搜索', font=16, bg='white').place(x=10, y=180, width=50, height=40)
        self.search = Entry(self.maintainwin, font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.search.place(x=60, y=180, width=200, height=40)

        # 添加记录
        Button(self.maintainwin, text='查询', bg='#5B9BD5', fg='white', font=16,
               relief='flat', command=self.query).place(x=270, y=180, width=60, height=40)
        Button(self.maintainwin, text='+添加记录', bg='green', font=16,
               fg='white', relief='flat', command=lambda: ModifyMainTain(False, 0)).place(x=340, y=180, width=100,
                                                                                          height=40)
        Button(self.maintainwin, text='编辑', bg='orange', font=16,
               fg='white', relief='flat', command=lambda: ModifyMainTain(True, self.id)).place(x=450, y=180, width=60,
                                                                                               height=40)
        Button(self.maintainwin, text='删除', bg='red', font=16,
               fg='white', relief='flat', command=self.delete).place(x=520, y=180, width=60, height=40)
        # 创建TreeView
        lst = ['id', 'sdate', 'thing', 'status', 'homesnumber', 'rdate', 'tcost', 'scost', 'maintainer', 'smemo']
        lst_name = ['序号', '报修日期', '报修物品', '状态', '房门号', '维修日期', '预计花费', '实际花费', '报修人',
                    '报修详情']
        self.tv = datautil.tv(self.maintainwin, lst, lst_name)  # 使用 tv 函数创建 Treeview
        self.tv.place(x=10, y=230, width=1129, height=286)  # 设置宽度为1129
        # 自适应调整列宽
        for i, col in enumerate(lst):
            self.tv.column(col, minwidth=0, width=100, stretch=True)  # 初始宽度100,允许自适应

        self.tv.bind('<Double-Button-1>', self.get_selected_item_data)
        self.query()
        self.maintainwin.mainloop()

    def get_selected_item_data(self, event):
        iid = self.tv.focus()
        if iid:
            item = self.tv.item(iid)
            values = item.get('values')
            self.id = values[0]
        else:
            self.id = 0

    def delete(self):
        if self.tv.focus():
            answer = askyesno('提示', '确定要删除吗?')
            if answer:
                sql = 'delete from maintain where id=%s'
                result = service.exec(sql, self.id)
                if result > 0:
                    showinfo('提示', '删除报修信息成功')
                    self.query()
                else:
                    showerror('错误', '删除报修信息失败')
        else:
            showwarning('提示', '请先选择一条要删除的数据')

    def query(self):
        if self.search.get() == '':
            sql = 'select id,sdate,thing,status,homesnumber,rdate,tcost,scost,maintainer,smemo from maintain'
            result = service.query2(sql)
        else:
            sql = 'select id,sdate,thing,status,homesnumber,rdate,tcost,scost,maintainer,smemo from maintain where sdate=%s'
            result = service.query(sql, self.search.get())
        result = list(result)
        lst_result = []
        for item in result:
            item = list(item)
            item[5] = '' if item[5] == None else item[5]
            item[7] = '' if item[7] == None else item[7]
            lst_result.append(item)
        datautil.tv_data(self.tv, lst_result)

    def close(self):
        self.maintainwin.destroy()


class ModifyMainTain:
    def __init__(self, modify, id):
        self.modify = modify
        self.id = id
        self.modifymainwin = Toplevel()
        self.modifymainwin.geometry('1129x519+280+150')
        self.modifymainwin.overrideredirect(True)
        self.modifymainwin.config(background='white')
        image = PhotoImage(file='./image/modifymaintain.png')
        btnreturn = datautil.create_win(image, self.modifymainwin)
        btnreturn.config(command=self.close)
        # 报修物品
        Label(self.modifymainwin, text='报修物品*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.38,
                                                                                        anchor='w', width=80, height=40)
        self.ting = Entry(self.modifymainwin, font=16, highlightbackground='#aaaaaa',
                          highlightthickness=1, relief='flat')
        self.ting.place(relx=0.07, rely=0.43, width=300, height=40)
        # 报修单状态
        Label(self.modifymainwin, text='报修单状态*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.57,
                                                                                        anchor='w', width=100, height=40)
        self.statusv = StringVar()
        statuslst = ['等待处理', '已完结']
        self.statusv.set(statuslst[0])
        self.status = Combobox(self.modifymainwin, font=16, textvariable=self.statusv, values=statuslst)
        self.status.place(relx=0.07, rely=0.62, width=300, height=40)
        # 房门号
        Label(self.modifymainwin, text='房门号*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.78,
                                                                                            anchor='w', width=100,
                                                                                            height=80)
        self.homenumber = Entry(self.modifymainwin, font=16, highlightbackground='#aaaaaa',
                                highlightthickness=1, relief='flat')
        self.homenumber.place(relx=0.07, rely=0.82, width=300, height=40)
        # 报修时间
        Label(self.modifymainwin, text='报修时间*', font=16, anchor='w', bg='white').place(relx=0.37, rely=0.38,
                                                                                        anchor='w', width=80, height=40)
        self.sdate = Entry(self.modifymainwin, font=16, highlightbackground='#aaaaaa',
                           highlightthickness=1, relief='flat')
        self.           sdate.place(relx=0.37, rely=0.46, anchor='w', width=300, height=40)
        # 维修时间
        Label(self.modifymainwin, text='维修时间', font=16, anchor='w', bg='white').place(relx=0.37, rely=0.58,
                                                                                        anchor='w', width=80, height=40)
        self.rdate = Entry(self.modifymainwin, font=16, highlightbackground='#aaaaaa',
                           highlightthickness=1, relief='flat')
        self.rdate.place(relx=0.37, rely=0.65, anchor='w', width=300, height=40)

        # 预计花费
        Label(self.modifymainwin, text='预计花费*', font=16, anchor='w', bg='white').place(relx=0.37, rely=0.78,
                                                                                          anchor='w', width=80,
                                                                                          height=40)
        self.tcost = Entry(self.modifymainwin, font=16, highlightbackground='#aaaaaa',
                           highlightthickness=1, relief='flat')
        self.tcost.place(relx=0.37,  rely=0.85, anchor='w', width=300, height=40)
        # 实际花费
        Label(self.modifymainwin, text='实际花费', font=16, anchor='w', bg='white').place(relx=0.67, rely=0.38,
                                                                                        anchor='w', width=80, height=40)
        self.scost = Entry(self.modifymainwin, font=16, highlightbackground='#aaaaaa',
                           highlightthickness=1, relief='flat')
        self.scost.place(relx=0.67,rely=0.46, anchor='w', width=300, height=40)
        # 报修人
        Label(self.modifymainwin, text='报修人*', font=16, anchor='w', bg='white').place(relx=0.67, rely=0.56, anchor='w',
                                                                                       width=80, height=40)
        self.maintainer = Entry(self.modifymainwin, font=16, highlightbackground='#aaaaaa',
                                highlightthickness=1, relief='flat')
        self.maintainer.place(relx=0.67, rely=0.65, anchor='w', width=300, height=40)
        # 维修详情
        Label(self.modifymainwin, text='维修详情', font=16, anchor='w', bg='white').place(relx=0.67, rely=0.78, anchor='w',
                                                                                       width=80, height=40)
        self.smemo = Text(self.modifymainwin, font=16, highlightbackground='#aaaaaa',
                          highlightthickness=1, relief='flat')
        self.smemo.place(relx=0.67,  rely=0.85, anchor='w', width=300, height=40)

        # 保存按钮
        btn_save = Button(self.modifymainwin, text='保存', bg='#5B9BD5', fg='white', font=16)
        btn_save.place(
            relx=0.91, rely=0.94, anchor='center', width=60, height=40)

        if modify and self.id != 0:  # modify==True ，执行修改
            sql = 'select thing,status,homesnumber,sdate,rdate,tcost,scost,maintainer,smemo from maintain where id=%s'
            result = service.query(sql, self.id)
            self.ting.insert(0, result[0][0])
            self.statusv.set(result[0][1])
            self.homenumber.insert(0, result[0][2])
            self.sdate.insert(0, result[0][3])
            self.rdate.insert(0, '' if result[0][4] == None else result[0][4])
            self.tcost.insert(0, result[0][5])
            self.scost.insert(0, '' if result[0][6] == None else result[0][6])
            self.maintainer.insert(0, result[0][7])
            self.smemo.insert('0.0', result[0][8])
            btn_save.config(command=self.modifymaintain)

        elif modify == False and self.id == 0:
            btn_save.config(command=self.insertmaintain)
        else:
            showinfo('提示', '请先选择一条要修改的数据')
        self.modifymainwin.mainloop()

    def insertmaintain(self):
        if self.ting.get() == '' or self.sdate.get() == '':
            showwarning('警告', '报修物品或报修时间不允许为空!')
            return False
        sql = 'insert into maintain(thing,status,homesnumber,sdate,rdate,tcost,scost,maintainer,smemo)values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values = (self.ting.get(), self.statusv.get(), self.homenumber.get(), self.sdate.get(),
                  None if self.rdate.get() == '' else self.rdate.get(), self.tcost.get(),
                  None if self.scost.get() == '' else self.scost.get(), self.maintainer.get(),
                  self.smemo.get('0.0', END))
        result = service.exec(sql, values)
        if result > 0:
            showinfo('提示', '新增报修信息成功')
            self.modifymainwin.destroy()
        else:
            showerror('错误', '新增报修信息失败')
            self.modifymainwin.destroy()

    def modifymaintain(self):

        if self.ting.get() == '' or self.sdate.get() == '':
            showwarning('警告', '报修物品或报修时间不允许为空!')
            return False
        sql = 'update maintain set thing=%s,status=%s,homesnumber=%s,sdate=%s,rdate=%s,tcost=%s,scost=%s,maintainer=%s,smemo=%s where id=%s'
        values = (self.ting.get(), self.statusv.get(), self.homenumber.get(), self.sdate.get(),
                  None if self.rdate.get() == '' else self.rdate.get(), self.tcost.get(),
                  None if self.scost.get() == '' else self.scost.get(), self.maintainer.get(),
                  self.smemo.get('0.0', END), self.id)
        result = service.exec(sql, values)
        if result > 0:
            showinfo('提示', '修改报修信息成功')
            self.modifymainwin.destroy()
        else:
            showerror('错误', '修改报修信息失败')
            self.modifymainwin.destroy()

    def close(self):
        self.modifymainwin.destroy()
