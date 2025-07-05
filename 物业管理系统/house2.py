from tkinter import *
import service, datautil


class HouseWin():
    def __init__(self):
        self.id = 0
        self.housewin = Toplevel()
        self.housewin.overrideredirect(True)
        image = PhotoImage(file='./image/house.png')
        # self.adminwin.title('http://www.management/admin')
        self.housewin.geometry('1129x519+280+150')
        self.housewin.config(background='white')
        btnreturn = datautil.create_win(image, self.housewin)
        btnreturn.config(command=self.close)
        Label(self.housewin, text='搜索', font=16, bg='white').place(x=10, y=180, width=50, height=40)
        self.search = Entry(self.housewin, font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.search.place(x=60, y=180, width=200, height=40)

        # 添加记录
        Button(self.housewin, text='查询', bg='#5B9BD5', fg='white', font=16,
               relief='flat', command=self.query).place(x=270, y=180, width=60, height=40)

        # 创建TreeView
        lst = ['id', 'num', 'dep', 'type', 'area', 'sell', 'unit', 'floor', 'direction', 'ownerid', 'memo']
        lst_name = ['序号', '门牌号', '楼号', '类型', '地区', '出售状况', '单元', '楼层', '朝向', '业主编号', '备注']
        self.tv = datautil.tv(self.housewin, lst, lst_name)  # 使用 tv 函数创建 Treeview
        self.tv.place(x=10, y=230, width=1129, height=286)  # 设置宽度为1129
        # 自适应调整列宽
        for i, col in enumerate(lst):
            self.tv.column(col, minwidth=0, width=100, stretch=True)  # 初始宽度100,允许自适应

        # self.tv.bind('<Double-Button-1>', self.get_selected_item_data)
        self.query()
        self.housewin.mainloop()

    def query(self):
        if self.search.get() == '':
            sql = 'select id,num,dep,type,area,sell,unit, floor,direction,ownerid,memo from house'
            result = service.query2(sql)
        else:
            sql = 'select id,num,dep,type,area,sell,unit, floor,direction,ownerid,memo from house where num=%s'
            result = service.query(sql, self.search.get())
        result = list(result)
        new_result = []
        for item in result:
            item = list(item)
            if len(item) > 10:
                item[10] = '' if item[10] is None else item[10]
            new_result.append(item)
        datautil.tv_data(self.tv, new_result)

    def close(self):
        self.housewin.destroy()
