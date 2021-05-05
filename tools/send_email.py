# -*- coding: utf-8 -*-
# @Time    : 2021/5/3 15:08
# @Author  : RanyLra
# @Wechat  : RanY_Luck
# @File    : send_email.py
import email

import yagmail
from tools import logger
import zipfile
import os


class EmailServe:

    @staticmethod
    def zip_report(file_path: str, out_path: str):
        """
        压缩指定文件夹
        :param file_path: 目标文件夹路径
        :param out_path: 压缩文件保存路径+xxx.zip
        :return: 生成zip格式文件
        """
        zip = zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(file_path):
            # 去掉目录根路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(file_path, '')
            for filename in filenames:
                zip.write(os.path.join(path, filename), os.path.join(
                    fpath, filename))
        zip.close()

    @staticmethod
    def send_email(setting: dict, file_path):
        """
        入参一个关键字
        :param user: 发件人邮箱
        :param password: 邮箱授权码
        :param host: 发件人使用的邮箱服务 例如：smtp.163.com
        :param contents: 内容
        :param addressees: 收件人列表
        :param title: 邮件标题
        :param enclosures: 附件列表
        :param file_path: 需要压缩的文件夹
        :return : None
        """
        EmailServe.zip_report(
            file_path=file_path,
            out_path=setting['enclosures'])
        yag = yagmail.SMTP(
            setting['user'],
            setting['password'],
            setting['host'])
        # 发送邮件
        yag.send(
            setting['addressees'],
            setting['title'],
            setting['contents'],
            setting['enclosures'])
        # 关闭服务
        yag.close()
        logger.info("邮件发送成功")


if __name__ == '__main__':
    # EmailServe.zip_report('../report/html', '../report.zip')
    path = '../report/html', '../report.zip'
    EmailServe.send_email(email, path)
