from py2neo import Graph, NodeMatcher, RelationshipMatcher
from Neo4j import disease


class Alias:
    def __init__(self):
        self.graph = Graph("bolt://localhost:7687", username="neo4j", password='1998')
        self.node_matcher = NodeMatcher(self.graph)
        self.rel_matcher = RelationshipMatcher(self.graph)
        self.search_type = ""
        self.name = ""
        self.disease = disease.Disease()

    def search(self, search_type, alias_name):
        self.search_type = search_type
        self.name = alias_name
        disease_name = self.disease_name()
        return self.disease.search(self.search_type, disease_name)

    # 关系
    def disease_name(self):
        """
        查询别名所对应的疾病
        :return: 疾病
        """
        cql = f"match(n:disease)-[]->(p:alias) where p.name='{self.name}' " \
            f"return n.name as disease"
        data = self.graph.run(cql).data()[0]['disease']
        # print(data)
        return data


if __name__ == '__main__':
    handler = Alias()
    handler.search("cause", "头疼")

