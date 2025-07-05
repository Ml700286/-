from tkinter import *
import service, datautil


class MainTainWin():
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

        # 创建TreeView
        lst = ['id', 'sdate', 'thing', 'status', 'homesnumber', 'rdate', 'tcost', 'scost', 'maintainer', 'smemo']
        lst_name = ['序号', '报修日期', '报修物品', '状态', '房门号', '维修日期', '预计花费', '实际花费', '报修人',
                    '报修详情']
        self.tv = datautil.tv(self.maintainwin, lst, lst_name)  # 使用 tv 函数创建 Treeview
        self.tv.place(x=10, y=230, width=1129, height=286)  # 设置宽度为1129
        # 自适应调整列宽
        for i, col in enumerate(lst):
            self.tv.column(col, minwidth=0, width=100, stretch=True)  # 初始宽度100,允许自适应

        # self.tv.bind('<Double-Button-1>', self.get_selected_item_data)
        self.query()
        self.maintainwin.mainloop()

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
