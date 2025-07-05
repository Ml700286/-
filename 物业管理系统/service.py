# coding:utf-8
import pymysql


def open():
    db = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='management', port=3306)
    return db


def exec(sql, values):
    db = open()
    cursor = db.cursor()
    try:
        cursor.execute(sql, values)
        db.commit()  # 提交事务
        return 1
    except:
        db.rollback()  # 回滚
        return 0
    finally:
        cursor.close()
        db.close()


def query(sql, *keys):  # *keys
    db = open()
    cursor = db.cursor()
    cursor.execute(sql, keys)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def query2(sql):
    db = open()
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


if __name__ == '__main__':
    pass
