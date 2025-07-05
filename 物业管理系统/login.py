# coding:utf-8
from tkinter import *
from tkinter.messagebox import *
from PIL import Image, ImageTk
import service, adminmain, adminmain2

class LoginWin:
    def __init__(self):
        self.loginwin = Tk()    # Toplevel()从登陆页面开始,TK()从管理员页面开始
        self.loginwin.geometry('1401x808+0+0')
        self.loginwin.title('http://management/login')

        # 加载图像并调整大小以适应窗口
        self.image = Image.open('./image/login1.png')
        self.image = self.image.resize((1401, 808), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        # 显示图像
        Label(self.loginwin, image=self.photo).place(x=0, y=0)

        self.loginwin.resizable(False, False)
        # 用户名和密码的文本框
        self.username = Entry(self.loginwin, font=16)
        self.username.place(x=663, y=410, width=230, height=28)

        self.password = Entry(self.loginwin, font=16, show='*')
        self.password.place(x=663, y=470, width=230, height=28)
        # 业主登录 还是管理员登录
        lst = ['业主登录', '管理员登录']
        self.logintypev = StringVar()
        self.logintypev.set(lst[0])
        self.logincustom = Radiobutton(self.loginwin, font=16, bg='#E7E6E6', variable=self.logintypev,
                                       text=lst[0], value=lst[0])
        self.logincustom.place(x=575, y=507, width=100, height=34)
        self.admin = Radiobutton(self.loginwin, font=16, bg='#E7E6E6', variable=self.logintypev,
                                 text=lst[1], value=lst[1])
        self.admin.place(x=715, y=507, width=150, height=34)
        # 登录按钮
        Button(self.loginwin, text='登   录', fg='#0070C0', bg='#4DCAF2',
               relief='flat', font=16, command=self.login).place(x=560, y=550, width=306, height=51)
        self.loginwin.mainloop()

    def login(self):
        # 非空验证
        if self.username.get() == '' or self.password.get() == '':
            showwarning('警告', '用户名或密码不允许为空')
            return False
        if self.logintypev.get() == '业主登录':
            sql = 'select ownerid from custom_account where username=%s and password=%s'
        else:
            sql = 'select id from admins where name=%s and password=%s'
        result = service.query(sql, self.username.get(), self.password.get())
        if len(result) > 0 and self.logintypev.get() == '业主登录':
            showinfo('提示', '业主登录成功')
            adminmain2.loginobj = self
            adminmain2.adminid = result[0][0]
            self.loginwin.withdraw()
            self.username.delete(0, END)
            self.password.delete(0, END)
            adminmain2.AdminMainWin()
        elif len(result) > 0 and self.logintypev.get() == '管理员登录':
            showinfo('提示', '管理员登录成功')
            adminmain.loginobj = self
            adminmain.adminid = result[0][0]
            self.loginwin.withdraw()
            self.username.delete(0, END)
            self.password.delete(0, END)
            adminmain.AdminMainWin()
        else:
            showerror('错误', '用户名或密码不正确！')


LoginWin()
