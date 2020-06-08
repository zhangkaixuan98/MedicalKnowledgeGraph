var disease_info = {
    "疾病":"",
    "类型":"",
    "别名":"",
    "简介":["",""],
    "挂什么科":"",
    "需做检查":"",
    "治疗方法":"",
    "常用药物":["",""],
    "一般费用":"",
    "传染性":"",
    "治愈周期":"",
    "治愈率":"",
    "患病比例":"",
    "好发人群":"",
    "相关症状":["",""],
    "相关疾病":["",""]
}
var symptom_info = {
    "症状": "",
    "概述": ["",""],
    "病因": ["",""],
    "检查": ["",""],
    "诊断": ["",""],
    "预防": ["",""],
    "可能患有的疾病": [
      {"疾病":"","相关症状":""},
      {"疾病":"","相关症状":""}
    ],
    "常见症状": []
};
var drug_info = {
    "通用名称": "",
    "功能主治": ["",""],
    "用法用量": ["",""],
    "剂型": "",
    "成份": ["",""],
    "不良反应": ["",""],
    "禁忌": ["",""],
    "注意事项": ["",""],
};
var result = {
    "相关疾病": [
      {"疾病":"","科室":"","简介":"","症状":""},
      {"疾病":"","科室":"","简介":"","症状":""}
    ]
    "相关症状":[
      {"症状": "","概述": ""},
      {"症状": "","概述": ""}
    ],
    "相关药物":[
      {"通用名称": "","功能主治": ""}，
      {"通用名称": "","功能主治": ""}
    ]
};
