# -*- encoding=utf8 -*-
import requests
import time
import base64
import hashlib
import json

# 时间格式
thisTime = time.strftime('%Y-%m-%d %H:%M:%S')
txt = "\t\t\t\t"
tabL = txt.expandtabs(2)


# 信息发送
def send_message(url, content):
    # CVTE企业机器人链接   群里面机器人地址
    # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ae6c6e34-5993-4f85-990a-7ee2c439defa"
    data = {
        "msgtype": "markdown",
        "markdown": {"content": content}
    }
    res = requests.post(url=url, json=data)
    print(type(res))
    if res.status_code == 200:
        print("send message sucessed")
        return "send message sucessed"
    else:
        print(res)
        return res


# 图片发送
def send_image_message(image_path):
    # CVTE企业机器人链接   群里面机器人地址
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ae6c6e34-5993-4f85-990a-7ee2c439defa"
    with open(image_path,'rb') as f:
        # 转换图片为base64格式
        base64_data = base64.b64encode(f.read())
        image_data = str(base64_data,'utf-8')
    with open(image_path,'rb') as f:
        # 获取图片的md5值
        md = hashlib.md5()
        md.update(f.read())
        image_md5 = md.hexdigest()

    headers = {"Content-Type":'application/json'}
    data = {
        'msgtype':'image',
        'image':{
            'base64':image_data,
            'md5':image_md5
        }
    }
    # 发送请求
    res = requests.post(url,headers=headers,json=data)
    if res.status_code == 200:
        print("send message sucessed")
        return "send message sucessed"
    else:
        print(res)
        return res
        
        
"""
文件发送
上传的文件限制：
~!要求文件大小在5B~20M之间
"""


# 企业机器人发送信息频率，20条/一分钟
def post_file(wx_url, id_url, file_path):
    # 本地文件路径
    # 企业微信机器人路径
    # wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ae6c6e34-5993-4f85-990a-7ee2c439defa"
    data = {'file':open(file_path,'rb')}
    # 请求id_url(将文件上传微信临时平台),返回media_id
    # https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=(企业微信机器人key)&type=file
    # id_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=ae6c6e34-5993-4f85-990a-7ee2c439defa&type=file'
    response = requests.post(url=id_url, files=data)
    print(response.text)
    json_res = response.json()
    media_id = json_res['media_id']
    data = {"msgtype": "file",
            "file": {"media_id": media_id}
            }
    # 发送文件
    result = requests.post(url=wx_url, json=data)
    print(result.status_code)


# 开始信息 #
"""
testName：测试名称
testNumber:指定测试次数
"""
def Start_Message(testName, testNumber):
    content = "<font color=\"warning\">测试报告" + tabL + "<font color=\"comment\">" + thisTime + "</font>" "</font>\n >测试名称：<font color=\"comment\">" + testName + "</font>\n 指定次数：<font color=\"info\">" + str(
        testNumber) + "</font>\n >状态：<font color=\"info\">开始执行</font>"
    send_message(content)

# 成功信息 #
"""
testName：测试名称
testNumber: 指定测试次数
testOutNumber: 完成次数
"""
def Succeed_Message(testName, testNumber, testOutNumber):
    content = "<font color=\"warning\">测试报告" + tabL + "<font color=\"comment\">" + thisTime + "</font>" "</font>\n >测试名称：<font color=\"comment\">" + testName + "</font>\n 指定次数：<font color=\"info\">" + str(
        testNumber) + "</font>\n >完成次数：<font color=\"info\">" + str(testOutNumber) + "</font>\n >状态：<font color=\"info\">完成</font>"
    send_message(content)

# 报错信息 #
"""
testName：测试名称
testNumber: 指定测试次数
testOutNumber: 完成次数
e：错误信息
"""
def Error_Message(testName, testNumber, testOutNumber, e):
    content = "<font color=\"warning\">测试报告" + tabL + "<font color=\"comment\">" + thisTime + "</font>" "</font>\n >测试名称：<font color=\"comment\">" + testName + "</font>\n >指定次数：<font color=\"info\">" + str(
        testNumber) + "</font>\n >完成次数：<font color=\"red\">" + str(
        testOutNumber) + "</font>\n >状态：<font color=\"red\">错误</font>\n >错误信息：<font color=\"red\">" + str(e) + "</font>"
    send_message(content)
if __name__ == '__main__':
    # 开始信息发送
    # Start_Message('1', '1')
    # 成功信息发送
    # Succeed_Message("11", 1, 1)
    # 错误信息发送
    # Error_Message("信息提醒_20230207测试", '测试1', '测试2', '测试3')
    # 图片发送
    # send_image_message(r'E:\机器人头像.png')
    # 图文发送
    # send_image_txt_message(r'E:\机器人头像.png')
    pass

