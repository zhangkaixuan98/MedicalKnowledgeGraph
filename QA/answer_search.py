from py2neo import Graph, Node, NodeMatcher, RelationshipMatcher
from Neo4j import disease, symptom, drug

class AnswerSearch:
    def __init__(self):
        self.graph = Graph("bolt://localhost:7687", username="neo4j", password='1998')
        self.node_matcher = NodeMatcher(self.graph)
        self.rel_matcher = RelationshipMatcher(self.graph)
        self.disease = disease.Disease()
        self.symptom = symptom.Symptom()
        self.drug = drug.Drug()
    # 主函数
    def search(self, entity, attr_type):

        entity_name = entity[0]
        entity_type = entity[1]
        attr = attr_type
        if entity_type == "disease":
            return self.disease.search(attr, entity_name)
        elif entity_type == "symptom":
            return self.symptom.search(attr, entity_name)
        elif entity_type == "drug":
            return self.drug.search(attr, entity_name)
        elif entity_type == "check":
            return
        elif entity_type == "population":
            return
        elif entity_type == "department":
            return
    # 检查
    def check(self, answer_type, entity):
        return

    # 人群
    def population(self, answer_type, entity):
        return





if __name__ == '__main__':
    handler = AnswerSearch()