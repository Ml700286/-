import mysql.connector
import unittest

# 创建测试数据库连接
test_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="management"
)
cursor = test_db.cursor()