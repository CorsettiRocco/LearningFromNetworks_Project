import networkit as nk
import time 

G_w = nk.readGraph("prova_grafo_pesato_medio", nk.Format.GML)
G = nk.readGraph("prova_grafo_medio.txt", nk.Format.EdgeListSpaceZero)

btww = nk.centrality.Betweenness(G_w)
btw = nk.centrality.Betweenness(G)

start = time.time()
btww.run()
end = time.time()

print("Time for weighted = ", end-start)

start = time.time()
btw.run()
end = time.time()

print("Time for unw = ", end-start)
