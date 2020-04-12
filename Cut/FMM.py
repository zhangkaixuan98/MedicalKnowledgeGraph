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
# 字典中最大长度
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
    max_length = max(len(word) for word in dict_alias_symptom)


# 正向最大匹配
def cut_words(sentence):
    global max_length
    sentence = sentence.strip()
    # 统计序列长度
    words_length = len(sentence)
    # 存储切分好的词语
    cut_word_list = []
    while words_length > 0:
        max_cut_length = min(max_length, words_length)
        sub_sentence = sentence[0: max_cut_length]
        while max_cut_length > 0:
            # 实体
            if sub_sentence in dict_disease_symptom:
                cut_word_list.append(sub_sentence)
                break
            elif sub_sentence in dict_alias_symptom:
                cut_word_list.append(sub_sentence)
                break
            elif sub_sentence in dict_disease:
                cut_word_list.append(sub_sentence)
                break
            elif sub_sentence in dict_alias:
                cut_word_list.append(sub_sentence)
                break
            elif sub_sentence in dict_symptom:
                cut_word_list.append(sub_sentence)
                break
            elif sub_sentence in dict_drug:
                cut_word_list.append(sub_sentence)
                break
            elif sub_sentence in dict_check:
                cut_word_list.append(sub_sentence)
                break
            # 属性
            elif sub_sentence in sx:
                cut_word_list.append(sub_sentence)
                break
            elif max_cut_length == 1:
                cut_word_list.append(sub_sentence)
                break
            else:
                max_cut_length -= 1
                sub_sentence = sub_sentence[0: max_cut_length]
        sentence = sentence[max_cut_length:]
        words_length = words_length - max_cut_length
    words = "/".join(cut_word_list)
    return words


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
