from types import CellType
import networkit as nk
import time

G_p = nk.readGraph("prova_grafo_piccolo.edges", nk.Format.EdgeListSpaceZero)
G_m = nk.readGraph("prova_grafo_medio.txt", nk.Format.EdgeListSpaceZero)


btw_p = nk.centrality.ApproxBetweenness(G_p, epsilon = 0.1)
btw_m = nk.centrality.ApproxBetweenness(G_m, epsilon = 0.1)

start = time.time()
btw_p.run()
end = time.time()

time_1 = end - start

start = time.time()
btw_m.run()
end = time.time()

time_2 = end - start

print("Tempo per grafo piccolo = ", time_1)
print("Tempo per grafo medio = ", time_2)
print("Il tempo è incrementato di ", time_2 / time_1 , " volte con il grafo 10 volte più grande")

print("Il grafo da 10^6 ci metterebbe circa: ",(time_2/time_1) * 100 * time_2 / 60, " minuti")

G_g = nk.readGraph("prova_grafo_grande.txt", nk.Format.EdgeListSpaceZero)

btw_g = nk.centrality.ApproxBetweenness(G_g, epsilon = 0.1)

start = time.time()
btw_g.run()
end = time.time()

time_3 = end-start

print("Ci ha messo = ", time_3/60, " minuti")
