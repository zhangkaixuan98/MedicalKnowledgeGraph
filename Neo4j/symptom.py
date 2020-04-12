from py2neo import Graph, Node, NodeMatcher, RelationshipMatcher


class Symptom:
    def __init__(self):
        self.graph = Graph("bolt://localhost:7687", username="neo4j", password='1998')
        self.node_matcher = NodeMatcher(self.graph)
        self.rel_matcher = RelationshipMatcher(self.graph)
        self.search_type = ""
        self.name = ""

    def search(self, search_type, symptom_name):
        self.search_type = search_type
        self.name = symptom_name
        if search_type == "brief":
            return

    # 关系
    def disease(self):
        cql = f"match(p:symptom)-[]->(n:disease) where p.name='{self.name}' " \
            f"return n.name as disease"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def symptom(self):
        cql = f"match(p:symptom)-[]->(n:symptom) where p.name='{self.name}' " \
            f"return n.name as symptom"
        data = self.graph.run(cql).data()
        # cql = f"match(n:symptom)-[]->(p:symptom) where p.name='{self.name}' " \
        #     f"return n.name as symptom"
        # data.extend(self.graph.run(cql).data())
        print(data)
        return data

    # 属性
    def brief(self):
        cql = f"match(n:symptom) where n.name='{self.name}' return n.brief as brief"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def cause(self):
        cql = f"match(n:symptom) where n.name='{self.name}' return n.cause as cause"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def check(self):
        cql = f"match(n:symptom) where n.name='{self.name}' return n.check as check"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def diagnose(self):
        cql = f"match(n:symptom) where n.name='{self.name}' return n.diagnose as diagnose"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def prevent(self):
        cql = f"match(n:symptom) where n.name='{self.name}' return n.prevent as prevent"
        data = self.graph.run(cql).data()
        print(data)
        return data


if __name__ == '__main__':
    handler = Symptom()
    handler.search("", "睡眠节律紊乱")
    handler.disease()
    handler.symptom()
    handler.brief()
    handler.cause()
    handler.check()
    handler.diagnose()
    handler.prevent()
