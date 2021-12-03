import networkit as nk
import networkx as nx
import time 
import csv
import os
import pandas as pd

#The class provides a way to compute and store some node-scores
#Provide methods to:
#   - Compute a score in the exact or approximated way
#   - A wrapper method to compute all the scores
#   - A method to save the scores in a csv file
#   - A method to read a file from an edge_list
#   - A method to upload a graph (if already read)
#   - Some access methods to set the parameters for the computation

#The attributes are:
#   - The networkit Graph
#   - Dictionary of attributes for the approximate algorithms
#   - Dictionary containing list of different scores
#   - Dictionary containing the execution time needed to compute a score ( statistical information )

class Scores_Calculator:
    #ATTRIBUTES

    graph = None
    
    #Dict that saves all the computed scores
    scores = {
        'betweenness' : [],
        'closeness' : []
    }

    #Dict that saves the ranking of each score
    #A ranking of a score is a list of tuples, in which the first element represents the id of the node, and the second element represents the score of that node
    #The list is sorted in a decrescent way, the most important nodes are the first in the list
    ranking = {
        'betweenness' : [],
        'closeness' : []
    }
    
    #Dict that saves the computational time needed by each score
    times = {
        'betweenness' : 0,
        'closeness' : 0
    }

    #Parameters for the approximated algorithm
    params = {
        'betweenness' : {'approx' : True , 'epsilon' : 0.1 , 'delta' : 0.1 , 'normalized' : True},
        'closeness' : {'approx' : True, 'epsilon' : 0.1, 'normalized' : True, 'nSamples' : 10, 'variant' : 1}   #Variant 1 ==> Generalized, 0 ==> Standard (Standard non feasible for disconnected graphs)
    }

    #Represent the name of the graph, it will be used to save the computed scores
    name = None

    #Attribute used to manage the correct saving of the scores in the csv file
    first_time = None

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

    #Method that reads a text file containing an edge_list and initialize the corresponding networkit graph
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

    #Method that sets the new params for the algorithms, take the exact dict as input
    def set_params(self, p):
        self.params = p

    #Method that sets a single parameter of a single algorithm
    def set_param_value(self, score_name, param_name, value):
        self.params[score_name][param_name] = value

    #Method that returns the scores and the times
    def get_results(self):
        return self.scores, self.ranking,self.times

    #Method that enable/disable the approximation for each algorithm
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

            self.first_time = False
        else:
            #else append a new column to existing file
            path_temp = path + 'temp.csv'
            path_original = path+self.name+'.csv'
            nk.gephi.exportNodeValues(self.scores[score_name], path_temp, score_name)

            #append new column of score to csv associated with this instance

            write = pd.read_csv(path_original)
            read = pd.read_csv(path_temp)

            write[score_name] = read[score_name]

            #remove original 
            os.remove(path_original)

            #save to csv
            write.to_csv(path_original,index=False)
            
            #remove temp.csv 
            os.remove(path_temp)   


    #Method that computes the betweenness centrality of a node
    def betweenness_centrality(self):
        #If the approx attribute is true, use an approximated version of the algorithm, otherwise the exact one
        if self.params['betweenness']['approx']:
            btw = nk.centrality.ApproxBetweenness(self.graph, self.params['betweenness']['epsilon'], self.params['betweenness']['delta'])
        else:
            btw = nk.centrality.Betweenness(self.graph, self.params['betweenness']['normalized'])
        
        #Run the algorithm
        start = time.time()
        btw.run()
        end = time.time()

        #Save the results
        self.scores['betweenness'] = btw.scores()
        self.ranking['betweenness'] = btw.ranking()
        self.times['betweenness'] = end-start

    #Method that computes the Closeness Centrality of a node        APPROXIMATION CURRENTLY NOT WORKING!!!
    def closeness_centrality(self):
        #If the approx attribute is true, use an approximated version of the algorithm, otherwise the exact one
        if self.params['closeness']['approx']:
            cln = nk.centrality.ApproxCloseness(self.graph, self.graph.numberOfNodes(), self.params['closeness']['epsilon'], self.params['closeness']['normalized'])
        else:
            cln = nk.centrality.Closeness(self.graph, self.params['closeness']['normalized'], self.params['closeness']['variant'])

        #Run the algorithm
        start = time.time()
        cln.run()
        end = time.time()

        #Save the results
        self.scores['closeness'] = cln.scores()
        self.ranking['closeness'] = cln.ranking()
        self.times['closeness'] = (end - start)   

    #Wrapper method that computes all the scores for a graph
    #To modify to add new scores
    def compute_scores(self):
        self.betweenness_centrality()
        self.closeness_centrality()

        return self.scores, self.ranking ,self.times