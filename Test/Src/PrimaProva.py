import networkit as nk
import time


#Betweenness aumenta di 100 volte il tempo di esecuzione ogni x10 del numero di nodi del grafo --> quadratico

#G = nk.readGraph("prova_grafo_medio.txt", nk.Format.EdgeListSpaceZero)
G = nk.readGraph("../Graphs/prova_grafo_piccolo.edges", nk.Format.EdgeListSpaceZero)

print("Max #threads = ", nk.getMaxNumberOfThreads())
#nk.setNumberOfThreads(8)
print("Attualmente attivi = ", nk.getCurrentNumberOfThreads())


print("Number of nodes = ",G.numberOfNodes())
print("Number of edges = ",G.numberOfEdges())


btw = nk.centrality.Betweenness(G)

start = time.time()
btw.run()
end = time.time()

rank=btw.ranking()[:10]
print(rank)
print(type(rank))

#export nodes values into a csv file
#id:node
#btw_score: btw for each node
nk.gephi.exportNodeValues(btw.scores(),"test.csv","btw_score")

print("Tempo trascorso = ", end-start)
