import os
# 疾病，症状，药物字典
dict_disease_symptom = []
dict_alias_symptom = []
dict_disease = []
dict_alias = []
dict_symptom = []
dict_drug = []
dict_check = []
# 特指，特殊，选择，是非，正反问句字典
dict_tz = []
dict_ts = []
dict_xz = []
dict_sf = []
dict_zf = []
# 属性
sx = []
# 词典中最长的词的长度
max_length = 0
# 字典路径
dict_file_path = {'disease_symptom': os.path.dirname(__file__) + '/dict/dis_sym.txt',
                  'alias_symptom': os.path.dirname(__file__) + '/dict/ali_sym.txt',
                  'disease': os.path.dirname(__file__) + '/dict/disease.txt',
                  'alias': os.path.dirname(__file__) + '/dict/alias.txt',
                  'symptom': os.path.dirname(__file__) + '/dict/symptom.txt',
                  'drug': os.path.dirname(__file__) + '/dict/drug.txt',
                  'check': os.path.dirname(__file__) + '/dict/check.txt'}


def init():
    # 词典中最长的词的长度
    global max_length

    # 实体
    with open(dict_file_path['disease_symptom'], 'r', encoding='utf-8') as f:
        dict_disease_symptom.extend(f.read().strip().split('\n'))
    with open(dict_file_path['alias_symptom'], 'r', encoding='utf-8') as f:
        dict_alias_symptom.extend(f.read().strip().split('\n'))
    with open(dict_file_path['disease'], 'r', encoding='utf-8') as f:
        dict_disease.extend(f.read().strip().split('\n'))
    with open(dict_file_path['alias'], 'r', encoding='utf-8') as f:
        dict_alias.extend(f.read().strip().split('\n'))
    with open(dict_file_path['symptom'], 'r', encoding='utf-8') as f:
        dict_symptom.extend(f.read().strip().split('\n'))
    with open(dict_file_path['drug'], 'r', encoding='utf-8') as f:
        dict_drug.extend(f.read().strip().split('\n'))
    with open(dict_file_path['check'], 'r', encoding='utf-8') as f:
        dict_check.extend(f.read().strip().split('\n'))
    # 问句关键词
    dict_tz.extend(['谁', '什么', '哪', '哪儿', '哪里', '几', '多少', '多', '多么', '怎么', '怎样', '怎么样', '什么', '怎样', '什么样', '哪些', '啥'])
    dict_ts.extend(['为什么'])
    dict_xz.extend(['还是'])
    dict_sf.extend(['能', '可以', '会', '有', '是', '长'])
    dict_zf.extend(['能不能', '可不可以', '会不会', '有没有', '是不是', '长不长'])
    # 属性
    sx.extend(['并发症'])
    # 词典中最长的词的长度
    max_length = max(len(word) for word in dict_alias_symptom)


# 逆向最大匹配算法
def cut_words(sentence):
    """
    逆向最大匹配算法
    :param sentence: 需要切的句子
    :return: 切好的词列表
    """
    global max_length
    sub_sentence = sentence.strip()  # 去除句子两边的空格换行等
    sub_sentence_length = len(sub_sentence)
    cut_word_list = []  # 存储切分好的词
    # 句子循环
    while sub_sentence_length > 0:
        # 当前句子所能切出的最长的词 及句子和词典长度最小值
        sub_word_length = min(max_length, sub_sentence_length)
        sub_word = sentence[-sub_word_length:]
        # 词循环
        while sub_word_length > 0:
            if is_in_dict(cut_word_list, sub_word):
                break
            elif sub_word_length == 1:  # 剩一个字时
                cut_word_list.append(sub_word)
                break
            else:  # 去除最左边的字
                sub_word_length -= 1
                sub_word = sub_word[-sub_word_length:]
        # 切除右边分出的词
        sub_sentence_length = sub_sentence_length - sub_word_length
        sub_sentence = sub_sentence[:sub_sentence_length]
    cut_word_list.reverse()  # 反转一下切出的词的顺序
    cut_sentence = "/".join(cut_word_list)  # 返回切好的句子
    return cut_sentence


def is_in_dict(word_list, word):
    """
    词是非在词典中
    :param word_list: 词列表
    :param word:
    :return: word在词典中则返回true
    """
    # 实体
    if word in dict_disease_symptom:
        word_list.append(word)
        return True
    elif word in dict_alias_symptom:
        word_list.append(word)
        return True
    elif word in dict_disease:
        word_list.append(word)
        return True
    elif word in dict_alias:
        word_list.append(word)
        return True
    elif word in dict_symptom:
        word_list.append(word)
        return True
    elif word in dict_drug:
        word_list.append(word)
        return True
    elif word in dict_check:
        word_list.append(word)
        return True
    # 属性
    elif word in sx:
        word_list.append(word)
        return True
    else:
        return False

def main():
    """
    用户交互接口
    :return:
    """
    init()
    while True:
        print("请输入需要分词的序列")
        input_str = input()
        if not input_str:
            break
        result = cut_words(input_str)
        print(f"分词结果\n{result}")


if __name__ == "__main__":
    main()
