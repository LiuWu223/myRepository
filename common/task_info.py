import os
import pandas as pd
import requests
import uiautomator2 as u2


# 获取任务信息
pwd = os.getcwd().split('testcase')[0]
print(pwd)
excel_file = pwd + os.sep + 'task_list.csv'
data = pd.read_csv(excel_file, encoding="gbk")
task_info = data.to_dict('records')[0]
print(task_info)
device_id = str(task_info['devices号'])
print(device_id)
test_type = task_info['测试类型']
print(test_type)
case_name = task_info['用例名']
print(case_name)
device_type = task_info['机型']
print(device_type)
app_first = int(task_info['应用序号_首'])
print(app_first)
app_last = int(task_info['应用序号_尾'])
print(app_last)

d = u2.connect(device_id)