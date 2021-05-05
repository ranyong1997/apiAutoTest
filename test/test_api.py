# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 22:14
# @Author  : RanyLra
# @Wechat  : RanY_Luck
# @File    : test_api.py


from .conftest import pytest

from api import BaseRequest
from tools.data_process import DataProcess


# @pytest.mark.flaky(reruns=2, reruns_delay=1)
# def test_main(cases, get_db):  # 使用数据库功能
#     # 发送请求
#     response, expect, sql = BaseRequest.send_request(cases)
#     # 执行sql
#     DataProcess.handle_sql(sql, get_db)
#     # 断言操作
#     DataProcess.assert_result(response, expect)


def test_main(cases):  # 不使用数据库功能
    # 发送请求
    response, expect, sql = BaseRequest.send_request(cases)
    # 断言操作
    DataProcess.assert_result(response, expect)
