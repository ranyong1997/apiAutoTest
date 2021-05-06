# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 16:42
# @Author  : RanyLra
# @Wechat  : RanY_Luck
# @File    : read_file.py

import yaml
import xlrd
from tools import extractor


class ReadFile:
    config_dict = None

    @classmethod
    def get_config_dict(cls, config_path: str = './config/config.yaml') -> dict:
        """
        读取配置文件，并且转换成字典
        :param config_path: 配置文件地址，默认当前使用该目录下config/config.yaml
        :return: cls.config_dict
        """
        if cls.config_dict is None:
            # 指定编码风格解决，win下跑代码抛出错误
            with open(config_path, 'r', encoding='utf-8') as file:
                cls.config_dict = yaml.load(
                    file.read(), Loader=yaml.FullLoader)
        return cls.config_dict

    @classmethod
    def read_config(cls, expr: str = '.') -> dict:
        """
        默认读取config目录下config.yaml配置文件，根据传递的expr jsonpath表达式可任意返回配置项
        :param expr: 提取表达式，使用jsonpath语法，默认值提取整个读取的对象
        :return: 根据表达式返回的值
        """
        return extractor(cls.get_config_dict(), expr)

    @classmethod
    def read_testcase(cls):
        """
        读取excel格式的测试用例
        :return: data_list - pytest参数化可用的数据
        """
        data_list = []
        book = xlrd.open_workbook(cls.read_config('$.file_path.test_case'))
        # 读取第一个sheet页
        table = book.sheet_by_index(0)
        for nrow in range(1, table.nrows):  # 忽略首行
            # 每行第4列，判断是否运行
            if table.cell_value(nrow, 4) != '否':  # 每行第4列等于否将不读取内容
                value = table.row_values(nrow)
                value.pop(4)
                data_list.append(list(value))
        return data_list
