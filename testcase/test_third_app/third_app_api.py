# -*- encoding=utf8 -*-
"""
#三方应用模块相关的API接口
#创建人：杨刚
#创建日期：2023/8/10
"""
import subprocess
from time import sleep

from self_api.task_info import *


class AppVar:
    """
    # 三方应用模块测试常用变量
    # app_file:app详情表格;
    # PKG_appstore:希沃应用商店包名;
    """
    PKG_appstore = 'com.seewo.studystation.update'
    app_file = './all_app_list.xlsx'


class AppTest:
    """
    # 三方应用测试常用方法
    """

    @classmethod
    def check_stop(cls):
        """
        #功能: 检查应用是否停止运行
        #返回值: 无
        """
        sleep(3)
        if d(text="关闭应用").exists:
            return False
        else:
            return True

    @classmethod
    def check_exit(cls):
        """
        #功能: 检查应用是否闪退
        #返回值: 无
        """
        sleep(3)
        if d(resourceId="com.seewo.studystation.launcher:id/appIconView").exists:
            return False
        else:
            return True

    @classmethod
    def get_battery_percent(cls):
        """
        #功能: 获取当前电池电量
        #返回值: 电池电量百分比
        """

        res = subprocess.run("adb -s " + device_id + " shell dumpsys battery", shell=True, stdout=subprocess.PIPE,
                             encoding="utf-8").stdout.split('\n')
        for s in res:
            if 'level' in s:
                battery_percent = int(s.split()[-1])
                return battery_percent

    @classmethod
    def write_log(cls, info):
        """
        #写入异常日志
        """
        with open('fail_log.txt', 'a', encoding='utf-8') as f:
            f.write(info)


