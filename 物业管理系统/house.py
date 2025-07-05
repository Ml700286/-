from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import Combobox, Treeview
import service, datautil


class HouseWin:
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
        Button(self.housewin, text='+添加记录', bg='green', font=16,
               fg='white', relief='flat', command=lambda: ModifyHouseWin(False, 0)).place(x=340, y=180, width=100,
                                                                                          height=40)
        Button(self.housewin, text='编辑', bg='orange', font=16,
               fg='white', relief='flat', command=lambda: ModifyHouseWin(True, self.id)).place(x=450, y=180, width=60,
                                                                                               height=40)
        Button(self.housewin, text='删除', bg='red', font=16,
               fg='white', relief='flat', command=self.delete).place(x=520, y=180, width=60, height=40)
        # 创建TreeView
        lst = ['id', 'num', 'dep', 'type', 'area', 'sell', 'unit', 'floor', 'direction', 'ownerid', 'memo']
        lst_name = ['序号', '门牌号', '楼号', '类型', '地区', '出售状况', '单元', '楼层', '朝向', '业主编号', '备注']

        self.tv = datautil.tv(self.housewin, lst, lst_name)  # 使用 tv 函数创建 Treeview
        self.tv.place(x=10, y=230, width=1129, height=286)  # 设置宽度为1129
        # 自适应调整列宽
        for i, col in enumerate(lst):
            self.tv.column(col, minwidth=0, width=100, stretch=True)  # 初始宽度100,允许自适应

        self.tv.bind('<Double-Button-1>', self.get_selected_item_data)
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
            item[10] = '' if item[10] == None else item[10]
            new_result.append(item)
        datautil.tv_data(self.tv, new_result)

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
            answer = askyesno('提示', '删除要删除房产吗?')
            if answer:
                sql = 'delete from house where id=%s'
                result = service.exec(sql, self.id)
                if result > 0:
                    showinfo('提示', '房产信息删除成功')
                else:
                    showerror('错误', '房产信息删除失败')

        else:
            showwarning('警告', '请先选择一条要删除的数据')

    def close(self):
        self.housewin.destroy()


class ModifyHouseWin():
    def __init__(self, modify, id):
        self.modify = modify
        self.id = id
        self.modifyhouse = Toplevel()
        self.modifyhouse.geometry('1129x519+280+150')
        self.modifyhouse.overrideredirect(True)
        self.modifyhouse.config(background='white')
        image = PhotoImage(file='./image/modifynotice.png')
        btnreturn = datautil.create_win(image, self.modifyhouse)
        btnreturn.config(command=self.close)

        # 页面布局
        # 门牌号
        Label(self.modifyhouse, text='门牌号*', font=16, anchor='w', bg='white').place(x=50, y=180, width=80, height=40)
        self.num = Entry(self.modifyhouse, font=16, highlightbackground='#aaaaaa',
                         highlightthickness=1, relief='flat')
        self.num.place(x=50, y=230, width=230, height=40)
        # 楼号
        Label(self.modifyhouse, text='楼号*', font=16, anchor='w', bg='white').place(x=50, y=280, width=80, height=40)
        self.dep = Entry(self.modifyhouse, font=16, highlightbackground='#aaaaaa',
                         highlightthickness=1, relief='flat')
        self.dep.place(x=50, y=330, width=230, height=40)
        # 类型
        Label(self.modifyhouse, text='类型*', font=16, anchor='w', bg='white').place(x=50, y=380, width=100, height=40)
        self.typev = StringVar()
        typelst = ['高层', '洋房', '别墅']
        self.typev.set(typelst[0])
        self.type = Combobox(self.modifyhouse, textvariable=self.typev, values=typelst)
        self.type.place(x=50, y=430, width=230, height=40)
        # 地区
        Label(self.modifyhouse, text='地区*', font=16, anchor='w', bg='white').place(x=320, y=180, width=100, height=40)
        self.area = Entry(self.modifyhouse, font=16, highlightbackground='#aaaaaa',
                          highlightthickness=1, relief='flat')
        self.area.place(x=320, y=230, width=230, height=40)
        # 出售状况
        self.sellv = StringVar()
        selllst = ['已售', '待售']
        self.sellv.set(selllst[0])
        Label(self.modifyhouse, text='出售状况*', font=16, anchor='w', bg='white').place(x=320, y=280, width=100,
                                                                                         height=40)
        self.sell = Combobox(self.modifyhouse, textvariable=self.sellv, values=selllst)
        self.sell.place(x=320, y=330, width=230, height=40)
        # 单元
        Label(self.modifyhouse, text='单元*', font=16, anchor='w', bg='white').place(x=320, y=380, width=100, height=40)
        self.unit = Entry(self.modifyhouse, font=16, highlightbackground='#aaaaaa',
                          highlightthickness=1, relief='flat')
        self.unit.place(x=320, y=430, width=230, height=40)
        # 楼层
        Label(self.modifyhouse, text='楼层*', font=16, anchor='w', bg='white').place(x=580, y=180, width=100, height=40)
        self.floor = Entry(self.modifyhouse, font=16, highlightbackground='#aaaaaa',
                           highlightthickness=1, relief='flat')
        self.floor.place(x=580, y=230, width=230, height=40)
        # 朝向
        Label(self.modifyhouse, text='朝向*', font=16, anchor='w', bg='white').place(x=580, y=280, width=100, height=40)
        self.direction = Entry(self.modifyhouse, font=16, highlightbackground='#aaaaaa',
                               highlightthickness=1, relief='flat')
        self.direction.place(x=580, y=330, width=230, height=40)
        # 业主编号
        Label(self.modifyhouse, text='业主编号*', font=16, anchor='w', bg='white').place(x=580, y=380, width=100,
                                                                                         height=40)
        self.owneridv = StringVar()
        ownerlst = self.query_owerid()
        self.owneridv.set(ownerlst[0])
        self.ownerid = Combobox(self.modifyhouse, textvariable=self.owneridv, values=ownerlst)
        self.ownerid.place(x=580, y=430, width=230, height=40)
        # 备注
        Label(self.modifyhouse, text='备注', font=16, anchor='w', bg='white').place(x=830, y=180, width=100, height=40)
        self.memo = Text(self.modifyhouse, font=16, highlightbackground='#aaaaaa',
                         highlightthickness=1, relief='flat')
        self.memo.place(x=830, y=230, width=230, height=180)
        # 按钮
        btn_save = Button(self.modifyhouse, text='保存', bg='#5B9BD5', fg='white', font=16)
        btn_save.place(x=1000, y=435, width=60, height=40)
        if modify and self.id != 0:
            sql = 'select num,dep,type,area,sell,unit,floor,direction,ownerid,memo from house where id=%s'
            result = service.query(sql, self.id)
            self.num.insert(0, result[0][0])
            self.dep.insert(0, result[0][1])
            self.typev.set(result[0][2])
            self.area.insert(0, result[0][3])
            self.sellv.set(result[0][4])
            self.unit.insert(0, result[0][5])
            self.floor.insert(0, result[0][6])
            self.direction.insert(0, result[0][7])
            self.owneridv.set(result[0][8])
            self.memo.insert('0.0', '' if result[0][9] == None else result[0][9])

            btn_save.config(command=self.update)
        elif modify == False and self.id == 0:
            btn_save.config(command=self.insert)
        else:
            showinfo('提示', '请先选择一条要修改的数据')

        self.modifyhouse.mainloop()

    def insert(self):
        num = self.num.get()
        dep = self.dep.get()
        type = self.typev.get()
        area = self.area.get()
        sell = self.sellv.get()
        unit = self.unit.get()
        floor = self.floor.get()
        direction = self.direction.get()
        ownerid = self.owneridv.get()
        memo = self.memo.get('0.0', END)
        if num == '' or dep == '' or area == '' or unit == '' or floor == '' or direction == '':
            showwarning('警告', '*内容为必填项')
            return False
        sql = 'insert into house(num,dep,type,area,sell,unit,floor,direction,ownerid,memo) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values = (num, dep, type, area, sell, unit, floor, direction, ownerid, memo)
        result = service.exec(sql, values)
        if result > 0:
            showinfo('提示', '添加房产信息成功')
            self.modifyhouse.destroy()
        else:
            showerror('错误', '新增房产信息失败')

    def update(self):
        num = self.num.get()
        dep = self.dep.get()
        type = self.typev.get()
        area = self.area.get()
        sell = self.sellv.get()
        unit = self.unit.get()
        floor = self.floor.get()
        direction = self.direction.get()
        ownerid = self.owneridv.get()
        memo = self.memo.get('0.0', END)
        if num == '' or dep == '' or area == '' or unit == '' or floor == '' or direction == '':
            showwarning('警告', '*内容为必填项')
            return False
        sql = 'update house set num=%s,dep=%s,type=%s,area=%s,sell=%s,unit=%s,floor=%s,direction=%s,ownerid=%s,memo=%s where id=%s'
        values = (num, dep, type, area, sell, unit, floor, direction, ownerid, memo, self.id)
        res = service.exec(sql, values)
        if res > 0:
            showinfo('提示', '修改房产信息成功')
            self.modifyhouse.destroy()
        else:
            showerror('错误', '修改房产信息失败')

    def query_owerid(self):
        sql = 'select ownerid from custom_account'
        result = service.query2(sql)
        lst = []
        for item in result:
            lst.append(item[0])
        return lst

    def close(self):
        self.modifyhouse.destroy()
