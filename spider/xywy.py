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
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher


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
            print(f'get_diseases_id:{letter},{parameter["page"]}')
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
    # 返回参数 疾病信息，常用药物链接，相关疾病症状链接，相关疾病链接
    disease_info = {}
    drugs_id = set()
    symptoms_id = set()
    diseases_id = set()
    try:
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
            disease_alias = re.split('，', disease_alias.strip('，'))
            disease_info["疾病别名"] = disease_alias
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
            department = re.split('\u2003', department.text.strip('\u2003'))
            disease_info["挂什么科"] = department
            # 需做检查
            check = disease_xz[1].select('.fl')[1]
            check = re.split('  \xa0', check.text.strip('  \xa0'))
            disease_info["需做检查"] = check
            # 治疗方法
            method = disease_xz[2].select('.fl')[1]
            method = re.split('  \xa0', method.text.strip('  \xa0'))
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
            infect = re.split('  ', infect.text.strip('  '))
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
            population = re.split(' ', population.text.strip(' '))
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
    except Exception as e:
        print(f'analyze_disease_info:http://3g.jib.xywy.com/il_sii_{disease_id}.html\n{e}')


# 存储疾病信息
def write_disease_info(disease_info):
    graph = Graph("bolt://localhost:7687", username="neo4j", password='1998')
    node_matcher = NodeMatcher(graph)
    r_matcher = RelationshipMatcher(graph)
    try:
        # 疾病名称
        if disease_info.get('疾病名称') is not None:
            disease = node_matcher.match("disease").where(f"_.name = '{disease_info['疾病名称']}'").first()
            # 此疾病节点还未创建
            if disease is None:
                disease = Node('disease', name=disease_info['疾病名称'])
                graph.create(disease)
        # 疾病类型
        if disease_info.get('疾病类型') is not None:
            kind = node_matcher.match("kind").where(f"_.name = '{disease_info['疾病类型']}'").first()
            # 此类型节点还未创建
            if kind is None:
                kind = Node('kind', name=disease_info['疾病类型'])

            kind_disease = Relationship(kind, 'kind_disease', disease)
            graph.create(kind_disease)
        # 疾病别名
        if disease_info.get('疾病别名') is not None:
            for bieming in disease_info['疾病别名']:
                alias = node_matcher.match("alias").where(f"_.name = '{bieming}'").first()
                # 此别名节点还未创建
                if alias is None:
                    alias = Node('alias', name=bieming)
                    graph.create(alias)
                disease_alias = r_matcher.match({disease, alias}, 'disease_alias').first()
                if disease_alias is None:
                    disease_alias = Relationship(disease, 'disease_alias', alias)
                    graph.create(disease_alias)
        # 疾病简介
        if disease_info.get('疾病简介') is not None:
            disease['brief'] = disease_info['疾病简介']
            graph.push(disease)
        # 挂什么科
        if disease_info.get('挂什么科') is not None:
            departments = []
            for keshi in disease_info['挂什么科']:
                department = node_matcher.match("department").where(f"_.name = '{keshi}'").first()
                if department is None:
                    department = Node('department', name=keshi)
                    graph.create(department)
                department_disease = r_matcher.match({disease, department}, 'dept_contain_disease').first()
                if department_disease is None:
                    department_disease = Relationship(department, 'dept_contain_disease', disease)
                    graph.create(department_disease)
                departments.append(department)
            for i in range(len(departments) - 1):
                keshi = disease_info['挂什么科'][i]
                department_department = r_matcher.match([departments[i], departments[i+1]], 'dept_contain_dept').first()
                if department_department is None:
                    department_department = Relationship(departments[i], 'dept_contain_dept', departments[i + 1])
                    graph.create(department_department)
        # 需做检查
        if disease_info.get('需做检查') is not None:
            for jiancha in disease_info['需做检查']:
                try:
                    check = node_matcher.match("check").where(f"_.name = '{jiancha}'").first()
                    if check is None:
                        check = Node('check', name=jiancha)
                        graph.create(check)
                    disease_check = r_matcher.match({disease, check}, 'disease_check')
                    if disease_check is None:
                        disease_check = Relationship(disease, 'disease_check', check)
                        graph.create(disease_check)
                except Exception as e:
                    print(f'需做检查 {e}')
                    # pass
        # 治疗方法 disease_method
        if disease_info.get('治疗方法') is not None:
            for fangfa in disease_info['治疗方法']:
                method = node_matcher.match("method").where(f"_.name = '{fangfa}'").first()
                if method is None:
                    method = Node('method', name=fangfa)
                    graph.create(method)
                disease_method = r_matcher.match({disease, method}, 'disease_method').first()
                if disease_method is None:
                    disease_method = Relationship(disease, 'disease_method', method)
                    graph.create(disease_method)
        # 常用药物 disease_drug
        if disease_info.get('常用药物') is not None:
            for yaowu in disease_info['常用药物']:
                drug = node_matcher.match("drug").where(f"_.name = '{yaowu}'").first()
                if drug is None:
                    drug = Node('drug', name=yaowu)
                    graph.create(drug)
                disease_drug = r_matcher.match({disease, drug}, 'disease_drug').first()
                if disease_drug is None:
                    disease_drug = Relationship(disease, 'disease_drug', drug)
                    graph.create(disease_drug)
        # 一般费用
        if disease_info.get('一般费用') is not None:
            disease['fee'] = disease_info['一般费用']
            graph.push(disease)
        # 传染性 disease_infect
        if disease_info.get('传染性') is not None:
            for chuanran in disease_info['传染性']:
                infect = node_matcher.match("infect").where(f"_.name = '{chuanran}'").first()
                if infect is None:
                    infect = Node('infect', name=chuanran)
                    graph.create(infect)
                disease_infect = r_matcher.match({disease, infect}, 'disease_infect').first()
                if disease_infect is None:
                    disease_infect = Relationship(disease, 'disease_infect', infect)
                    graph.create(disease_infect)
        # 治愈周期
        if disease_info.get('治愈周期') is not None:
            disease['cure_period'] = disease_info['治愈周期']
            graph.push(disease)
        # 治愈率
        if disease_info.get('治愈率') is not None:
            for zhiyulv in disease_info['治愈率']:
                cure_rate = node_matcher.match("cure_rate").where(f"_.name = '{zhiyulv}'").first()
                if cure_rate is None:
                    cure_rate = Node('cure_rate', name=zhiyulv)
                disease_cure_rate = Relationship(disease, 'disease_rate', cure_rate)
                graph.create(disease_cure_rate)
        # 患病比例 disease_proportion
        if disease_info.get('患病比例') is not None:
            for bili in disease_info['治愈率']:
                proportion = node_matcher.match("proportion").where(f"_.name = '{bili}'").first()
                if proportion is None:
                    proportion = Node('proportion', name=bili)
                disease_proportion = Relationship(disease, 'disease_rate', proportion)
                graph.create(disease_proportion)
        # 好发人群 susceptible_population
        if disease_info.get('好发人群') is not None:
            for renqun in disease_info['好发人群']:
                population = node_matcher.match("population").where(f"_.name = '{renqun}'").first()
                if population is None:
                    population = Node('population', name=renqun)
                disease_population = Relationship(disease, 'disease_rate', population)
                graph.create(disease_population)
        # 相关症状 relate_symptoms
        if disease_info.get('相关症状') is not None:
            for zz in disease_info['相关症状']:
                symptom = node_matcher.match("symptom").where(f"_.name = '{zz}'").first()
                if symptom is None:
                    symptom = Node('symptom', name=zz)
                disease_symptom = Relationship(disease, 'disease_rate', symptom)
                graph.create(disease_symptom)
        # 相关疾病
        if disease_info.get('相关疾病') is not None:
            for jib in disease_info['相关疾病']:
                r_disease = node_matcher.match("disease").where(f"_.name = '{jib}'").first()
                if r_disease is None:
                    r_disease = Node('disease', name=jib)
                disease_r_disease = Relationship(disease, 'disease_relate', r_disease)
                graph.create(disease_r_disease)
        return True
    except Exception as e:
        print(f"write_disease_info:{disease_info['疾病名称']}\n{e}\nurl=", end='')
        return False


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
    i = 0
    for cate_id in categories_id:
        i += 1
        parameter["cate_id"] = cate_id
        parameter["page"] = 1
        # 防止死循环
        n = 1
        while n:
            n -= 1
            # 请求参数dict格式转url格式
            print(f'get_drugs_id:{i} {parameter["page"]}')
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
def analyze_drug_info(drug_id):
    """
    分析药物页面信息
    :param drug_id:药物页面链接
    :return: 字典型药物信息
    """
    response = requests.get(f'http://3g.yao.xywy.com/goods/{drug_id}.htm')
    # 设置编码方式
    response.encoding = 'utf-8'
    # 创建Beautiful Soup对象
    soup = BeautifulSoup(response.text, 'html.parser')
    # 药物页面有效
    try:
        if len(soup.select('.search-box')) == 0:
                data = soup.select('.drugs-info-box')[0].select('li')
                h5 = ['通用名称', '功能主治', '用法用量', '剂型', '成份', '不良反应', '禁忌', '注意事项']
                drug_info = {}
                for info in data:
                    if info.select('h5')[0].text in h5:
                        drug_info[info.select('h5')[0].text] = info.select('p')[0].text
                # 返回字典型药物信息
                return drug_info
        # 药物页面无效
        else:
            return None
    except Exception as e:
        print(f'analyze_drug_info:http://3g.yao.xywy.com/goods/{drug_id}.htm\n{e}')
        return None


#
def write_drug_info(drug_info):
    graph = Graph("bolt://localhost:7687", username="neo4j", password='1998')
    node_matcher = NodeMatcher(graph)
    try:
        # 通用名称
        if drug_info.get('通用名称') is not None:
            drug = node_matcher.match("drug").where(f"_.name = '{drug_info['通用名称']}'").first()
            # 此节点还未创建
            if drug is None:
                drug = Node('drug', name=drug_info['通用名称'])
                graph.create(drug)
        # 功能主治
        if drug_info.get('功能主治') is not None:
            drug['function'] = drug_info['功能主治']
            graph.push(drug)
        # 用法用量
        if drug_info.get('用法用量') is not None:
            drug['usage'] = drug_info['用法用量']
            graph.push(drug)
        # 剂型
        if drug_info.get('剂型') is not None:
            form = node_matcher.match('form').where(f"_.name = '{drug_info['剂型']}'").first()
            if form is None:
                form = Node('form', name=drug_info['剂型'])
            form_drug = Relationship(form, 'form_drug', drug)
            graph.create(form_drug)
        # 成份
        if drug_info.get('成份') is not None:
            drug['component'] = drug_info['成份']
            graph.push(drug)
        # 不良反应
        if drug_info.get('不良反应') is not None:
            drug['effects'] = drug_info['不良反应']
            graph.push(drug)
        # 禁忌
        if drug_info.get('禁忌') is not None:
            drug['avoid'] = drug_info['禁忌']
            graph.push(drug)
        # 注意事项
        if drug_info.get('注意事项') is not None:
            drug['matters'] = drug_info['注意事项']
            graph.push(drug)
    except Exception as e:
        print(f'write_drug_info:{drug_info["通用名称"]}\n{e}\nurl=', end='')
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
        print(f'get_symptoms_id:{letter}')
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


# 分析症状页面
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
    try:
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
    except Exception as e:
        print(f'analyze_symptom_info:http://3g.jib.xywy.com/zzk_{symptom_id}.html\n{e}')
        return None

#
def write_symptom_info(symptom_info):
    graph = Graph("bolt://localhost:7687", username="neo4j", password='1998')
    node_matcher = NodeMatcher(graph)
    try:
        # 症状
        if symptom_info.get('症状') is not None:
            symptom = node_matcher.match("symptom").where(f"_.name = '{symptom_info['症状']}'").first()
            # 此节点还未创建
            if symptom is None:
                symptom = Node('symptom', name=symptom_info['症状'])
                graph.create(symptom)
        # 概述
        if symptom_info.get('概述') is not None:
            symptom['brief'] = symptom_info['概述']
            graph.push(symptom)
        # 病因
        if symptom_info.get('概述') is not None:
            symptom['brief'] = symptom_info['概述']
            graph.push(symptom)
        # 检查
        if symptom_info.get('检查') is not None:
            symptom['check'] = symptom_info['检查']
            graph.push(symptom)
        # 诊断
        if symptom_info.get('诊断') is not None:
            symptom['diagnose'] = symptom_info['诊断']
            graph.push(symptom)
        # 预防
        if symptom_info.get('预防') is not None:
            symptom['prevent'] = symptom_info['预防']
            graph.push(symptom)
        # 可能患有的疾病
        if symptom_info.get('可能患有的疾病') is not None:
            for jib in symptom_info['可能患有的疾病']:
                disease = node_matcher.match('disease').where(f"_.name = '{jib}'").first()
                if disease is None:
                    disease = Node('disease', name=jib)
                symptom_disease = Relationship(symptom, 'symptom_disease', disease)
                graph.create(symptom_disease)
        # 常见症状
        if symptom_info.get('常见症状') is not None:
            for zz in symptom_info['常见症状']:
                r_symptom = node_matcher.match('symptom').where(f"_.name = '{zz}'").first()
                if r_symptom is None:
                    r_symptom = Node('symptom', name=zz)
                symptom_r_symptom = Relationship(symptom, 'r_symptom', r_symptom)
                graph.create(symptom_r_symptom)
        return True
    except Exception as e:
        print(f"write_symptom_info:{symptom_info['症状']}\n{e}\nurl=", end='')
        return False
# # 所有疾病链接
# diseases_urls = set()
# # 所有药物链接
# drugs_urls = set()
# # 所有症状链接
# symptoms_urls = set()


if __name__ == '__main__':
    # drugs_id = [21726, 575396, 39022, 575318, 60898, 575231, 6907]
    # for id in drugs_id:
    #     info = analyze_drug_info(id)
    #     if info is not None:
    #         print(info)
            # if write_drug_info(info) is False:
            #     print(f'http://3g.yao.xywy.com/goods/{id}.htm')

    # info = analyze_disease_info(704)[0]
    # print(info)
    # write_disease_info(info)
    # 获取疾病id
    diseases_id = get_diseases_id()
    # print(max(diseases_id))
    # 获取药品id
    drugs_id = get_drugs_id()
    # 获取症状id
    symptoms_id = get_symptoms_id()

    #
    diseases_finish = set()
    drugs_finish = set()
    symptoms_finish = set()
    lens = [len(diseases_id), len(drugs_id), len(symptoms_id)]
    while len(diseases_id) or len(drugs_id) or len(symptoms_id):
        # **************************************************疾病**************************************************
        # 疾病页面解析
        # diseases_id = [3135, 9748, 4891, 4764]
        if len(diseases_id) != 0:
            id = diseases_id.pop()
            diseases_finish.add(id)
            info = analyze_disease_info(id)
            if info is not None:
                # 疾病信息
                # print(info[0])
                if write_disease_info(info[0]) is False:
                    print(f'http://3g.jib.xywy.com/il_sii_{id}.html')
                # 药物链接
                for drug_id in info[1]:
                    # print(drug_id)
                    if drug_id not in drugs_finish:
                        drugs_id.add(drug_id)
                # 症状链接
                for symptom_id in info[2]:
                    # print(symptom_id)
                    if symptom_id not in symptoms_finish:
                        symptoms_id.add(symptom_id)
                # 疾病链接
                for disease_id in info[3]:
                    # print(disease_id)
                    if disease_id not in diseases_finish:
                        diseases_id.add(disease_id)
        # **************************************************药物**************************************************
        # 分析药物页面信息
        # drugs_id = [130194, 996, 59426, 666, 999]
        if len(drugs_id) != 0:
            id = drugs_id.pop()
            drugs_finish.add(id)
            info = analyze_drug_info(id)
            if info is not None:
                if write_drug_info(info) is False:
                    print(f'http://3g.yao.xywy.com/goods/{id}.htm')
            # else:
            #     print(id)
        # **************************************************症状**************************************************
        # 分析症状页面信息
        # symptoms_id = [6819, 4515, 5605, 4057]
        if len(symptoms_id) != 0:
            id = symptoms_id.pop()
            symptoms_finish.add(id)
            symptom_info = analyze_symptom_info(id)
            if symptom_info is not None:
                # 症状信息
                if write_symptom_info(symptom_info[0]) is False:
                    print(f'http://3g.jib.xywy.com/zzk_{id}.html')
                # 可能患病疾病链接
                for disease_id in symptom_info[1]:
                    # print(disease_id)
                    if disease_id not in diseases_finish:
                        diseases_id.add(disease_id)
                # 常见症状链接
                for symptom_id in symptom_info[2]:
                    # print(symptom_id)
                    if symptom_id not in symptoms_finish:
                        symptoms_id.add(symptom_id)
    print('length of diseases:' + str(lens[0]) + len(diseases_finish))
    print('length of drugs:' + str(lens[1]) + len(drugs_finish))
    print('length of symptoms:' + str(lens[2]) + len(symptoms_finish))

















