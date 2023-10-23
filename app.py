import csv
import os
import requests
from time import sleep  

def getThisIp():
    ip = os.popen('ipconfig').readlines()
    for i in ip:
        iss = i.find('IPv4 地址 . . . . . . . . . . . . :')
        if iss != -1:
            return i[i[iss:-1].find(':') + 5:-1]
    return 'not Ip'

def apps():
    # 接收用户传的用户ID，项目ID，项目的任务
    def record_test_info(info):
        """
        #功能: 记录本次测试的应用信息
        #参数: 列表
        """
        with open('task_list.csv', 'a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(info)
    ip = getThisIp()
    if os.path.exists('task_list.csv'):
        os.remove('task_list.csv')

    result_title = ['序号', 'devices号', '机型', '测试类型', '用例名', '应用序号_首', '应用序号_尾']
    record_test_info(result_title)
    # 写表
    # 请求查询用户信息接口，通过IP地址查询
    url = 'http://192.168.3.85:3000/auto_sw_admin_war/sy/syUser/selectByUserIp/' + ip
    response = requests.get(url)
    a = response.json()
    xx = a['data']
    print(xx)

    result_title = [str(xx['id']), str(xx['devices']), '--', 'test_third_app', 'test_App_Fuc_all.py', str(xx['tripartite']).split(',')[0], str(xx['tripartite']).split(',')[1]]
    record_test_info(result_title)
    os.system("python run_task.py")

if __name__ == '__main__':
    apps()
