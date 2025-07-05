# 物业管理系统 (Property Management System)

![系统界面截图](image/login1.png)

## 项目简介
基于Python Tkinter和MySQL开发的小区物业管理系统，主要功能包括：
- 业主端：个人信息管理、房屋信息查询、在线报修申请、社区公告查看
- 管理端：业主信息管理、房产数据维护、报修工单处理、公告发布


## 项目特点
- 🏠 采用MVC架构设计，前端使用Tkinter GUI，后端连接MySQL数据库
- 👨‍💻 双角色系统：管理员(全功能CRUD)/业主(信息查询与报修)
- 📱 适配笔记本屏幕（14寸）的响应式界面布局
- 📊 Excel测试用例覆盖核心业务流程

## 原始项目参考
[B站教学视频](https://www.bilibili.com/video/BV1aA411s74n/)

## 学习目标
- 理解Python与MySQL的连接原理
- 掌握Tkinter组件布局与事件处理
- 学习基础数据库CRUD操作实现

## 本地化修改
1. **数据库配置**  
   - 修改`datautil.py`中的MySQL连接参数：
     ```python
     conn = pymysql.connect(
         host='localhost',
         user='root,  
         password='123456', 
         database='management'
     )
     ```

2. **界面优化**  
   - 调整所有窗口为适应14寸笔记本的尺寸（800x600）
   - 统一放大登录页面字体（从10号调整为12号）
   - 重构表单控件布局，避免显示不全

## 代码结构
物业管理系统/
├── image/ # 图片资源
├── account.py # 业主账户管理
├── account2.py # 管理员账户管理
├── adminmain.py # 业主主界面
├── adminmain2.py # 管理员主界面
├── datautil.py # 数据库连接工具类
├── house.py # 业主房屋信息模块
├── house2.py # 管理员房屋管理
├── inspection.py # 业主巡检查询
├── inspection2.py # 管理员巡检管理
├── maintain.py # 业主报修功能
├── maintain2.py # 管理员报修处理
├── notice.py # 业主公告查看
├── notice2.py # 管理员公告发布
└── 物业管理系统_测试用例.xlsx # 功能测试案例

## 运行指南
1. 执行MySQL初始化脚本（见`schema.sql`）
2. 安装依赖：
   ```bash
   pip install pymysql tkinter
3.启动系统：
  python login.py


## 学习心得

通过参与本项目，我获得了以下关键技能：

1. **数据库连接**
   - 掌握了使用 `pymysql` 库进行 Python 与 MySQL 数据库的连接方法。

2. **GUI 开发**
   - 学习了 Tkinter 的网格布局管理和事件绑定机制。

3. **事务管理**
   - 理解了数据库事务的原理，并在物业管理系统中实践了其应用。

4. **测试验证**
   - 学习了编写测试用例来确保系统功能的完整性和正确性。

提示：管理员测试账号 admin/admin | 业主测试账号 qwe/123456

