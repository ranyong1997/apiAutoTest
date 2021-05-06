# -*- coding: utf-8 -*-
# @Time    : 2021/5/2 22:26
# @Author  : RanyLra
# @Wechat  : RanY_Luck
# @File    : run.py
import os
import shutil
from test.conftest import pytest
from tools import logger
from tools.read_file import ReadFile
from tools.send_email import EmailServe

report = ReadFile.read_config('$.file_path.report')
logfile = ReadFile.read_config('$.file_path.log')
file_path = ReadFile.read_config('$.file_path')
s_email = ReadFile.read_config('$.email')


def run():
    if os.path.exists('report/'):
        shutil.rmtree(path='report/')
    logger.add(logfile, enqueue=True, encoding='utf-8')
    logger.info("""
                 _    _         _      _____         _   
  __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_ 
 / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
| (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_ 
 \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
      |_|                                            
      Starting      ...     ...     ...
    """)
    pytest.main(args=['test/test_api.py', f'--alluredir={report}/data'])

    # 生成本地生成报告
    os.system(f'allure generate {report}/data -o {report}/html --clean')
    logger.success('报告已生成,请查收')
    # 启动allure服务
    # os.system(f'allure serve {report}/data')  # 该方法会生成一个http服务 挂载报告文件 阻塞线程 (如果需要压缩报告,请注释)


def zip_report():
    """打包报告"""
    EmailServe.zip_report('report/html', 'report.zip')


def send_email():
    """发送邮件"""
    EmailServe.send_email(s_email, file_path['report'])


def del_report():
    """删除本地附件"""
    os.remove(s_email['enclosures'])
    logger.success('附件删除完成')


if __name__ == '__main__':
    run()
    zip_report()
    send_email()
    # del_report()
