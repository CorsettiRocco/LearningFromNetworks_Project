import networkx as nx
import networkit as nk
import time

#SAREBBE DA FARCI UNA CLASSE ATTORNO, POI LA SI FA ITERARE IN MODO AUTOMATIZZATO SU TUTTI I GRAFI

#Read a text file that represents an edge list ( all the graphs downloaded up to now use this format)
#By default the delimiter is a space and the graph is unweighted
#Returns a networkx graph
def read_text_graph(file_path, weighted = True, delimiter = " "):
    if weighted:
        graph = nx.read_weighted_edgelist(file_path, delimiter = delimiter)
    else:
        graph = nx.read_edgelist(file_path, delimiter = delimiter)
    return graph

#Read a GML graph
def read_gml_graph(file_path):
    graph = nx.read_gml(file_path)
    return graph

#Save the Graph as GML file to keep track of all the computed scores
def save_graph(graph, file_path):
    nx.write_gml(graph, file_path)



#Compute the betweenness centrality (approximated by default)
#Assign to each node the score as attribute
#Returns the list of scores
def betweenness_centrality(graph, g_kit = None, Approx = True, epsilon = 0.1):
    if g_kit == None:
        #Convert to networkit for better performances
        g_kit = nk.nxadapter.nx2nk(graph)

    #Prepare Algorithm
    if Approx:
        btw = nk.centrality.ApproxBetweenness(g_kit, epsilon = epsilon)
    else:
        btw = nk.centrality.Betweenness(g_kit)

    #Run algorithm (time for statistics)
    start = time.time()
    btw.run()
    end = time.time()

    #Save the scores in the graph
    btw = btw.scores()
    assert(len(btw) == len(graph.nodes))            #PORCO DIO MI DA ERRORE SUL CAZZO DI FOR MADONNA LADRA NON CAPISCO PERCHE'
    #for i in range(len(graph.nodes)):
       #graph.nodes[i]['betweenness'] = btw[i]

    #Return the list of scores and the time
    return btw, (end-start)

#Wrapper to compute all the scores in an automatized way
def compute_scores(graph):
    #Convert the graph just one time
    g_kit = nk.nxadapter.nx2nk(graph)

    #Dictionary that contains all the scores
    scores = {
        'betweenness' : 0
        #...
    }

    times = {
        'betweenness' : 0
        #...
    }

    #Call the other functions
    scores['betweenness'], times['betweenness'] = betweenness_centrality(graph, g_kit)
    #...

    return scores, times

##export_scores(list_of_scores,fp,score_name)
#export nodes values into a csv file:
#id:node
#score_name: score associated for each node
##
    
#@list_of_scores : e.g btw.scores()
#@fp: file path to csv file
#@score_name: name of the score
def export_scores(list_of_scores,fp,score_name):

    nk.gephi.exportNodeValues(list_of_scores,fp,score_name)


G = read_text_graph("Test/Graphs/prova_grafo_piccolo.edges", False)
scores, times = compute_scores(G)

export_scores(scores['betweenness'],"csv/grafo_piccolo_btw.csv","btw")

scores['betweenness'].sort()
print("Top 10 scores = ", scores['betweenness'][len(scores['betweenness']) - 10 : len(scores['betweenness'])])
#save_graph(G, "prova") --> Inutile finchè non sistemo il for che non capisco perchè non vada che nell'altro programma andava
