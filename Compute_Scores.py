import networkit as nk
import networkx as nx
import time 
import csv
import os

#The class provides a way to compute and store some node-scores
#Provide a methods to:
#   - Compute a score in the exact or approximated way
#   - A wrapper method to compute all the scores
#   - A method to save the scores in a csv file
#   - A method to read a file from an edge_list
#   - A method to upload a graph (if already read)
#   - Some access method to set the parameters for the computation

#The attribute are:
#   - The networkit Graph
#   - Dictionary of attributes for the approximate algorithms
#   - Dictionary containing list of different scores
#   - Dictionary containing the execution time needed to compute a score ( statistical information )

class Scores_Calculator:
    #ATTRIBUTES

    graph = None
    
    scores = {
        'betweenness' : []
    }
    
    times = {
        'betweenness' : 0
    }

    #Parameter for the approximated algorithm
    params = {
        'betweenness' : { 'approx' : True , 'epsilon' : 0.1 , 'normalized' : True}
    }

    #METHODS

    #Constructor with optional graph as parameter
    def __init__(self, g = None, weighted = False ,network_x = False,name = ''):
        if g != None:
            if network_x:
                self.graph = nk.nxadapter.nx2nk(g)
            else:
                self.graph = g
            if weighted:
                self.graph = nk.graphtools.toWeighted(self.graph)
        
        #set first time value for csv generation
        self.first_time = True
        #set instance name used for csv file set and retrivial
        self.name = name

    #Method that read a text file containing an edge_list and initialize the corresponding networkit graph
    def read_text_graph(self, file_path, weighted = False, format = nk.Format.EdgeListSpaceZero):
        self.graph = nk.readGraph(file_path, format)
        if weighted:
            self.graph = nk.graphtools.toWeighted(self.graph)

    #Method to set the graph in the class
    def set_graph(self, g, weighted = False, network_x = False):
        if network_x:
            self.graph = nk.nxadapter.nx2nk(g)
        else:
            self.graph = g
        if weighted:
            self.graph = nk.graphtools.toWeighted(self.graph)

    #Method that returns the dictionary params, if it is needed to change something
    def get_params(self):
        return self.params

    #Method that sets the new params for the algorithm, take the exact dict as input
    def set_params(self, p):
        self.params = p

    #Method that sets a single parameter of a single algorithm
    def set_param_value(self, score_name, param_name, value):
        self.params[score_name][param_name] = value

    #Method that returns the scores and the times
    def get_results(self):
        return self.scores, self.times

    #Method that enable/disable the approximation for every algorithm
    def set_approx(self, approx):
        for key in self.params:
            self.params[key]['approx'] = approx

    ##
    #export_scores(list_of_scores,fp,score_name)
    #export nodes values into a csv file:
    #id:node
    #score_name: score associated for each node
    #@list_of_scores : e.g btw.scores()
    #@path: folder path to csv file
    #@score_name: name of the score
    ##
    def export_scores(self, path, score_name):

        if self.first_time:
            #if first time create associated csv file
            path = path + self.name +'.csv'                                        
            nk.gephi.exportNodeValues(self.scores[score_name], path, score_name)
        else:
            #else append a new column to existing file
            path_temp = path + 'temp.csv'
            nk.gephi.exportNodeValues(self.scores[score_name], path_temp, score_name)

            #append new column of score to csv associated with this instance
            with open(path_temp,'r') as rd, open(path+self.name+'.csv','w',newline='') as wrt:
                csv_reader = csv.reader(rd)
                csv_writer = csv.writer(wrt)

                for row in csv_reader:
                    row.append(row[1])
                    csv_writer.writerow(row)
            
            #remove temp.csv 
            os.remove(path_temp)

        self.first_time = False


    #Method that compute the betweenness centrality of a node
    def betweenness_centrality(self):
        if self.params['betweenness']['approx']:
            btw = nk.centrality.ApproxBetweenness(self.graph, self.params['betweenness']['epsilon'])
        else:
            btw = nk.centrality.Betweenness(self.graph, self.params['betweenness']['normalized'])
        
        start = time.time()
        btw.run()
        end = time.time()

        self.scores['betweenness'] = btw.scores()
        self.times['betweenness'] = end-start

    #Wrapper method that compute all the scores for a graph
    #To modify to add new scores
    def compute_scores(self):
        self.betweenness_centrality()

        return self.scores, self.times