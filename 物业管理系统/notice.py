from tkinter import *
from tkinter.messagebox import *

import service, datautil


class Notice:
    def __init__(self):
        self.id = 0
        self.noticewin = Toplevel()
        self.noticewin.overrideredirect(True)
        image = PhotoImage(file='./image/notice.png')
        # self.adminwin.title('http://www.management/admin')
        self.noticewin.geometry('1129x519+280+150')
        self.noticewin.config(background='white')
        btnreturn = datautil.create_win(image, self.noticewin)
        btnreturn.config(command=self.close)

        Label(self.noticewin, text='搜索', font=16, bg='white').place(x=10, y=180, width=50, height=40)
        self.search = Entry(self.noticewin, font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.search.place(x=60, y=180, width=200, height=40)

        # 添加记录
        Button(self.noticewin, text='查询', bg='#5B9BD5', fg='white', font=16,
               relief='flat', command=self.query).place(x=270, y=180, width=60, height=40)
        Button(self.noticewin, text='+添加记录', bg='green', font=16,
               fg='white', relief='flat', command=lambda: ModifyNoticeWin(False, 0)).place(x=340, y=180, width=100,
                                                                                           height=40)
        Button(self.noticewin, text='编辑', bg='orange', font=16,
               fg='white', relief='flat', command=lambda: ModifyNoticeWin(True, self.id)).place(x=450, y=180, width=60,
                                                                                                height=40)
        Button(self.noticewin, text='删除', bg='red', font=16,
               fg='white', relief='flat', command=self.delete).place(x=520, y=180, width=60, height=40)
        # 创建TreeView
        lst = ['id', 'title', 'content', 'ndate', 'uper']
        lst_name = ['序号', '公告标题', '公告内容', '发布日期', '发布者']
        self.tv = datautil.tv(self.noticewin, lst, lst_name)  # 使用 tv 函数创建 Treeview
        self.tv.place(x=10, y=230, width=1129, height=286)  # 设置宽度为1129
        # 自适应调整列宽
        for i, col in enumerate(lst):
            self.tv.column(col, minwidth=0, width=100, stretch=True)  # 初始宽度100,允许自适应

        self.tv.bind('<Double-Button-1>', self.get_selected_item_data)
        self.query()

        self.noticewin.mainloop()

    def delete(self):
        if self.tv.focus():
            answer = askyesno('提示', '删除要删除公告吗?')
            if answer:
                sql = 'delete from notice where id=%s'
                result = service.exec(sql, self.id)
                if result > 0:
                    showinfo('提示', '公告信息删除成功')
                else:
                    showerror('错误', '公告信息删除失败')

        else:
            showwarning('警告', '请先选择一条要删除的数据')

    def get_selected_item_data(self, event):
        iid = self.tv.focus()
        if iid:
            item = self.tv.item(iid)
            values = item.get('values')
            self.id = values[0]
        else:
            self.id = 0

    def query(self):
        if self.search.get() == '':
            sql = 'select id,title,content,ndate,uper from notice'
            result = service.query2(sql)
        else:
            sql = 'select id,title,content,ndate,uper from notice where title like %s'
            result = service.query(sql, '%' + self.search.get() + '%')
        datautil.tv_data(self.tv, result)

    def close(self):
        self.noticewin.destroy()


class ModifyNoticeWin:
    def __init__(self, modify, id):
        self.modify = modify
        self.id = id
        self.modifynotice = Toplevel()
        self.modifynotice.geometry('1129x519+280+150')
        self.modifynotice.overrideredirect(True)
        self.modifynotice.config(background='white')
        image = PhotoImage(file='./image/modifynotice.png')
        btnreturn = datautil.create_win(image, self.modifynotice)
        btnreturn.config(command=self.close)
        # 页面布局
        Label(self.modifynotice, text='公告标题*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.37,
                                                                                          anchor='w', width=100,
                                                                                          height=40)
        self.title = Entry(self.modifynotice, font=16, highlightbackground='#aaaaaa',
                           highlightthickness=1, relief='flat')
        self.title.place(relx=0.07, rely=0.42, width=300, height=40)
        # 发布日期
        Label(self.modifynotice, text='发布日期*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.57,
                                                                                          anchor='w', width=60,
                                                                                          height=40)
        self.ndate = Entry(self.modifynotice, font=16, highlightbackground='#aaaaaa',
                           highlightthickness=1, relief='flat')
        self.ndate.place(relx=0.07, rely=0.62, width=300, height=40)
        # 公告发布者
        Label(self.modifynotice, text='公告发布者*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.78,
                                                                                            anchor='w', width=100,
                                                                                            height=40)
        self.uper = Entry(self.modifynotice, font=16, highlightbackground='#aaaaaa',
                          highlightthickness=1, relief='flat')
        self.uper.place(relx=0.07, rely=0.82, width=300, height=40)
        # 公告内容
        Label(self.modifynotice, text='公告内容*', font=16, anchor='w', bg='white').place(relx=0.47, rely=0.35,
                                                                                          width=100, height=40)
        self.content = Text(self.modifynotice, font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.content.place(relx=0.47, rely=0.44, width=400, height=200)
        # 保存按钮
        btn_save = Button(self.modifynotice, text='保存', bg='#5B9BD5', fg='white', font=16)
        btn_save.place(
            relx=0.80, rely=0.89, anchor='center', width=60, height=40)

        if modify and self.id != 0:
            sql = 'select title,content,ndate,uper from notice where id=%s'
            result = service.query(sql, self.id)
            print(result)
            self.title.insert(0, result[0][0])
            self.content.insert('0.0', result[0][1])
            self.ndate.insert(0, result[0][2])
            self.uper.insert(0, result[0][3])
            btn_save.config(command=self.update)
        elif modify == False and self.id == 0:
            btn_save.config(command=self.insert)
        else:
            showinfo('提示', '请先选择一条要修改的数据')

        self.modifynotice.mainloop()

    def update(self):
        title = self.title.get()
        ndate = self.ndate.get()
        uper = self.uper.get()
        content = self.content.get('0.0', END)
        if title == '' or ndate == '' or uper == '' or content == '':
            showwarning('警告', '公告标题、发布时间、发布者或者发布内容不允许为空')
            return False
        sql = 'update notice set title=%s,content=%s,ndate=%s,uper=%s where id=%s'
        values = (title, content, ndate, uper, self.id)
        result = service.exec(sql, values)
        if result > 0:
            showinfo('提示', '修改公告信息成功')
            self.modifynotice.destroy()
        else:
            showerror('错误', '修改公告信息失败')

    def insert(self):
        title = self.title.get()
        ndate = self.ndate.get()
        uper = self.uper.get()
        content = self.content.get('0.0', END)
        if title == '' or ndate == '' or uper == '' or content == '':
            showwarning('警告', '公告标题、发布时间、发布者或者发布内容不允许为空')
            return False
        sql = 'insert into notice(content,ndate,title,uper)values (%s,%s,%s,%s)'
        result = service.exec(sql, (content, ndate, title, uper))
        if result > 0:
            showinfo('提示', '新增公告成功')
            self.modifynotice.destroy()
        else:
            showerror('错误', '新增公告失败')

    def close(self):
        self.modifynotice.destroy()
