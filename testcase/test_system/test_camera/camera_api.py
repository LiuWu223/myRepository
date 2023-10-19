# -*- encoding=utf8 -*-
"""
#camera模块相关的API接口
#创建人：杨刚
#创建日期：2023/7/25
"""
import logging
from self_api.task_info import *


class CameraVar:
    """
    # camera模块测试常用变量
    # camera_pkg:camera包名;
    # shutter_button:拍摄按钮;
    # switch_button:摄像头切换按钮
    # photo_view:照片预览
    # cmd_camera_id: 获取当前正在使用哪一个摄像头
    """
    camera_pkg = 'com.android.camera2'
    shutter_button = 'com.android.camera2:id/shutter_button'
    switch_button = 'com.android.camera2:id/btn_camera_switch'
    photo_view = 'com.android.camera2:id/rounded_thumbnail_view'
    cmd_camera_id = 'dumpsys media.camera | grep "Camera ID"'


class CameraTest:
    """
    # camera模块测试常用方法
    """

    @classmethod
    def take_photo(cls):
        """
        # 单次拍照
        """
        logging.info("开始拍照")
        if d(resourceId=CameraVar.shutter_button).exists:
            d(resourceId=CameraVar.shutter_button).click()
        else:
            logging.info("未找到拍照按钮")

    @classmethod
    def multi_shots(cls):
        """
        # 连拍
        """
        logging.info("开始连拍")
        if d(resourceId=CameraVar.shutter_button).exists:
            d(resourceId=CameraVar.shutter_button).long_click(2)
        else:
            logging.info("未找到拍照按钮")

    @classmethod
    def switch_camera(cls):
        """
        # 摄像头切换
        """
        logging.info("开始切换摄像头")
        if d(resourceId=CameraVar.switch_button).exists:
            d(resourceId=CameraVar.switch_button).click()
        else:
            logging.info("未找到切换按钮")

    @classmethod
    def photo_view(cls):
        """
        # 照片预览
        """
        logging.info("进入照片预览")
        if d(resourceId=CameraVar.photo_view).exists:
            d(resourceId=CameraVar.photo_view).click()
        else:
            logging.info("未找到照片预览按钮")

    @classmethod
    def get_camera_id(cls):
        """
        # 获取当前使用的camera id
        """
        camera_id = None
        logging.info("开始获取当前camera id")
        output = d.shell('dumpsys media.camera | grep "Camera ID"').output
        if 'Camera ID: 0' in output:
            camera_id = 0
            logging.info("当前正在camera 0预览界面")
        elif 'Camera ID: 1' in output:
            camera_id = 1
            logging.info("当前正在camera 1预览界面")
        else:
            logging.info("当前不在相机预览界面")
        return camera_id
