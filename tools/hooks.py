# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 14:19
# @Author  : RanyLra
# @Wechat  : RanY_Luck
# @File    : hooks.py

import time
import base64
import hashlib


def exec_func(func: str) -> str:
    """
    执行函数(exec可以执行python代码)
    :param func: 字符的形式调用函数
    :return: 返回的将是个str类型的结果
    """
    # 得到一个局部变量字典，来修正exec函数中的变量，在其他函数内部使用不到的问题
    loc = locals()
    exec(f"result = {func}")
    return str(loc['result'])  # 可能会有个bug 先试试 不行的话 用json.dumps 转下


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


def md5_encode2(appVersion: str = '1.33.0', openid: str = '',
                key: str = 'eef02eb6258996ccab6e49e6e7ad94f'):
    """MD5加密(openid+ts+key)"""
    # appVersion = '1.33.0'
    # openid = ''
    ts = get_current_highest()
    # key = 'eef02eb6258996ccab6e49e6e7ad94f'
    sign = md5_encode(openid + str(ts) + key)
    md5_enc = hashlib.md5()
    md5_enc.update(sign.encode('utf-8'))
    # print("appVersion=" + appVersion + "\n"
    #       + "openid=" + openid + "\n"
    #       + "sign=" + sign + "\n"
    #       + "ts=" + str(ts))
    # return sign
    return {"appVersion": appVersion, "openid": openid, "sign": sign, "ts": str(ts)}


if __name__ == '__main__':
    # md5_encode2()
    print(exec_func("md5_encode2()"))
    # 实例, 调用无参数方法 get_current_highest
    print(exec_func("get_current_highest()"))
    # 调用有参数方法 sum_data
    print(exec_func("sum_data(1,3)"))
