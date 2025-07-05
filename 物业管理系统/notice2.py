from tkinter import *

import service,datautil
class Notice:
    def __init__(self):
        self.id=0
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
               relief='flat',command=self.query).place(x=270, y=180, width=60, height=40)

        # 创建TreeView
        lst = ['id','title','content','ndate','uper']
        lst_name = ['序号','公告标题','公告内容','发布日期','发布者']
        self.tv = datautil.tv(self.noticewin, lst, lst_name)  # 使用 tv 函数创建 Treeview
        self.tv.place(x=10, y=230, width=1129, height=286)  # 设置宽度为1129
        # 自适应调整列宽
        for i, col in enumerate(lst):
            self.tv.column(col, minwidth=0, width=100, stretch=True)  # 初始宽度100,允许自适应

        # self.tv.bind('<Double-Button-1>', self.get_selected_item_data)
        self.query()

        self.noticewin.mainloop()

    def query(self):
        if self.search.get()=='':
            sql='select id,title,content,ndate,uper from notice'
            result=service.query2(sql)
        else:
            sql='select id,title,content,ndate,uper from notice where title like %s'
            result=service.query(sql,'%'+self.search.get()+'%')
        datautil.tv_data(self.tv,result)

    def close(self):
        self.noticewin.destroy()

