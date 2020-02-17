#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : xywy.py
# @Time     : 20-2-17 上午9:10
# @Author   : zkx
# @Email    : zkx9810@163.com
# @Site     : https://zkx98.github.io
# @Software : PyCharm


import requests
import re
from urllib.parse import urlencode


# 获取疾病链接
def get_disease_link():
    # 使用全局变量
    global url
    global parameter
    # 防止死循环
    n = 1000
    while n:
        n -= 1
        # 请求参数dict格式转url格式
        url_parameter = urlencode(parameter)
        # 获取链接返回的内容
        print(url + "?" + url_parameter)
        data = requests.get(url + "?" + url_parameter).text
        # print(type(content))
        # 将返回数据中的'\'换为''空
        data = re.sub(r'[\\]', '', data)
        # 截取返回数据在"url":与",之间的数据
        # 即疾病的网址 list类型
        data = re.findall(r'"url":"(.+?)",', data)
        print(type(data), len(data))
        print(data)
        # 获取疾病网址个数不为0
        if len(data) != 0:
            # 请求页数 + 1 继续循环进行下页请求
            parameter["page"] = int(parameter["page"]) + 1
        # 获取疾病网址个数为0
        else:
            print("letter:", parameter["letter"], "page:", parameter["page"], "空")
            # 跳出循环
            break
    return True


# 请求地址 string类型
url = "http://jib.api.xywy.com/GetJibInfo/getJibInfoByLetter"
# 请求参数 dict类型
parameter = {
    "callback": "jsoncallback",
    "letter": "A",
    "page": "1",
    "pageSize": "50"
}


if __name__ == '__main__':
    # 按首字母循环查询疾病——A-Z
    for i in range(65, 91):
        print(chr(i))
        # 修改请求字母
        parameter["letter"] = chr(i)
        # 重置请求页数
        parameter["page"] = 1
        # 获取疾病链接
        get_disease_link()
