import networkx as nx

G = nx.Graph()

G.add_node('1', position = 23)
G.add_node('2', position = 24)

G.add_edge('1','2', meaning = 'meaningless')

a = G.nodes['1']['position']

G.nodes['1']['position']=24

print(G.nodes['1']['position'])

print(G.edges)

G.remove_node('2')

print(G.edges)