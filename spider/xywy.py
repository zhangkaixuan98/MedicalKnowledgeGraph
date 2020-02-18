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
from bs4 import BeautifulSoup
from lxml import etree


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
    # for i in range(65, 91):
    #     print(chr(i))
    #     # 修改请求字母
    #     parameter["letter"] = chr(i)
    #     # 重置请求页数
    #     parameter["page"] = 1
    #     # 获取疾病链接
    #     get_disease_link()
    disease_url = 'http://3g.jib.xywy.com/il_sii_9748.html'
    response = requests.get(disease_url)
    # print(response.text)
    # 设置编码方式
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    # 疾病概述
    disease_gs = soup.select('.Disease-box')[0]
    # print(disease_gs)
    # for i in range(0, 1):
    #     # 疾病名称
    #     disease_title = disease_gs.select('em')
    #     for title in disease_title:
    #         print(title.text)
    #     # 疾病别名
    #     disease_alias = disease_gs.select('.Disease-alias')
    #     for alias in disease_alias:
    #         print(alias.text)
    #     # 疾病类型
    #     disease_type = disease_gs.select('span')
    #     for types in disease_type:
    #         print(types.text)
    #     # 疾病简介
    #     disease_brief = disease_gs.select('.Disease-brief')[0].select('p')
    #     for brief in disease_brief:
    #         print(brief.text)
    # 到院就诊须知
    disease_xz = soup.find_all(attrs={'class': 'clearfix'})[1:13]
    for xz in disease_xz:
        print('***************\n', xz)
    print(len(disease_xz))
    for i in range(0, 1):
        # 挂什么科
        disease_department = disease_xz[0].select('.reach-right')[0]
        print('挂什么科:', disease_department.text)
        # 需做检查
        disease_check = disease_xz[1].select('.reach-right')[0]
        print('需做检查:', disease_check.text)
        # 治疗方法
        disease_method = disease_xz[2].select('.reach-right')[0]
        print('治疗方法:', disease_method.text)
        # 常用药物
        disease_drug = disease_xz[3].select('.reach-tabright')[0]
        print('常用药物:', disease_drug.text)
        # 一般费用
        disease_cost = disease_xz[4].select('.reach-right')[0]
        print('一般费用:', disease_cost.text)
        # 传染性
        disease_infect = disease_xz[5].select('.reach-right')[0]
        print('传染性:', disease_infect.text)
        # 治愈周期
        cure_period = disease_xz[6].select('.reach-right')[0]
        print('治愈周期:', cure_period.text)
        # 治愈率
        cure_rate = disease_xz[7].select('.reach-right')[0]
        print('治愈率:', cure_rate.text)
        # 患病比例
        disease_proportion = disease_xz[8].select('.reach-right')[0]
        print('患病比例:', disease_proportion.text)
        # 好发人群
        susceptible_population = disease_xz[9].select('.reach-right')[0]
        print('好发人群:', susceptible_population.text)
        # 相关症状
        relate_symptoms = disease_xz[10].select('.reach-tabright')[0]
        print('相关症状:', relate_symptoms.text)
        # 相关疾病
        relate_diseases = disease_xz[11].select('.reach-tabright')[0]
        print('相关疾病:', relate_diseases)
    # 解析
    # disease_analysis = soup.find_all(attrs={'class': 'Disease-analysis'})[0:8]
    # # for analysis in disease_analysis:
    #     # print('************************\n', analysis.text)
    # print(len(disease_analysis))
    # 症状解析
    # analysis_zz = disease_analysis[0].select('p')
    # print('****************症状解析****************')
    # for zz in analysis_zz:
    #     print(zz)
    # # 病因解析
    # analysis_by = disease_analysis[1].select('p')
    # print('****************病因解析****************')
    # for by in analysis_by:
    #     print(by)
    # # 诊断解析
    # analysis_zd = disease_analysis[2].select('p')
    # print('****************诊断解析****************')
    # for zd in analysis_zd:
    #     print(zd)
    # # 治疗解析
    # analysis_zl = disease_analysis[3].select('p')
    # print('****************治疗解析****************')
    # for zl in analysis_zl:
    #     print(zl)
    # # 饮食保健
    # analysis_ysbj = disease_analysis[4].select('p')
    # print('****************饮食保健****************')
    # for ysbj in analysis_ysbj:
    #     print(ysbj)

