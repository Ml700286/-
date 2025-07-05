from tkinter import *
from tkinter.messagebox import *
import service, datautil


class Inspection:
    def __init__(self):
        self.id = 0
        self.inspectionwin = Toplevel()
        self.inspectionwin.overrideredirect(True)
        image = PhotoImage(file='./image/inspection.png')
        # self.adminwin.title('http://www.management/admin')
        self.inspectionwin.geometry('1129x519+280+150')
        self.inspectionwin.config(background='white')
        btnreturn = datautil.create_win(image, self.inspectionwin)
        btnreturn.config(command=self.close)
        Label(self.inspectionwin, text='搜索', font=16, bg='white').place(x=10, y=180, width=50, height=40)
        self.search = Entry(self.inspectionwin, font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.search.place(x=60, y=180, width=200, height=40)

        # 添加记录
        Button(self.inspectionwin, text='查询', bg='#5B9BD5', fg='white', font=16,
               relief='flat', command=self.query).place(x=270, y=180, width=60, height=40)
        Button(self.inspectionwin, text='+添加记录', bg='green', font=16,
               fg='white', relief='flat', command=lambda: ModifyInspectionWin(False, 0)).place(x=340, y=180, width=100,
                                                                                               height=40)
        Button(self.inspectionwin, text='编辑', bg='orange', font=16,
               fg='white', relief='flat', command=lambda: ModifyInspectionWin(True, self.id)).place(x=450, y=180,
                                                                                                    width=60, height=40)
        Button(self.inspectionwin, text='删除', bg='red', font=16,
               fg='white', relief='flat', command=self.delete).place(x=520, y=180, width=60, height=40)
        # 创建TreeView
        lst = ['id', 'person', 'type', 'ttime', 'conductor', 'party', 'result', 'memo']
        lst_name = ['序号', '巡查人', '类别', '时间', '处理人', '当事人', '巡查结果', '备注']
        self.tv = datautil.tv(self.inspectionwin, lst, lst_name)  # 使用 tv 函数创建 Treeview
        self.tv.place(x=10, y=230, width=1129, height=286)  # 设置宽度为1129
        # 自适应调整列宽
        for i, col in enumerate(lst):
            self.tv.column(col, minwidth=0, width=100, stretch=True)  # 初始宽度100,允许自适应

        self.tv.bind('<Double-Button-1>', self.get_selected_item_data)
        self.query()
        self.inspectionwin.mainloop()

    def close(self):
        self.inspectionwin.destroy()

    def query(self):
        if self.search.get() == '':
            sql = 'select * from inspection'
            result = service.query2(sql)
        else:
            sql = 'select * from inspection where person like %s'
            result = service.query(sql, '%' + self.search.get() + '%')
        lst = list(result)
        result_lst = []
        for item in lst:
            item = list(item)
            item[7] = '' if item[7] == None else item[7]
            result_lst.append(item)

        datautil.tv_data(self.tv, result_lst)

    def get_selected_item_data(self, event):
        iid = self.tv.focus()
        if iid:
            item = self.tv.item(iid)
            values = item.get('values')
            self.id = values[0]
            print(self.id)
        else:
            self.id = 0

    def delete(self):
        if self.tv.focus():
            answer = askyesno('提示', '删除要删除公告吗?')
            if answer:
                sql = 'delete from inspection where id=%s'
                result = service.exec(sql, self.id)
                if result > 0:
                    showinfo('提示', '保安保洁信息删除成功')
                else:
                    showerror('错误', '保安保洁信息删除失败')

        else:
            showwarning('警告', '请先选择一条要删除的数据')


class ModifyInspectionWin:
    def __init__(self, modify, id):
        self.modify = modify
        self.id = id
        self.modifyinspection = Toplevel()
        self.modifyinspection.geometry('1129x519+280+150')
        self.modifyinspection.overrideredirect(True)
        self.modifyinspection.config(background='white')
        image = PhotoImage(file='./image/modifyinspection.png')

        btnreturn = datautil.create_win(image, self.modifyinspection)
        btnreturn.config(command=self.close)
        # 巡查人
        Label(self.modifyinspection, text='巡查人*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.37,
                                                                                            anchor='w', width=80,
                                                                                            height=40)
        self.person = Entry(self.modifyinspection, font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.person.place(relx=0.07, rely=0.43, width=300, height=40)
        # 类别
        Label(self.modifyinspection, text='类别*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.57,
                                                                                          anchor='w', width=100,
                                                                                          height=40)
        self.type = Entry(self.modifyinspection, font=16, highlightbackground='#aaaaaa',
                          highlightthickness=1, relief='flat')
        self.type.place(relx=0.07, rely=0.62, width=300, height=40)
        # 时间
        Label(self.modifyinspection, text='时间*', font=16, anchor='w', bg='white').place(relx=0.07, rely=0.78,
                                                                                          anchor='w', width=100,
                                                                                          height=80)
        self.ttime = Entry(self.modifyinspection, font=16, highlightbackground='#aaaaaa',
                           highlightthickness=1, relief='flat')
        self.ttime.place(relx=0.07, rely=0.82, width=300, height=40)
        # 处理人
        Label(self.modifyinspection, text='处理人*', font=16, anchor='w', bg='white').place(relx=0.38, rely=0.38,
                                                                                            anchor='w', width=80,
                                                                                            height=40)

        self.conductor = Entry(self.modifyinspection, font=16, highlightbackground='#aaaaaa',
                               highlightthickness=1, relief='flat')
        self.conductor.place(relx=0.38, rely=0.46, anchor='w', width=300, height=40)
        # 当事人
        Label(self.modifyinspection, text='当事人*', font=16, anchor='w', bg='white').place(relx=0.38, rely=0.58,
                                                                                            anchor='w', width=80,
                                                                                            height=40)
        self.party = Entry(self.modifyinspection, font=16, highlightbackground='#aaaaaa',
                           highlightthickness=1, relief='flat')
        self.party.place(relx=0.38, rely=0.66, anchor='w', width=300, height=40)
        # 巡查结果
        Label(self.modifyinspection, text='巡查结果*', font=16, anchor='w', bg='white').place(relx=0.38, rely=0.78,
                                                                                              anchor='w', width=80,
                                                                                              height=40)
        self.result = Entry(self.modifyinspection, font=16, highlightbackground='#aaaaaa',
                            highlightthickness=1, relief='flat')
        self.result.place(relx=0.38, rely=0.86, anchor='w', width=300, height=40)
        # 备注
        Label(self.modifyinspection, text='备注', font=16, anchor='w', bg='white').place(relx=0.70, rely=0.38,
                                                                                         anchor='w', width=80,
                                                                                         height=40)
        self.memo = Text(self.modifyinspection, font=16, highlightbackground='#aaaaaa',
                         highlightthickness=1, relief='flat')
        self.memo.place(relx=0.70, rely=0.46, anchor='w', width=300, height=40)
        # 保存按钮
        btn_save = Button(self.modifyinspection, text='保存', bg='#5B9BD5',
                          fg='white', font=16)
        btn_save.place(
            relx=0.94, rely=0.87, anchor='center', width=60, height=40)
        if modify and self.id != 0:
            sql = 'select person,type,ttime,conductor,party,result,memo from inspection where id =%s'
            result = service.query(sql, self.id)
            self.person.insert(0, result[0][0])
            self.type.insert(0, result[0][1])
            self.ttime.insert(0, result[0][2])
            self.conductor.insert(0, result[0][3])
            self.party.insert(0, result[0][4])
            self.result.insert(0, result[0][5])
            self.memo.insert('0.0', '' if result[0][6] == None else result[0][6])

            btn_save.config(command=self.update)
        elif modify == False and self.id == 0:
            btn_save.config(command=self.insert)
        else:
            showinfo('提示', '请先选择一条要修改的数据')
        self.modifyinspection.mainloop()

    def update(self):
        person = self.person.get()
        type = self.type.get()
        ttime = self.ttime.get()
        conductor = self.conductor.get()
        party = self.party.get()
        result = self.result.get()
        memo = self.memo.get('0.0', END)
        if person == '' or type == '' or ttime == '' or conductor == '' or party == '' or result == '':
            showwarning('警告', '*内容为必填项')
            return False
        sql = 'update inspection set person=%s,type=%s,ttime=%s,conductor=%s,party=%s,result=%s,memo=%s where id=%s'
        values = (person, type, ttime, conductor, party, result, memo, self.id)
        res = service.exec(sql, values)
        if res > 0:
            showinfo('提示', '修改保安保洁信息成功')
            self.modifynotice.destroy()
        else:
            showerror('错误', '修改保安保法信息失败')

    def insert(self):
        person = self.person.get()
        type = self.type.get()
        ttime = self.ttime.get()
        conductor = self.conductor.get()
        party = self.party.get()
        result = self.result.get()
        memo = self.memo.get('0.0', END)
        if person == '' or type == '' or ttime == '' or conductor == '' or party == '' or result == '':
            showwarning('警告', '*内容为必填项')
            return False
        sql = 'insert into inspection(person,type,ttime,conductor,party,result,memo) values (%s,%s,%s,%s,%s,%s,%s)'
        values = (person, type, ttime, conductor, party, result, memo)
        res = service.exec(sql, values)
        if res > 0:
            showinfo('提示', '添加保安保洁信息成功')
            self.modifyinspection.destroy()
        else:
            showerror('错误', '新增保安保洁信息失败')

    def close(self):
        self.modifyinspection.destroy()
