#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
@project: apiAutoTest
@file: hooks.py
@author: zy7y
@time: 2021/2/27
@site: https://cnblogs.com/zy7y
@github: https://github.com/zy7y
@gitee: https://gitee.com/zy7y
@desc: 扩展方法, 2021/02/27
关于exec执行python代码可查阅资料：https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p23_executing_code_with_local_side_effects.html

"""
import time
import base64
import json
import hashlib


def exec_func(func: str) -> str:
    """执行函数(exec可以执行Python代码)
    :params func 字符的形式调用函数
    : return 返回的将是个str类型的结果
    """
    # 得到一个局部的变量字典，来修正exec函数中的变量，在其他函数内部使用不到的问题
    loc = locals()
    exec(f"result = {func}")
    return str(loc['result'])


def get_current_highest():
    """获取当前时间戳"""
    return int(time.time())


def sum_data(a, b):
    """计算函数"""
    return a + b


def md5_encode(character, coding='utf-8'):
    """MD5加密"""
    encstr = character.encode(coding)
    md5_enc = hashlib.md5()
    md5_enc.update(encstr)
    return md5_enc.hexdigest()


def base64_encode(character, coding='utf-8'):
    encstr = character.encode(coding)
    base64_enc = base64.b64encode(encstr)
    return base64_enc.decode()


def base64_decode(character, coding='utf-8'):
    dec_str = character.encode(coding)
    base64_dec = base64.b64decode(dec_str)
    return base64_dec.decode()


if __name__ == '__main__':
    # 实例, 调用无参数方法 get_current_highest
    result = exec_func("get_current_highest()")
    print(result)

    # 调用有参数方法 sum_data
    print(exec_func("sum_data(1,3)"))
    # 调用md5加密方法
    print(md5_encode("123"))
    # 调用时间戳
    print(get_current_highest())
    # 调用base64加密
    print(base64_encode("456"))
    # 调用base64解密
    print(base64_decode("NDU2"))
