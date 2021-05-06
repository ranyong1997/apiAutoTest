# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 14:19
# @Author  : RanyLra
# @Wechat  : RanY_Luck
# @File    : hooks.py
import json
import time
import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


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
    time = get_current_highest()
    ts = int(round(time))
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


def add_to_32(text):
    while len(text) % 16 != 0:
        text += "\0"
    return text


def decrypt(key, msg):
    key = add_to_32(key)
    decode = base64.b64decode(msg)
    aeskey = base64.b64decode(key)
    Cryptor = AES.new(aeskey, AES.MODE_ECB)
    plain_text = Cryptor.decrypt(decode)
    bin_decrypt_result = unpad(plain_text, AES.block_size)  # 输出的是二进制Unicode编码
    b = bin_decrypt_result.decode('utf8')
    return b


def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return value


def encrypt(key, data):
    data = json.dumps(data).encode('utf-8')  # 对数据进行utf-8编码
    key = base64.b64decode(key)
    cryptor = AES.new(add_to_16(key), AES.MODE_ECB)  # 创建一个新的AES实例
    ciphertext = cryptor.encrypt(pad(data, 32))
    return base64.b64encode(ciphertext)


def headers():
    """请求头加密MD5"""
    appVersion = "1.33.0"
    openId = ""
    time = get_current_highest()
    ts = int(round(time))
    key = "eef02eb6258996ccab6e49e6e7ad94f"
    value = openId + str(ts) + key
    md5 = hashlib.md5()
    md5.update(value.encode("utf8"))
    sign = md5.hexdigest()
    # header = {"appVersion": appVersion, "sign": sign, "openId": openId, "ts": str(ts)}
    header = {"sign": sign, "openId": openId, "ts": str(ts)}
    return header


if __name__ == '__main__':
    print(get_current_highest())
    # md5_encode2()
# print(exec_func("md5_encode2()"))
# # 实例, 调用无参数方法 get_current_highest
# print(exec_func("get_current_highest()"))
# # 调用有参数方法 sum_data
# print(exec_func("sum_data(1,3)"))
# print(base64.b64decode("kJrOctnrtdj0obkMkdDMfVptvJYEi9BgiZP/m5T5n84="))
