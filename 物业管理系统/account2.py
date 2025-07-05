from tkinter import *
import service,datautil
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
               relief='flat',command=self.query).place(x=270, y=180, width=60, height=40)

        # 创建TreeView
        lst = ['ownerid','username','password','carid']
        lst_name = ['序号', '用户名', '密码', '车牌号', ]
        self.tv = datautil.tv(self.accountwin, lst, lst_name)  # 使用 tv 函数创建 Treeview
        self.tv.place(x=10, y=230, width=1129, height=286)  # 设置宽度为1129
        # 自适应调整列宽
        for i, col in enumerate(lst):
            self.tv.column(col, minwidth=0, width=100, stretch=True)  # 初始宽度100,允许自适应

        # self.tv.bind('<Double-Button-1>', self.get_selected_item_data)
        self.query()
        self.accountwin.mainloop()


    def close(self):
        self.accountwin.destroy()
    def query(self):
        if self.search.get()=='':
            sql='select * from custom_account'
            result=service.query2(sql)
        else:
            sql='select * from custom_account where username like %s'
            result=service.query(sql,'%'+self.search.get()+'%')
        result=list(result)
        result_lst=[]
        for item in result:
            item=list(item)
            item[2]='****'
            result_lst.append(item)
        datautil.tv_data(self.tv,result_lst)
