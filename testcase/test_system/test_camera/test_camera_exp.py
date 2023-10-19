# -*- encoding=utf8 -*-
"""
#测试场景：相机连拍测试
#测试前置：1.打开相机app
#测试步骤：1.获取当前使用的摄像头ID
#        2.长按拍照键连拍
#判断条件：3.进入照片预览查看是否连拍成功
#测试后置：1.退出相机app
#创建人：杨刚
#创建日期：2023/7/25
"""
from time import sleep
from camera_api import *
import pytest
from self_api.common_api import common
from self_api.task_info import *

# 获取当前用例名
case_name = __file__.split(os.sep)[-1]


class Test_camera:

    @staticmethod
    def setup_method():
        logging.info("测试类前置方法---setup_method---")
        logging.info("setup_method_1.打开camera")
        d.app_start(CameraVar.camera_pkg, use_monkey=True)
        sleep(2)

    def test_multi_shots(self):
        """
        # 连拍测试
        """
        logging.info('----测试用例：multi_shots开始------')
        camera_id = CameraTest.get_camera_id()
        if camera_id == 0:
            CameraTest.multi_shots()
            sleep(2)
        elif camera_id == 1:
            CameraTest.switch_camera()
            sleep(2)
            CameraTest.multi_shots()
            sleep(2)
        else:
            logging.info("打开camera失败，用例中止")
            exit(1)

        logging.info("判断测试结果")
        CameraTest.photo_view()
        result = d(textContains='连拍').wait(timeout=11)
        with pytest.assume:
            assert result, "连拍失败"
        if not result:
            logging.info("将失败信息写入日志中")
            common.write_log(case_name, "camera连拍失败")
            common.save_screenshot(case_name, "camera连拍失败.jpg")

    @staticmethod
    def teardown_method():
        logging.info("测试类后置方法---teardown_method---")
        logging.info("teardown_method_1.退出camera")
        common.back_home()
        sleep(2)

