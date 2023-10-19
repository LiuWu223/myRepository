# -*- encoding=utf8 -*-
import os
import subprocess
from self_api.task_info import *
from self_api.EnterpriseWeChatInfrom import *

# 常用变量
url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ae6c6e34-5993-4f85-990a-7ee2c439defa"
id_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=ae6c6e34-5993-4f85-990a-7ee2c439defa&type=file'


def send_report():
    """
    函数功能: 调用群机器人发送测试报告
    """
    app_num = app_last - app_first

    # 获取测试版本号
    cmd = "adb -s " + device_id + " shell getprop ro.build.display.id"
    sys_version = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8").stdout.strip()

    if os.path.exists('fail_log.txt'):
        with open("fail_log.txt", "r", encoding='utf-8') as f1:  # 打开文本
            fail_info = f1.readlines()  # 读取文本
        fail_num = len(fail_info)
        fail_percent = str(round((app_num - fail_num) / app_num * 100, 2)) + '%'
        print(fail_percent)
        send_message(url, "系统版本号: " + sys_version + "\n" + "本次测试的应用个数: " + str(app_num) + "\n" + "fail的应用个数: " + str(fail_num)
                     + "\n" + "通过率: " + fail_percent + "\n" + "详情见如下报告:")
    else:
        send_message(url, "系统版本号: " + sys_version + "\n" + "本次测试的应用个数: " + str(app_num) + "\n" + "fail的应用个数: 0" + "\n"
                     + "通过率: 100%" + "\n" + "详情见如下报告:")
    # if os.path.exists('reports'):
    #     report_list = sorted(os.listdir('./reports'))
    #     post_file('./reports' + os.sep + report_list[-2])
    # if os.path.exists('fail_log.txt'):
    #     post_file('./fail_log.txt')
    if os.path.exists('result_collect'):
        result_list = sorted(os.listdir('./result_collect'))
        post_file(url, id_url, './result_collect' + os.sep + result_list[-1])


send_report()
