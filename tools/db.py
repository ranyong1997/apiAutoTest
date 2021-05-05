# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 17:23
# @Author  : RanyLra
# @Wechat  : RanY_Luck
# @File    : db.py

import pymysql

from tools.read_file import ReadFile


class DB:
    mysql = ReadFile.read_config('$.database')

    def __init__(self):
        """初始化连接Mysql"""
        self.connection = pymysql.connect(
            host=self.mysql.get('host', 'host'),
            port=self.mysql.get('port', 'port'),
            user=self.mysql.get('user', 'user'),
            password=self.mysql.get('password', 'password'),
            db=self.mysql.get('db_name', 'db_name'),
            charset=self.mysql.get('charset', 'utf8mb4'),
            cursorclass=pymysql.cursors.DictCursor
        )
    # def __init__(self):
    #     """初始化连接Mysql"""
    #     self.connection = pymysql.connect(
    #         host=self.mysql.get('host', 'localhost'),
    #         port=self.mysql.get('port', 3306),
    #         user=self.mysql.get('user', 'root'),
    #         password=self.mysql.get('password', '123456'),
    #         db=self.mysql.get('db_name', 'test'),
    #         charset=self.mysql.get('charset', 'utf8mb4'),
    #         cursorclass=pymysql.cursors.DictCursor
    #     )

    def fetch_one(self, sql: str) -> object:
        """查询数据，查一条"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            # 使用commit解决查询数据出现概率查错问题
            self.connection.commit()
        return result

    def close(self):
        """关闭数据库连接"""
        self.connection.close()


if __name__ == '__main__':
    print(ReadFile.read_config('$.database'))
    DB()
