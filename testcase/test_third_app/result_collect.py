# -*- encoding=utf8 -*-
"""
#测试目的：收集最终测试结果，写入到表格中
"""
import csv
import datetime
import subprocess
from self_api.common_api import common
from self_api.task_info import *

# 常用变量
excel_file = './result_collect/' + common.get_time_now() + '_result_collect.csv'
result_title = ['序号', '测试日期', '机型', '系统版本', '应用名称', '应用包名', '应用版本', '测试结果', '问题备注']

if not os.path.exists('result_collect'):
    os.mkdir('result_collect')


def record_test_info(info):
    """
    #功能: 记录本次测试的应用信息
    #参数: 列表
    """
    with open(excel_file, 'a', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(info)


print("result_collect.py-1.先写入表格标题")
record_test_info(result_title)

# 常用变量
app_name_list = []
app_pkg_list = []
app_version_list = []

if os.path.exists('app_version.txt'):
    with open("app_version.txt", "r", encoding='utf-8') as f1:  # 打开文本
        data = f1.readlines()  # 读取文本
        for s in data:
            app_name_list.append(s.split('*')[0])
            app_pkg_list.append(s.split('*')[1])
            app_version_list.append(s.strip().split('*')[2])

# 获取测试日期
date01 = str(datetime.date.today())
print(date01)

# 获取测试版本号
cmd = "adb -s " + device_id + " shell getprop ro.build.display.id"
sys_version = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8").stdout.strip()

if os.path.exists('fail_log.txt'):
    with open("fail_log.txt", "r", encoding='utf-8') as f1:  # 打开文本
        fail_info = f1.read()  # 读取文本
        for i in range(len(app_name_list)):
            if app_name_list[i] in fail_info:
                test_result = 'fail'
                for d in fail_info.split():
                    if app_name_list[i] in d:
                        result_info = d.split('*')[-1]
                da = [i + 1, date01, device_type, sys_version, app_name_list[i], app_pkg_list[i], app_version_list[i],
                      test_result, result_info]
                record_test_info(da)
            else:
                da = [i + 1, date01, device_type, sys_version, app_name_list[i], app_pkg_list[i], app_version_list[i], "pass"]
                record_test_info(da)
else:
    for i in range(len(app_name_list)):
        da = [i + 1, date01, device_type, sys_version, app_name_list[i], app_pkg_list[i], app_version_list[i], "pass"]
        record_test_info(da)
