# -*- coding: UTF-8 -*-

import sys, getopt
import requests
import base64


# API地址
url = "http://127.0.0.1:5000/api/v1/detection/"
# 图片地址
file_path = '/home/wen/PycharmProjects/test00_1/Fingers_v0.5/images/000003.jpg'
# 图片名
file_name = file_path.split('/')[-1]
# 二进制打开图片
file = open(file_path, 'rb')
# 拼接参数
files = {'file': (file_name, file, 'image/jpg')}
# 身份验证？
email = '13798282351@qq.com'
password = '123456'
# 模型参数信息,可不提供,有默认值
top_b = 10
bottom_b = 30
left_b = 0
right_b = 0
formData = {'top_b': top_b,
            'bottom_b': bottom_b,
            'left_b': left_b,
            'right_b': right_b, }
# 发送post请求到服务器端
r = requests.post(url, files=files, auth=(email, password), data=formData)
# 获取服务器返回的图片，字节流返回
result = r.content
# 字节转换成图片
img = base64.b64decode(result)
file = open('test.jpg', 'wb')
file.write(img)
file.close()
