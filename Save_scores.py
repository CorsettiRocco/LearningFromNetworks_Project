import networkit as nk
import networkx as nx

#UPLOAD THE GRAPH (networkit has a cool way to do it)
G = nk.readGraph("prova_grafo_piccolo.edges", nk.Format.EdgeListSpaceZero)

#APPLY THE ALGORITHM(s)
btw = nk.centrality.Betweenness(G)
btw.run()

#GO BACK TO NETWORKX TO MANAGE THE GRAPH
G_x = nk.nxadapter.nk2nx(G)
btw = btw.scores()

#ASSING THE SCORES TO THE NODES AS ATTRIBUTE OF THE NODE
for i in range(G.numberOfNodes()):
    G_x.nodes[i]['btw'] = btw[i]

#SAVE GRAPH WITH GML FORMAT TO KEEP TRACK OF THE SCORES
nx.write_gml(G_x, "grafo_piccolo_con_scores")
