# -*- encoding=utf8 -*-
"""
#获取任务信息
"""
import logging
from time import sleep
from self_api.task_info import *


def main():
    os.system("adb devices")
    sleep(2)
    print("设置测试机不休眠")
    os.system("adb -s " + device_id + " shell settings put system screen_off_timeout 1000000000")
    sleep(2)
    os.system("cd testcase/" + test_type + "&& pytest " + case_name)


if __name__ == "__main__":
    main()


