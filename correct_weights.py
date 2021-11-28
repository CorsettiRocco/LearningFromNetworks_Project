import networkx as nx
import networkit as nk

file = open("deter4.txt", "r")
line = "a"
edge_list = []
params = []

while line != "":
    line = file.readline()
    params = line.split()
    if len(params) == 3:
        edge_list.append( (params[0], params[1], params[2]) )

G = nx.Graph()
G.add_weighted_edges_from(edge_list)

print(G.number_of_nodes())
print(G.number_of_edges())

nx.write_gml(G, "prova_grafo_pesato_medio")

G = nk.readGraph("prova_grafo_pesato_medio", nk.Format.GML)

print(G.numberOfNodes())
print(G.numberOfEdges())