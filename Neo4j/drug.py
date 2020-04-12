from py2neo import Graph, Node, NodeMatcher, RelationshipMatcher


class Drug:
    def __init__(self):
        self.graph = Graph("bolt://localhost:7687", username="neo4j", password='1998')
        self.node_matcher = NodeMatcher(self.graph)
        self.rel_matcher = RelationshipMatcher(self.graph)
        self.search_type = ""
        self.name = ""

    def search(self, search_type, drug_name):
        self.search_type = search_type
        self.name = drug_name
        if search_type == "disease":
            return self.disease()
        elif search_type == "form":
            self.form()
        elif search_type == "function":
            self.function()
        elif search_type == "usage":
            self.usage()
        elif search_type == "component":
            self.component()
        elif search_type == "effects":
            self.effects()
        elif search_type == "avoid":
            self.avoid()
        elif search_type == "matters":
            self.matters()

    def disease(self):
        cql = f"match(n:disease)-[r:disease_drug]->(p:drug) where p.name='{self.name}' " \
            f"return n.name as disease order by n.proportion desc"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def form(self):
        cql = f"match(n:form)-[r:form_drug]->(p:drug) where p.name='{self.name}' " \
            f"return n.name as form"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def function(self):
        cql = f"match(n:drug) where n.name='{self.name}' return n.function as function"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def usage(self):
        cql = f"match(n:drug) where n.name='{self.name}' return n.usage as usage"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def component(self):
        cql = f"match(n:drug) where n.name='{self.name}' return n.component as component"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def effects(self):
        cql = f"match(n:drug) where n.name='{self.name}' return n.effects as effects"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def avoid(self):
        cql = f"match(n:drug) where n.name='{self.name}' return n.avoid as avoid"
        data = self.graph.run(cql).data()
        print(data)
        return data

    def matters(self):
        cql = f"match(n:drug) where n.name='{self.name}' return n.matters as matters"
        data = self.graph.run(cql).data()
        print(data)
        return data


if __name__ == '__main__':
    handler = Drug()
    handler.search("", "消癌平片")
    handler.disease()
    handler.form()
    handler.function()
    handler.usage()
    handler.component()
    handler.effects()
    handler.avoid()
    handler.matters()
