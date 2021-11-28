import networkit as nk
import time

#Betweenness aumenta di 100 volte il tempo di esecuzione ogni x10 del numero di nodi del grafo --> quadratico

#G = nk.readGraph("prova_grafo_medio.txt", nk.Format.EdgeListSpaceZero)
G = nk.readGraph("prova_grafo_piccolo.edges", nk.Format.EdgeListSpaceZero)

print("Max #threads = ", nk.getMaxNumberOfThreads())
#nk.setNumberOfThreads(8)
print("Attualmente attivi = ", nk.getCurrentNumberOfThreads())


print("Number of nodes = ",G.numberOfNodes())
print("Number of edges = ",G.numberOfEdges())


btw = nk.centrality.Betweenness(G)

start = time.time()
btw.run()
end = time.time()

print(btw.ranking()[:10])

print("Tempo trascorso = ", end-start)
