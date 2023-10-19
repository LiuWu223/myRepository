# -*- encoding=utf8 -*-
"""
#测试目的：对fail应用重测
"""
import logging
import pytest
import threading
from third_app_api import *
from self_api.common_api import common
from self_api.task_info import *

if not os.path.exists('monkey_log'):
    os.mkdir('monkey_log')

if not os.path.exists('fail_jpg'):
    os.mkdir('fail_jpg')

# 常用变量
fail_app_list = []
fail_pkg_list = []

# 获取当前用例名
case_name = __file__.split(os.sep)[-1]

# 获取fail_app列表
if os.path.exists('fail_log.txt'):
    with open("fail_log.txt", "r", encoding='utf-8') as f1:  # 打开文本
        data = f1.readlines()  # 读取文本
        for s in data:
            fail_app_list.append(s.split('*')[0])
            fail_pkg_list.append(s.split('*')[1])

logging.info(fail_app_list)

# 删除原fail_log
if os.path.exists('fail_log.txt'):
    os.remove('fail_log.txt')
    logging.info("已删除") 

count = 1
popup_app_list = ["同意", "同意并继续", "我同意", "已满14岁", "同意开启", "确定", "允许", "是", "跳过", "同意并使用", "监护人已同意", "监护人同意", "使用时允许",
                  "同意并进入", "使用时允许", "同意并开始使用", "已满14周岁", "使用时允许"]


def watch_check():
    for i in range(10000000):
        try:
            if d(resourceId="com.seewo.studystation.launcher:id/verifyCloseView").exists:
                d(resourceId="com.seewo.studystation.launcher:id/verifyCloseView").click()
                logging.info("watch_check:第{}次监控".format(i))
                sleep(2)

            if d(text="确定").exists:
                d(text="确定").click()
                sleep(2)

            if d(resourceId="com.seewo.studystation.launcher:id/pointConfirmButton").exists:
                d(resourceId="com.seewo.studystation.launcher:id/pointConfirmButton").click()
                logging.info("watch_check:第{}次监控".format(i))
                sleep(2)

            if d(text="下次再说").exists:
                d(text="下次再说").click()
                sleep(2)

            if d(text="android:id/aerr_app_info").exists:
                common.save_screenshot(case_name, "应用停止运行.jpg")
                err_text = d(resourceId="android:id/alertTitle").get_text()
                AppTest.write_log(err_text)
                logging.info("watch_check:第{}次监控".format(i))
                if d(text="关闭应用").exists:
                    d(text="关闭应用").click()
                    sleep(2)
            sleep(1.5)
        except:
            pass


thread_hi = threading.Thread(target=watch_check, daemon=True)
thread_hi.start()


def app_install(app_name, app_pkg):
    """
    函数功能: 应用下载安装测试
    返回值: 测试结果, True or False
    """
    logging.info("app_install_1.打开商店")
    d.app_start(AppVar.PKG_appstore, use_monkey=True)
    sleep(5)

    logging.info("app_install_2.搜索应用")
    d(resourceId="com.seewo.studystation.update:id/searchView").click(timeout=20)
    sleep(3)
    if d(text="重试").exists:
        d(text="重试").click()
        sleep(3)
    d.send_keys(app_name)
    sleep(3)
    d.send_action("search")
    sleep(4)

    if d(resourceId="com.seewo.studystation.update:id/appNameTv", text=app_name).exists:
        d(resourceId="com.seewo.studystation.update:id/appNameTv", text=app_name).click()
        sleep(4)

        if d(text="申请").exists:
            logging.info(app_name + '*' + app_pkg + '*' + "未推送")
            # d(text="申请").click()
            # sleep(3)
            # d(text="发送申请").click()
            # sleep(3)
        elif d(text="下载").exists:
            logging.info("app_install_3.开始下载")
            d(text="下载").click()
            sleep(3)

        logging.info("app_install_4.检查是否下载安装成功")
        down_res = d(text="打开").wait(timeout=500)
        with pytest.assume:
            assert down_res, app_name + "下载安装失败"
        logging.info("将失败应用写入日志中")
        if not down_res:
            AppTest.write_log(app_name + '*' + app_pkg + '*' + '下载安装失败\n')
            common.save_screenshot(case_name, app_name + "下载安装失败.jpg")
        common.back_home()
        sleep(3)
        return down_res
    else:
        logging.info(app_name + "未搜到")
        AppTest.write_log(app_name + '*' + app_pkg + '*' + '已下架\n')
        common.back_home()
        sleep(3)
        return False


def app_function(app_name, app_pkg):
    """
    函数功能: 应用基本功能测试
    """
    cmd_monkey = "adb -s " + device_id + " shell monkey -p " + app_pkg + \
                 " --ignore-crashes -v --pct-touch 100 --throttle 200 500 > monkey_log" + os.sep + app_name + \
                 "_monkey_log.txt"
    logging.info("app_function_1.打开应用")
    d.app_start(app_pkg, use_monkey=True)
    sleep(20)

    logging.info("app_function_2.点击打开应用时可能出现的弹窗")
    for i in range(5):
        for popup in popup_app_list:
            if d(text=popup).exists:
                d(text=popup).click()
                sleep(5)
                break

    logging.info("step3.运行monkey测试")
    logging.info(cmd_monkey)
    subprocess.run(cmd_monkey, shell=True)
    sleep(5)
    d.app_start(app_pkg, use_monkey=True)
    sleep(10)

    logging.info("app_function_3.判断应用是否出现闪退")
    with pytest.assume:
        assert (AppTest.check_exit()), app_name + "应用出现闪退"
    logging.info("将失败应用写入log中")
    if not AppTest.check_exit():
        AppTest.write_log(app_name + '*' + app_pkg + '*' + '应用出现闪退\n')
        common.save_screenshot(case_name, app_name + "闪退.jpg")

    logging.info("app_function_4.判断应用是否停止运行")
    with pytest.assume:
        assert (AppTest.check_stop()), app_name + "应用出现停止运行"
    logging.info("将失败应用写入log中")
    if not AppTest.check_stop():
        AppTest.write_log(app_name + '*' + app_pkg + '*' + '应用出现停止运行\n')
        common.save_screenshot(case_name, app_name + "停止运行.jpg")
        d(text="关闭应用").click()
        sleep(3)

    logging.info("app_function_5.返回桌面，卸载app")
    common.back_home()
    sleep(2)
    os.system("adb -s " + device_id + " uninstall " + app_pkg)
    sleep(5)


@pytest.mark.repeat(len(fail_app_list))
@pytest.mark.flaky(reruns=0)
def test_app_fuc():
    """
    函数功能: 应用基本功能测试
    """
    global count
    logging.info(count)

    if len(fail_app_list) > 0:
        app_name = fail_app_list[count - 1]
        app_pkg = fail_pkg_list[count - 1]
        
        # 判断电池电量
        if AppTest.get_battery_percent() is not None and AppTest.get_battery_percent() < 20:
            if d.info.get('screenOn'):
                d.screen_off()
                sleep(7200)
                d.screen_on()
                sleep(5)
            else:
                d.screen_on()
                sleep(5)

        logging.info("开始测试第" + str(count) + "个应用：" + app_name)
        common.back_home()
        sleep(2)
        count += 1
        logging.info("*******开始下载安装测试*******")
        if app_install(app_name, app_pkg):
            logging.info("*******开始应用功能测试*******")
            app_function(app_name, app_pkg)
        else:
            logging.info(app_name + "下载安装失败, 继续下一个")
    else:
        logging.info("*******本次没有待测试的应用，测试中止*******")

