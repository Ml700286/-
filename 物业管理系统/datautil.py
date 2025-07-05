# coding:utf-8
from tkinter import *
from tkinter.ttk import Treeview


def tv_data(treeview, result):  # 向treeview中添加数据
    # 定义斑马线颜色
    odd_row_color = "#f2f2f2"  # 奇数行颜色
    even_row_color = "#ffffff"  # 偶数行颜色（默认白色）
    treeview.tag_configure('odd', background=odd_row_color)
    treeview.tag_configure('even', background=even_row_color)
    # 添加数据之前先去检查，treeview中是否有数据
    item_num = treeview.get_children()
    if len(item_num) > 0:
        for item in treeview.get_children():
            treeview.delete(item)
    # 向treeview中添加数据

    for idx, item in enumerate(result):  # 查询结果
        # 使用 'iid' 参数为每个项指定一个唯一的标识符
        # 这里我们简单地使用索引值，但在实际应用中，你可能需要使用更有意义的ID
        iid = str(idx)  # idx的值从0开始
        treeview.insert('', 'end', iid=iid, values=item, tags=('even' if idx % 2 == 0 else 'odd'))


def tv(win, lst, lst_name):
    treev = Treeview(win, columns=lst, show='headings')
    for i in range(len(lst)):
        treev.heading(lst[i], text=lst_name[i])
    return treev


def adjust_column_width(treev):
    # 自适应调整列宽和高度
    for col in treev['columns']:
        max_width = max(
            [len(str(treev.item(item, 'values')[treev['columns'].index(col)])) for item in treev.get_children()])
        treev.column(col, width=max_width * 10)  # 根据内容长度调整宽度

    # 调整高度（如果有内容换行）
    for item in treev.get_children():
        values = treev.item(item, 'values')
        max_lines = max([len(str(value).split('\n')) for value in values])
        treev.item(item, height=max_lines * 20)  # 根据换行次数调整高度


def create_win(image, win):
    Label(win, image=image).place(x=0, y=0, width=1451, height=519)
    btnreturn = Button(win, text='返回', bg='#5B9BD5', fg='white', font=16)
    btnreturn.place(x=300, y=15, width=60, height=40)
    return btnreturn
# 返回值是一个按钮对象
