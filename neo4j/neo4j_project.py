import csv
import py2neo
from py2neo import Graph, Node, Relationship, NodeMatcher

g = Graph('http://localhost:7474', username='neo4j', password='2454neo4j.WJC')

with open('shuihuzhuan.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for item in reader:
        if reader.line_num == 1:
            continue
        print("当前行数: ", reader.line_num, "当前内容：", item)
        start_node = Node("Person", name=item[0])
        end_node = Node("Person", name=item[1])
        relation = Relationship(start_node, item[3], end_node)
        g.merge(start_node, "Person", "name")
        g.merge(end_node, "Person", "name")
        g.merge(relation, "Person", "name")

# MATCH (p: Person {name:"贾宝玉"})-[k:丫鬟]-(r)
# return p,k,r

# MATCH (p1:Person {name:"贾宝玉"}),(p2:Person{name:"香菱"}),p=shortestpath((p1)-[*..10]-(p2))
# RETURN p

"""
# g.run('match (n) detach delete n')
test_node_1 = Node("Person", name="Bili_1")
test_node_2 = Node("Person", name="Bili_2")

test_node_1['age'] = 18
test_node_1['sex'] = 'male'
test_node_2['age'] = 19
test_node_2['sex'] = 'female'
# 创建结点
# g.create(test_node_1)
# g.create(test_node_2)
# 覆盖式创建结点
g.merge(test_node_1, "Person", "name")
g.merge(test_node_2, "Person", "name")

friend = Relationship(test_node_1, 'friend', test_node_2)
g.merge(friend, "Person", "name")

matcher = NodeMatcher(g)
print(matcher.match("Person").first())
"""
