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
def get_diseases_id():
    """
    从寻医问药按首字母查询疾病页面获取爬取所有疾病链接
    :return: 一个包含所有疾病链接的集合
    """
    # 疾病请求地址
    url = "http://jib.api.xywy.com/GetJibInfo/getJibInfoByLetter"
    # 疾病请求参数 dict类型
    parameter = {
        "callback": "jsoncallback",
        "letter": "",
        "page": "1",
        "pageSize": "50"
    }
    #
    letters = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z']

    # 所有疾病的链接
    diseases_id = set()
    # 按首字母A-Z爬取疾病链接
    for letter in letters:
        # 修改请求字母
        parameter["letter"] = letter
        # 重置请求页数
        parameter["page"] = 1
        #
        while True:
            # 请求参数dict格式转url格式
            url_parameter = urlencode(parameter)
            # 获取链接返回的内容
            data = requests.get(url + "?" + url_parameter).text
            # 查找疾病的id
            data = re.findall(r'il_sii_(.+?).html', data)
            # 获取疾病id个数不为0
            if len(data) != 0:
                # 添加疾病id到集合中
                diseases_id.update(data)
                # 请求页数 + 1 继续循环进行下页请求
                parameter["page"] = int(parameter["page"]) + 1
            # 获取疾病id个数为0
            else:
                break
    # 返回疾病id集合
    return diseases_id


# 分析疾病页面
def analyze_disease_info(disease_id):
    response = requests.get(f'http://3g.jib.xywy.com/il_sii_{disease_id}.html')
    # 设置编码方式
    response.encoding = 'utf-8'
    # 创建Beautiful Soup对象
    soup = BeautifulSoup(response.text, 'html.parser')
    print('*'*50)
    # 返回参数 疾病信息，常用药物链接，相关疾病症状链接，相关疾病链接
    disease_info = {}
    drugs_id = set()
    symptoms_id = set()
    diseases_id = set()
    # **************************************************疾病概述**************************************************
    # 疾病名称, 疾病类型, 疾病别名, 疾病简介
    disease_gs = soup.select('.Disease-box')[0]
    # 疾病名称
    disease_title = disease_gs.select('em')
    if len(disease_title) == 1:
        disease_info["疾病名称"] = disease_title[0].text
    # 疾病类型
    disease_type = disease_gs.select('span')
    if len(disease_type) == 1:
        disease_info["疾病类型"] = disease_type[0].text
    # 疾病别名
    disease_alias = disease_gs.select('.Disease-alias')
    if len(disease_alias) == 1:
        disease_alias = re.sub(r'别名：', '', disease_alias[0].text)
        disease_alias = re.split('，', disease_alias)
        disease_info["别名"] = disease_alias
    # 疾病简介
    disease_brief = disease_gs.select('.Disease-brief')[0].select('p')
    if len(disease_brief) != 0:
        brief = []
        for p in disease_brief:
            brief.append(p.text.lstrip('\r\n'))
        disease_brief = '\n'.join(brief)
        disease_info["疾病简介"] = disease_brief
    # **************************************************到院就诊须知**************************************************
    # 挂什么科, 需做检查, 治疗方法, 常用药物, 一般费用, 传染性, 治愈周期, 治愈率, 患病比例, 好发人群, 相关症状, 相关疾病
    disease_xz = soup.find_all(attrs={'class': 'clearfix'})[1:13]
    # 挂什么科
    department = disease_xz[0].select('.fl')[1]
    department = re.split('\u2003', department.text)
    disease_info["挂什么科"] = department
    # 需做检查
    check = disease_xz[1].select('.fl')[1]
    check = re.split('  \xa0', check.text)
    disease_info["需做检查"] = check
    # 治疗方法
    method = disease_xz[2].select('.fl')[1]
    method = re.split('  \xa0', method.text)
    disease_info["治疗方法"] = method
    # 常用药物
    drug = disease_xz[3].select('.fl')[1]
    for drug_id in drug.select('a'):
        drugs_id.update(re.findall(r'goods/(.+?).htm', drug_id['href']))
    drug = re.split('\n ', drug.text.strip('\n\r\t '))
    disease_info["常用药物"] = drug
    # 一般费用
    cost = disease_xz[4].select('.fl')[1]
    disease_info["一般费用"] = cost.text
    # 传染性
    infect = disease_xz[5].select('.fl')[1]
    infect = re.split('  ', infect.text)
    disease_info["传染性"] = infect
    # 治愈周期
    cure_period = disease_xz[6].select('.fl')[1]
    disease_info["治愈周期"] = cure_period.text.strip('\n\r\t ')
    # 治愈率
    cure_rate = disease_xz[7].select('.fl')[1]
    cure_rate = re.findall(r"\d+\.?\d*%", cure_rate.text)
    disease_info["治愈率"] = cure_rate
    # 患病比例
    proportion = disease_xz[8].select('.fl')[1]
    proportion = re.findall(r"\d+\.?\d*%", proportion.text)
    disease_info["患病比例"] = proportion
    # 好发人群
    population = disease_xz[9].select('.fl')[1]
    population = re.split(' ', population.text)
    disease_info["好发人群"] = population
    # 相关症状
    symptoms = disease_xz[10].select('.fl')[1]
    for symptom_id in symptoms.select('a'):
        symptoms_id.update(re.findall(r'zzk_(.+?).html', symptom_id['href']))
    symptoms = re.split('\n', symptoms.text.strip('\n\r\t '))
    disease_info["相关症状"] = symptoms
    # 相关疾病
    relate_diseases = disease_xz[11].select('.fl')[1]
    for disease_id in relate_diseases.select('a'):
        diseases_id.update(re.findall(r'il_sii_(.+?).html', disease_id['href']))
    relate_diseases = re.split('\n', relate_diseases.text.strip('\n\r\t '))
    disease_info["相关疾病"] = relate_diseases

    # **************************************************解析**************************************************
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
    return [disease_info, drugs_id, symptoms_id, diseases_id]


# 获取药物链接
def get_drugs_id():
    # 药物分类链接
    category_url = 'http://3g.yao.xywy.com/ill_category.html'
    # 药物分类id
    categories_id = []
    # 所有药物链接
    drugs_id = set()
    response = requests.get(category_url)
    # 设置编码方式
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    # 提取药物所有分类
    ill_categories = soup.select('.clearfix')[0].select('li')
    # 提取药物分类id
    for ill_category in ill_categories:
        ill_category = ill_category.select('a')[0]['href']
        categories_id.append(re.findall(r'cate-(.+?).html', ill_category)[0])
    # 药物请求链接
    url = 'http://3g.yao.xywy.com/index.php'
    # 药物请求参数 dict类型
    parameter = {
        "s":"IllCategory/ajax_get_cate_info",
        "callback": "list",
        "cate_id": "",
        "page": "1"
    }
    for cate_id in categories_id:
        parameter["cate_id"] = cate_id
        parameter["page"] = 1
        # 防止死循环
        n = 1000000
        while n:
            n -= 1
            # 请求参数dict格式转url格式
            print(cate_id, parameter['page'])
            url_parameter = urlencode(parameter)
            # 获取链接返回的内容
            data = requests.get(url + "?" + url_parameter).text
            data = re.findall(r'"id":"(.+?)",', data)
            # 获取药物id个数不为0
            if len(data) != 0:
                drugs_id.update(data)
                parameter["page"] = int(parameter["page"]) + 1
            # 获取疾病网址个数为0
            else:
                break
    return drugs_id


# 分析药物页面
def analyze_drug_info(drug_url):
    """
    分析药物页面信息
    :param drug_url:药物页面链接
    :return: 字典型药物信息
    """
    response = requests.get(drug_url)
    # 设置编码方式
    response.encoding = 'utf-8'
    # 创建Beautiful Soup对象
    soup = BeautifulSoup(response.text, 'html.parser')
    # 药物页面有效
    if len(soup.select('.search-box')) == 0:
        data = soup.select('.drugs-info-box')[0].select('li')
        h5 = ['通用名称', '功能主治', '用法用量', '剂型', '成份', '不良反应', '禁忌', '注意事项']
        drug_info = {}
        for i in range(8):
            if h5[i] == data[i].select('h5')[0].text:
                drug_info[h5[i]] = data[i].select('p')[0].text
            else:
                print('Waring drug_analyze, url:', drug_url, 'h5')
        # 返回字典型药物信息
        return drug_info
    # 药物页面无效
    else:
        return False


# 获取症状链接
def get_symptoms_id():
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z']
    # 所有疾病的id
    symptoms_id = set()
    # 按首字母a-z爬取疾病id
    for letter in letters:
        # 疾病请求地址
        url = f"http://zzk.xywy.com/p/{letter}.html"
        # 获取链接返回的内容
        response = requests.get(url)
        # 设置编码方式
        response.encoding = 'gb2312'
        # 创建Beautiful Soup对象
        soup = BeautifulSoup(response.text, 'html.parser')
        for data in soup.select('.ks-ill-txt'):
            for da in data.select('a'):
                symptoms_id.add(re.findall(r'/(.+?)_', da['href'])[0])
    return symptoms_id


#
def analyze_symptom_info(symptom_id):
    response = requests.get(f'http://3g.jib.xywy.com/zzk_{symptom_id}.html')
    # 设置编码方式
    response.encoding = 'utf-8'
    # 创建Beautiful Soup对象
    soup = BeautifulSoup(response.text, 'html.parser')
    # 概述, 病因, 检查, 诊断, 预防, 可能患有的疾病, 常见症状
    symptom_info = {}
    diseases_id = set()
    symptoms_id = set()
    print('*' * 100)
    data = soup.select('.sec-box ')[:7]
    # 症状
    symptom_info["症状"] = data[0].select('em')[0].text.strip(' ')
    # 概述, 病因, 检查, 诊断, 预防
    h2 = ['概述', '病因', '检查', '诊断', '预防']
    for i in range(5):
        ps = data[i].select('p')
        if len(ps) != 0:
            dic = []
            for p in ps:
                dic.append(p.text.strip('\r\n '))
            p = '\n'.join(dic)
            symptom_info[h2[i]] = p
    # 可能患有的疾病
    diseases = []
    for a in data[5].select('a'):
        diseases.append(a.select('p')[0].text.strip(' '))
        diseases_id.add(re.findall(r'il_sii_(.+?).html', a['href'])[0])
    symptom_info["可能患有的疾病"] = diseases
    # 常见症状
    r_symptoms = []
    for a in data[6].select('a'):
        r_symptoms.append(a.text.strip(' '))
        symptoms_id.add(re.findall(r'zzk_(.+?).html', a['href'])[0])
    symptom_info["常见症状"] = r_symptoms
    # # 病因
    # symptom_cause = data[1].select('p')
    # if len(symptom_cause) != 0:
    #     cause = []
    #     for p in symptom_cause:
    #         cause.append(p.text.strip('\r\n '))
    #     symptom_cause = '\n'.join(cause)
    #     symptom_info["病因"] = symptom_cause
    # # 检查
    # symptom_inspect = data[2].select('p')
    # if len(symptom_inspect) != 0:
    #     inspect = []
    #     for p in symptom_inspect:
    #         inspect.append(p.text.strip('\r\n '))
    #     symptom_inspect = '\n'.join(inspect)
    #     symptom_info["检查"] = symptom_inspect
    # # 诊断
    # symptom_diagnose = data[3].select('p')
    # if len(symptom_diagnose) != 0:
    #     diagnose = []
    #     for p in symptom_diagnose:
    #         diagnose.append(p.text.strip('\r\n '))
    #     symptom_diagnose = '\n'.join(diagnose)
    #     symptom_info["诊断"] = symptom_diagnose
    # # 预防
    # symptom_prevent = data[4].select('p')
    # if len(symptom_prevent) != 0:
    #     prevent = []
    #     for p in symptom_prevent:
    #         prevent.append(p.text.strip('\r\n '))
    #     symptom_prevent = '\n'.join(prevent)
    #     symptom_info["预防"] = symptom_prevent
    return [symptom_info, diseases_id, symptoms_id]
# # 所有疾病链接
# diseases_urls = set()
# # 所有药物链接
# drugs_urls = set()
# # 所有症状链接
# symptoms_urls = set()


if __name__ == '__main__':
    # 获取疾病id
    # diseases_id = get_diseases_id()
    # print(len(diseases_id), diseases_id)
    # print(max(diseases_id))
    # 获取药品id
    # drugs_id = get_drugs_id()
    # print(len(drugs_id), type(drugs_id), drugs_id)
    # 获取症状id
    # symptoms_id = get_symptoms_id()
    # print(len(symptoms_id), type(symptoms_id), symptoms_id)
    # **************************************************疾病**************************************************
    # 疾病页面解析
    # diseases_id = [3135, 9748, 4891, 4764]
    # for id in diseases_id:
    #     info = analyze_disease_info(id)
    #     # 疾病信息
    #     for key, value in info[0].items():
    #         print(f'{key}：{value}')
    #     # 药物链接
    #     for drug_url in info[1]:
    #         print(drug_url)
    #     # 症状链接
    #     for symptom_url in info[2]:
    #         print(symptom_url)
    #     # 疾病链接
    #     for disease_url in info[3]:
    #         print(disease_url)
    # **************************************************药物**************************************************
    # 分析药物页面信息
    # drugs_url = ['http://3g.yao.xywy.com/goods/130194.htm',
    #              'http://3g.yao.xywy.com/goods/996.htm',
    #              'http://3g.yao.xywy.com/goods/59426.htm']
    # for url in drugs_url:
    #     print(analyze_drug_info(url))
    # **************************************************症状**************************************************
    # 分析症状页面信息
    # symptoms_id = [6819, 4515, 5605, 4057]
    # for id in symptoms_id:
    #     symptom_info = analyze_symptom_info(id)
    #     print(symptom_info)
    #     # 症状信息
    #     for key, value in symptom_info[0].items():
    #         print(f'{key}：\n{value}')
    #     # 可能患病疾病链接
    #     for disease_id in symptom_info[1]:
    #         print(disease_id)
    #     # 常见症状链接
    #     for symptom_id in symptom_info[2]:
    #         print(symptom_id)


















