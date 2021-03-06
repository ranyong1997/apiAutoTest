# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 16:56
# @Author  : RanyLra
# @Wechat  : RanY_Luck
# @File    : data_process.py


from tools import logger, extractor, convert_json, rep_expr, allure_step
from tools.read_file import ReadFile


class DataProcess:
    response_dict = {}
    header = ReadFile.read_config('$.request_headers')

    @classmethod
    def save_response(cls, key: str, value: object) -> None:
        """
        保存实际响应
        :param key: 保存字典中key，一般使用用例编号
        :param value: 保存字典中的value,使用json献映
        :return: 返回最终保存结果
        """
        cls.response_dict[key] = value
        logger.info(f'添加key:{key},对应value:{value}')

    @classmethod
    def handle_path(cls, path_str: str) -> str:
        """
        路径参数处理
        :param path_str: 带提取表达式的字符串 /&$.case_005_data.id&/stats/&$.case_005.data.create_time&
        上述内容解析为：从响应字典中提取到case_005字典里datazi字典里的id的值，假设是500，后面&$.case_005.data.create_time& 类似，最终提取结果为：
        :return: /500/state/123456
        """
        # /&$.case_005.data.id&/state/&$.case_005.data.create_time&
        return rep_expr(path_str, cls.response_dict)

    @classmethod
    def handle_header(cls, header_str: str) -> dict:
        """
        处理header,将用例中的表达式处理后,追加到基础header中
        :param header_str: 用例栏中的header
        :return: 返回header
        """
        if header_str == '':
            header_str = '{}'
        cls.header.update(cls.handle_data(header_str))
        return cls.header

    @classmethod
    def handler_files(cls, file_obj: str) -> object:
        """
        file对象处理方法
        :param file_obj: 上传文件使用，格式：接口中文件参数的名称："文件路径地址"/["文件地址1","文件地址2"]
        :return: {"files":["C:\\Users\\ranyong\\Desktop\\b.jpg", "C:\\Users\\ranyong\\Desktop\\c.jpg"]}
        """
        if file_obj == '':
            return
        for k, v in convert_json(file_obj).items():
            # 多文件上传
            if isinstance(v, list):
                files = []
                for path in v:
                    files.append((k, (open(path, 'rb'))))
            else:
                # 单文件上传
                files = {k: open(v, 'rb')}
        return files

    @classmethod
    def handle_data(cls, variable: str) -> dict:
        """
        请求数据处理
        :param variable: 请求数据，传入的是可换成字典/json的字符串，其中可以包含变量表达式
        :return: 处理之后的json/dict类型的字典数据
        """
        if variable == '':
            return
        data = rep_expr(variable, cls.response_dict)
        variable = convert_json(data)
        return variable

    @classmethod
    def handle_sql(cls, sql: str, db: object):
        """
        处理sql,并将结果写在响应字典中
        :param sql: sql语句
        :param db: 数据库名
        :return: 写到响应字典中
        """
        if sql not in ['no', '']:
            sql = rep_expr(sql, DataProcess.response_dict)
        else:
            sql = None
        allure_step('运行sql', sql)
        logger.info(sql)
        if sql is not None:
            # 查后置sql
            result = db.fetch_one(sql)
            allure_step('sql执行结果', result)
            logger.info(f'结果：{result}')
            if result is not None:
                # 将查询结果添加到响应字典里面，作用在接口响应的内容某个字段，直接和数据库某个字段比对，在预期结果中
                # 使用同样的语法提取即可
                DataProcess.response_dict.update(result)

    @classmethod
    def assert_result(cls, response: dict, expect_str: str):
        """
        预期结果实际结果断言方式
        :param response: 实际响应结果
        :param expect_str: 预期响应内容，从excel中读取
        :return: None
        """
        # 后置sql变量控制
        expect_str = rep_expr(expect_str, DataProcess.response_dict)
        expect_dict = convert_json(expect_str)
        index = 0
        for k, v in expect_dict.items():
            # 获取需要断言的实际结果部分
            actual = extractor(response, k)
            index += 1
            logger.info(
                f'第{index}个断言', f'实际结果:{actual} || 预期结果:{v} \n断言结果 {actual == v}')
            allure_step(f'第{index}个断言', f'实际结果:{actual}=预期结果:{v}')
            try:
                assert actual == v
            except AssertionError:
                raise AssertionError(
                    f'第{index}个断言失败 -|- 实际结果:{actual} || 你的预期结果: {v}')


if __name__ == '__main__':
    DataProcess()
