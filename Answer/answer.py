# 组织答案
from Neo4j import data_search
from Answer import disease, alias, symptom, drug, check, population


class Answer:
    def __init__(self):
        self.entity = None
        self.attr = None
        self.xz_entity = None
        self.answer = ''
        self.feedback = '可反馈'
        self.data = ""
        self.data_search = data_search.DataSearch()
        self.disease = disease.Disease()
        self.alias = alias.Alias()
        self.symptom = symptom.Symptom()
        self.drug = drug.Drug()
        self.check = check.Check()
        self.population = population.Population()
        return

    def generate(self, question_type, entity, attr, xz_entity=None):
        self.entity = entity
        self.attr = attr
        self.xz_entity = xz_entity
        if question_type == 'ts':
            self.ts()
        elif question_type == 'tz':
            self.tz()
        elif question_type == 'xz':
            self.xz()
        elif question_type == 'zf':
            self.zf()
        elif question_type == 'sf':
            self.sf()
        else:
            return self.feedback

    def ts(self):
        self.data = self.data_search.search(self.entity, 'cause')
        if self.data is None or self.data == '':
            self.data = self.data_search.search(self.entity, 'brief')
            self.answer = '\n'.join(self.data)
        else:
            self.answer = "主要有以下原因\n" + self.data
        print(self.answer)
        return self.answer

    def tz(self):

        return

    def xz(self):

        return

    def zf(self):

        return

    def sf(self):

        return
