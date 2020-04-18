import os
from Neo4j import data_search
from Answer import answer

class QuestionAnalysis:
    def __init__(self):
        self.path = '/'.join(os.path.dirname(__file__).split('\\'))
        self.data = ""
        self.entity = []
        self.attribute = []
        self.dict_entity = ["dis_sym", "ali_sym", "disease", "alias", "symptom", "drug", "check",
                            'population', 'department']
        self.dict_attribute = ['attr_disease', 'attr_department', 'attr_check', 'attr_method', 'attr_infect',
                               'attr_proportion', 'attr_population', 'attr_fee', 'attr_cure_period', 'attr_cure_rate',
                               'attr_cause', 'attr_prevent', 'attr_symptom', 'attr_drug', 'attr_form', 'attr_function',
                               'attr_usage', 'attr_component', 'attr_effects', 'attr_avoid', 'attr_matters']
        self.data_search = data_search.DataSearch()
        self.answer = answer.Answer()

    #
    def take_main_part(self, cut_words):
        self.entity = []
        self.attribute = []
        self.data = ""
        for word, pos in cut_words:
            if pos in self.dict_entity:
                self.entity.append((word, pos))
            elif pos in self.dict_attribute:
                self.attribute.append((word, pos))
        # print(self.entity, self.attribute)

    # 特殊问句
    def question_ts(self, sentence, cut_words):
        self.take_main_part(cut_words)
        entity = []
        entity_pos = []
        for word, pos in self.entity:
            if pos in ["dis_sym", "ali_sym", "disease", "alias", "symptom"] and pos not in entity_pos:
                entity.append((word, pos))
        if len(entity) == 1:
            self.answer.generate('ts', entity[0], None)
        # 组合答案
        if self.answer.answer is None or self.answer.answer == '':
            self.write_log(sentence)
        return self.answer.answer

    # 特指问句
    def question_tz(self, sentence, cut_words):
        self.take_main_part(cut_words)
        # 1实体
        if len(self.entity) == 1:
            # 疾病症状类
            if self.entity[0][1] in ["dis_sym", "ali_sym", "disease", "alias", "symptom"]:
                # 疾病症状类可有的属性
                dis_attr = ['attr_disease', 'attr_department', 'attr_check', 'attr_method', 'attr_infect',
                            'attr_proportion', 'attr_population', 'attr_fee', 'attr_cure_period', 'attr_cure_rate',
                            'attr_cause', 'attr_prevent', 'attr_symptom', 'attr_drug']
                # 0属性
                if len(self.attribute) == 0:
                    entity = self.entity[0]
                    attr_type = "brief"
                    self.answer.generate('tz', entity, attr_type)
                    data = self.data_search.search(entity, attr_type)
                    attr_type = "check"
                    self.answer.generate('tz', entity, attr_type)
                    data2 = self.data_search.search(entity, attr_type)
                    print(data, data2, sep='\n')
                # 1属性
                elif len(self.attribute) == 1 and self.attribute[0][1] in dis_attr:
                    entity = self.entity[0]
                    attr_type = self.attribute[0][1][5:]
                    # print(data_type)
                    data = self.data_search.search(entity, attr_type)
                    print(data)
                # 多个属性 找特指疑问词后最近的属性
                elif len(self.attribute) > 1:
                    key_tz_loc = len(cut_words)
                    attr_left = ""
                    attr_right = ""
                    # 特指疑问词的位置和其后的属性
                    for i in range(len(cut_words)):
                        if cut_words[i][1] == 'key_tz':
                            key_tz_loc = i
                        # 如果再严格一点可以只考虑特指疑问词后紧邻的那个是不是属性
                        elif i > key_tz_loc and cut_words[i][1] in dis_attr:
                            attr_right = cut_words[i][1]
                        elif i < key_tz_loc and cut_words[i][1] in dis_attr:
                            attr_left = cut_words[i][1]
                    # 特指疑问词后最近的属性
                    if attr_right != "":
                        entity = self.entity[0]
                        attr_type = attr_right[5:]
                        # print(data_type)
                        data = self.data_search.search(entity, attr_type)
                        print(data)
                        # 组合答案
                        self.data = ""
                        return self.data
                    elif attr_left != "":
                        entity = self.entity[0]
                        attr_type = attr_left[5:]
                        # print(data_type)
                        data = self.data_search.search(entity, attr_type)
                        print(data)
                        # 组合答案
                        self.data = ""
                        return self.data

                self.write_log(sentence)
                self.data = ""
                return self.data
            # 药物类
            elif self.entity[0][1] in ["drug"]:
                # 药物类可有的属性
                drug_attr = ['attr_disease', 'attr_form', 'attr_function', 'attr_usage', 'attr_component',
                             'attr_effects', 'attr_avoid', 'attr_matters']
                # 0属性
                if len(self.attribute) == 0:
                    entity = self.entity[0][1]
                    attr_type = ""
                    # print(data_type)
                    data = self.data_search.search(entity, attr_type)
                    print(data)
                    # 组合答案
                    self.data = ""
                    return self.data
                # 1属性
                elif len(self.attribute) == 1 and self.attribute[0][1] in drug_attr:
                    entity = self.entity[0]
                    attr_type = self.attribute[0][1][5:]
                    # print(data_type)
                    data = self.data_search.search(entity, attr_type)
                    print(data)
                    # 组合答案
                    self.data = ""
                    return self.data
                # 多属性 找特指疑问词后最近的属性
                elif len(self.attribute) > 1:
                    key_tz_loc = len(cut_words)
                    attr = []
                    # 特指疑问词的位置和其后的属性
                    for i in range(len(cut_words)):
                        if cut_words[i][1] == 'key_tz':
                            key_tz_loc = i
                        # 如果再严格一点可以只考虑特指疑问词后紧邻的那个是不是属性
                        elif i > key_tz_loc and cut_words[i][1] in drug_attr:
                            attr.append(cut_words[i][1])
                    # 特指疑问词后最近的属性
                    if len(attr) > 0:
                        entity = self.entity[0]
                        attr_type = attr[0][5:]
                        # print(data_type)
                        data = self.data_search.search(entity, attr_type)
                        print(data)
                        # 组合答案
                        self.data = ""
                        return self.data
                self.write_log(sentence)
                self.data = ""
                return self.data
            # 检查项目/人群类
            elif self.entity[0][1] in ["check", 'population']:
                # 检查/人群可有属性
                ch_attr = ['attr_disease']
                # 0属性
                if len(self.attribute) == 0:
                    entity = self.entity[0]
                    attr_type = 'disease'
                    # print(data_type)
                    data = self.data_search.search(entity, attr_type)
                    print(data)
                    # 组合答案
                    self.data = ""
                    return self.data
                # 1属性
                elif len(self.attribute) == 1 and self.attribute[0][1] in ch_attr:
                    entity = self.entity[0]
                    attr_type = self.attribute[0][1][5:]
                    # print(data_type)
                    data = self.data_search.search(entity, attr_type)
                    print(data)
                    # 组合答案
                    self.data = ""
                    return self.data
                # 多属性 找特指疑问词后最近的属性
                elif len(self.attribute) > 1:
                    key_tz_loc = len(cut_words)
                    attr = []
                    # 特指疑问词的位置和其后的属性
                    for i in range(len(cut_words)):
                        if cut_words[i][1] == 'key_tz':
                            key_tz_loc = i
                        # 如果再严格一点可以只考虑特指疑问词后紧邻的那个是不是属性
                        elif i > key_tz_loc and cut_words[i][1] in ch_attr:
                            attr.append(cut_words[i][1])
                    # 特指疑问词后最近的属性
                    if len(attr) > 0:
                        entity = self.entity[0]
                        attr_type = attr[0][5:]
                        # print(data_type)
                        data = self.data_search.search(entity, attr_type)
                        print(data)
                        # 组合答案
                        self.data = ""
                        return self.data
                self.write_log(sentence)
                self.data = ""
                return self.data
            self.write_log(sentence)
            self.data = ""
            return self.data
        # 2实体
        elif len(self.entity) == 2:
            self.write_log(sentence)
            return self.data

        self.write_log(sentence)
        return self.data

    # 选择问句
    def question_xz(self, sentence, cut_words):
        self.take_main_part(cut_words)
        # 确定哪个pos是被选择的 被选中的pos个数大于1
        entity = {}
        entity_pos = []
        for word, pos in self.entity:
            if entity.get(pos) is None:
                entity[pos] = 1
                entity_pos.append((word, pos))
            else:
                entity[pos] += 1
        # 一个主实体 多个被选择实体
        if len(entity_pos) == 2:
            if entity[entity_pos[0][1]] == 1 and entity[entity_pos[1][1]] == len(self.entity) - 1:
                entity = entity_pos[0]
                attr_type = entity_pos[1][1]
                data = self.data_search.search(entity, attr_type)
                print(data)
                # 组合答案
                self.data = ""
                return self.data
            elif entity[entity_pos[1][1]] == 1 and entity[entity_pos[0][1]] == len(self.entity) - 1:
                entity = entity_pos[1]
                attr_type = entity_pos[0][1]
                data = self.data_search.search(entity, attr_type)
                print(data)
                # 组合答案
                self.data = ""
                return self.data
        self.write_log(sentence)
        return self.data

    # 正反问句
    def question_zf(self, sentence, cut_words):
        self.take_main_part(cut_words)
        # 一实体——一属性
        if len(self.entity) == 1 and len(self.attribute) == 1:
            # 疾病症状类
            if self.entity[0][1] in ["dis_sym", "ali_sym", "disease", "alias", "symptom"] and \
                    self.attribute[0][1] in ['attr_disease', 'attr_department', 'attr_check', 'attr_method',
                                             'attr_infect', 'attr_proportion', 'attr_population', 'attr_fee',
                                             'attr_cure_period', 'attr_cure_rate', 'attr_cause', 'attr_prevent',
                                             'attr_symptom', 'attr_drug']:
                entity = self.entity[0]
                attr_type = self.attribute[0][1][5:]
                # print(data_type)
                data = self.data_search.search(entity, attr_type)
                print(data)
                # 组合答案
                self.data = ""
                return self.data
        # 实体-实体
        elif len(self.entity) == 2 and len(self.attribute) == 0:
            if self.entity[0][1] in ["dis_sym", "ali_sym", "disease", "alias", "symptom"] and \
                    self.entity[1][1] in self.entity:
                entity = self.entity[0]
                attr_type = self.entity[1][1]
                # print(data_type)
                data = self.data_search.search(entity, attr_type)
                print(data)
                # 组合答案
                self.data = ""
                return self.data
        self.write_log(sentence)
        return self.data

    # 是非问句
    def question_sf(self, sentence, cut_words):
        self.take_main_part(cut_words)
        # 实体-属性
        if len(self.entity) == 1 and len(self.attribute) == 1:
            if self.entity[0][1] in ["dis_sym", "ali_sym", "disease", "alias", "symptom"] and \
                    self.attribute[0][1] in ['attr_disease', 'attr_department', 'attr_check', 'attr_method',
                                             'attr_infect', 'attr_proportion', 'attr_population', 'attr_fee',
                                             'attr_cure_period', 'attr_cure_rate', 'attr_cause', 'attr_prevent',
                                             'attr_symptom', 'attr_drug']:
                entity = self.entity[0]
                attr_type = self.attribute[0][1][5:]
                # print(data_type)
                data = self.data_search.search(entity, attr_type)
                print(data)
                # 组合答案
                self.data = ""
                return self.data
        # 实体-实体
        elif len(self.entity) == 2 and len(self.attribute) == 0:
            if self.entity[0][1] in ["dis_sym", "ali_sym", "disease", "alias", "symptom"] and \
                    self.entity[1][1] in self.entity:
                entity = self.entity[0]
                attr_type = self.entity[1][1]
                # print(data_type)
                data = self.data_search.search(entity, attr_type)
                print(data)
                # 组合答案
                self.data = ""
                return self.data
        self.write_log(sentence)
        return self.data

    def write_log(self, sentence):
        with open(f'{self.path}/log.txt', 'a+', encoding='utf-8') as f:
            f.write(sentence + '\n')
