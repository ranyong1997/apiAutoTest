# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 22:09
# @Author  : RanyLra
# @Wechat  : RanY_Luck
# @File    : conftest.py


import pytest

from tools.db import DB
from tools.read_file import ReadFile


@pytest.fixture(scope='session')
def get_db():
    """
    :return:
    """
    try:
        db = DB()
        yield db
    finally:
        db.close()


@pytest.fixture(params=ReadFile.read_testcase())
def cases(request):
    """
    用例数据，测试方法参数入参该方法 case即可，实现同样的参数化，目前来看相较于
    @pytest.mark.paramtrize 更简洁
    :param request:
    :return:
    """
    return request.param
