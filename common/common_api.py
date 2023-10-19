# -*- encoding=utf8 -*-
"""
#公共的API接口
#创建人：杨刚
#创建日期：2023/7/26
"""

import os
from time import sleep
from datetime import datetime
from self_api.task_info import d


class common:
    """
    # 常用公共方法
    """
    @classmethod
    def get_time_now(cls):
        """
        #获取当前时间点
        #返回值：时间点字符串
        """
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace("-", "_").replace(" ", "_").replace(":", "_")
        return time_now

    @classmethod
    def back_home(cls):
        """
        # 退出app,返回桌面
        """
        d.press("back")
        d.press("back")
        sleep(1)
        d.press("back")
        d.press("back")
        sleep(1)
        d.press("home")
        sleep(1)

    @classmethod
    def write_log(cls, case_name, info):
        """
        #写入异常日志
        """
        if not os.path.exists('log'):
            os.mkdir('log')
        with open('log' + os.sep + 'fail_log.txt', 'a', encoding='utf-8') as f:
            f.write(case_name + '_' + cls.get_time_now() + '_' + info + '\n')

    @classmethod
    def save_screenshot(cls, case_name, png):
        """
        #保存截图
        """
        if not os.path.exists('fail_jpg'):
            os.mkdir('fail_jpg')
        d.screenshot('fail_jpg' + os.sep + case_name + '_' + cls.get_time_now() + '_' + png)

