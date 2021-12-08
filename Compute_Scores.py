import networkit as nk
import networkx as nx
import time 
import csv
import os
import pandas as pd
from random import randint

#The class provides a way to compute and store some node-scores
#Provide methods to:
#   - Compute a score in the exact or approximated way
#   - A wrapper method to compute all the scores
#   - A method to save the scores in a csv file
#   - A method to read a file from an edge_list
#   - A method to upload a graph (if already read)
#   - Some access methods to set the parameters for the computation
#   - Check the number of connected components (useful for some algorithms that requires connected components) and return the #components
#   - Voting rule method to identify most influential nodes
#   - Create a subgraph that exclude some nodes

#The attributes are:
#   - The networkit Graph
#   - Dictionary of attributes for the approximate algorithms
#   - Dictionary containing list of different scores
#   - Dictionary containing the execution time needed to compute a score ( statistical information )
#   - Dictionary containing the results of the voting

class Scores_Calculator:
    #ATTRIBUTES

    graph = None
    
    #Dict that saves all the computed scores
    scores = {
        'betweenness' : [],
        'closeness' : [],
        'degree' : [],
        'eigenvector' : [],
        'page' : [],
        'clustering' : [],
        'katz' : []
    }

    #Dict that saves the ranking of each score
    #A ranking of a score is a list of tuples, in which the first element represents the id of the node, and the second element represents the score of that node
    #The list is sorted in a decrescent way, the most important nodes are the first in the list
    ranking = {
        'betweenness' : [],
        'closeness' : [],
        'degree' : [],
        'eigenvector' : [],
        'page' : [],
        'clustering' : [],
        'katz' : []
    }
    
    #Dict that saves the computational time needed by each score
    times = {
        'betweenness' : 0,
        'closeness' : 0,
        'degree' : 0,
        'eigenvector' : 0,
        'page' : 0,
        'clustering' : 0,
        'katz' : 0
    }

    #Parameters for the algorithm
    #Used even for different algorithm, in this way there is a unique access method
    params = {
        'betweenness' : {'approx' : True , 'epsilon' : 0.1 , 'delta' : 0.1 , 'normalized' : True},
        'closeness' : {'approx' : True, 'epsilon' : 0.1, 'normalized' : True, 'nSamples' : 10, 'variant' : 1},   #Variant 1 ==> Generalized, 0 ==> Standard (Standard non feasible for disconnected graphs)
        'degree' : {'normalized' : True},
        'eigenvector': {'tolerance' : 1e-9},
        'page' : {'damp' : 0.85, 'tolerance' : 1e-9, 'maxIterations' : -1, 'norm' : 'l2'},
        'clustering' : {'turbo' : True},
        'katz' : {'alpha' : 5e-4, 'beta' : 0.1, 'tolerance' : 1e-8},
        'choose_candidate' : {'voting_rule' : 'borda_count', 'selected' : 1 ,'candidates' : 5, 'random' : False, 'random_range' : 5}   #Used to select the nodes to remove
    }

    #voting rule results
    results_voting_rule = {
        'borda_count' : {},
        'single_count': {},
        'majority_count': {}
    }

    #Represent the name of the graph, it will be used to save the computed scores
    name = None

    #Attribute used to manage the correct saving of the scores in the csv file
    first_time = None

    #Majority vote rule winner
    majority_winner = None

    #Blacklist = List of nodes that will be eliminated
    blacklist = []

    #METHODS

    #Constructor with optional graph as parameter
    def __init__(self, graph = None, weighted = False , network_x = False, name = ''):
        if graph != None:
            if network_x:
                self.graph = nk.nxadapter.nx2nk(graph)
            else:
                self.graph = graph
            if weighted:
                self.graph = nk.graphtools.toWeighted(self.graph)
        
        #set first time value for csv generation
        self.first_time = True
        #set instance name used for csv file set and retrivial
        self.name = name

    #Method that reads a text file containing an edge_list and initialize the corresponding networkit graph
    def read_text_graph(self, file_path, weighted = False, format = nk.Format.EdgeListSpaceZero, name = ''):
        self.graph = nk.readGraph(file_path, format)
        if weighted:
            self.graph = nk.graphtools.toWeighted(self.graph)
        #set instance name used for csv file set and retrivial
        self.name = name

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
        return self.scores, self.ranking, self.times, self.results_voting_rule

    #Method that returns the graph
    def get_graph(self):
        return self.graph

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

            #save to csv
            write.to_csv(path_original,index=False)
            
            #remove temp.csv 
            os.remove(path_temp)   

    
    #Method that return the number of connected components of the network
    def connected_components(self):
        #Prepare the algorithm
        cc = nk.components.ConnectedComponents(self.graph)
        #Run the algorithm
        cc.run()
        return  cc.numberOfComponents()

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

    #Method that computes the Closeness Centrality of the nodes        
    def closeness_centrality(self):
        #If the approx attribute is true, use an approximated version of the algorithm, otherwise the exact one
        if self.params['closeness']['approx']:
            #It requires a connected graph
            #assert self.connected_components()[0] == 1, "Graph not connected, cannot apply approximation\n"
            ncc = self.connected_components()
            if ncc >=2:
                print("Graph not connected , cannot apply closeness centrality approximation. ( Number of components = ", ncc, ")")
                return
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


    #Methods that compute the degree centrality of the nodes
    def degree_centrality(self):
        #Setup the algorithm
        dc = nk.centrality.DegreeCentrality(self.graph, self.params['degree']['normalized'])

        #Run the algorithm
        start = time.time()
        dc.run()
        end = time.time()

        #Save the results
        self.scores['degree'] = dc.scores()
        self.ranking['degree'] = dc.ranking()
        self.times['degree'] = end - start


    #Mehtods that computes the eigenvector centrality
    def eigenvector_centrality(self):
        #Setup algorithm
        ec = nk.centrality.EigenvectorCentrality(self.graph, self.params['eigenvector']['tolerance'])

        #Run algorithm
        start = time.time()
        ec.run()
        end = time.time()

        #Save results
        self.scores['eigenvector'] = ec.scores()
        self.ranking['eigenvector'] = ec.ranking()
        self.times['eigenvector'] = end - start


    #Methods that compute the page rank score
    def page_rank(self):
        #setup the algorithm
        pr = nk.centrality.PageRank(self.graph, self.params['page']['damp'], self.params['page']['tolerance'])
        #Set max iters only if modified, otherwise default
        if self.params['page']['maxIterations'] != -1:
            pr.maxIterations = self.params['page']['maxIterations']
        if self.params['page']['norm'] == 'l1':
            pr.norm = nk.centrality.Norm.l1norm
        else:
            pr.norm = nk.centrality.Norm.l2norm

        #Run the algorithm
        start = time.time()
        pr.run()
        end = time.time()

        #Save the results
        self.scores['page'] = pr.scores()
        self.ranking['page'] = pr.ranking()
        self.times['page'] = end - start


    #Method that computes the local clustering coefficient
    def local_clustering_coefficient(self):
        #Setup the algorithm
        lcc = nk.centrality.LocalClusteringCoefficient(self.graph, self.params['clustering']['turbo'])

        #Run the algorithm
        start = time.time()
        lcc.run()
        end = time.time()

        #save the results
        self.scores['clustering'] = lcc.scores()
        self.ranking['clustering'] = lcc.ranking()
        self.times['clustering'] = end - start

    
    #Mehtod that computes the katz centrality
    def katz_centrality(self):
        #Setup the algorithm
        kc = nk.centrality.KatzCentrality(self.graph, self.params['katz']['alpha'], self.params['katz']['beta'], self.params['katz']['tolerance'])

        #Run the algorithm
        start = time.time()
        kc.run()
        end = time.time()

        #Save teh results
        self.scores['katz'] = kc.scores()
        self.ranking['katz'] = kc.ranking()
        self.times['katz'] = end - start


    #Wrapper method that computes all the scores for a graph
    #To modify to add new scores
    def compute_scores(self):
        self.betweenness_centrality()
        self.closeness_centrality()
        self.degree_centrality()
        self.eigenvector_centrality()
        self.page_rank()
        self.local_clustering_coefficient()
        self.katz_centrality()

        return self.scores, self.ranking ,self.times

    #Problem with the approximated computation ( Closeness centrality in its approximated version isn't always computable
    #       when this happen the method fail ) [Try using the try_class.py file removing set_approx(False)]
    #Problem when the majority vote has a winner (it happend with random elimination, hence is difficult to have the error)
    #       [To try to have the error, delete the '#' in the 2 lines before the creation of the subgraph and execute some times, ti should happe]
    #voting rule to identify the most influential nodes in the network based on the scores(voters) and nodes(candidates)
    def voting_rule(self, type = 'borda_count', candidates = 5, print_res = True):

        #Keep track of the params considered to keep consistency in the methods
        self.params['choose_candidate']['voting_rule'] = type
        self.params['choose_candidate']['candidates'] = candidates

        #points are assigned based on the ranking of the size of candidates( equal to 5 by default)
        if type == 'borda_count' or 'all':        
            for ranks in self.ranking:
                for i in range(candidates):
                    if str(self.ranking[ranks][i][0]) in self.results_voting_rule['borda_count']:
                        self.results_voting_rule['borda_count'][str(self.ranking[ranks][i][0])] += (candidates - i)
                    else:
                        self.results_voting_rule['borda_count'][str(self.ranking[ranks][i][0])] = 1
        #each candidate receive a single point if it is in the top 5
        if type == 'single_count' or 'all':
            for ranks in self.ranking:
                for i in range(candidates):
                    if str(self.ranking[ranks][i][0]) in self.results_voting_rule['single_count']:
                        self.results_voting_rule['single_count'][str(self.ranking[ranks][i][0])] += 1
                    else:
                        self.results_voting_rule['single_count'][str(self.ranking[ranks][i][0])] = 1
        #each voter votes for the most prefered candidate, if the candidate receives more then of the majority of voters it is selected
        if type == 'majority_count' or 'all':
            for ranks in self.ranking:
                if str(self.ranking[ranks][0][0]) in self.results_voting_rule['majority_count']:
                    self.results_voting_rule['majority_count'][str(self.ranking[ranks][0][0])] += 1
                else:
                    self.results_voting_rule['majority_count'][str(self.ranking[ranks][0][0])] = 1
                

        #sort the voting 
        for counts in self.results_voting_rule:
            self.results_voting_rule[counts]={k: v for k, v in sorted(self.results_voting_rule[counts].items(), key=lambda item: item[1], reverse = True)}

        #evaluate if a majority winner exists
        if (list(self.results_voting_rule['majority_count'].values())[0] >= len(self.ranking)) and (type == 'majority_count' or 'all'):
            print('Node: ',list(self.results_voting_rule['majority_count'].keys())[0],' wins the majority with ',\
            list(self.results_voting_rule['majority_count'].values())[0],' votes')
            self.majority_winner = int(list(self.results_voting_rule['majority_count'].keys())[0])
        else:
            print('No majority voting rule winner')

        df_voting = pd.DataFrame(self.results_voting_rule)

        #save to .csv in './voting_results/'
        df_voting.to_csv('voting_results/'+'votes_'+self.name+'.csv')
        
        #print results
        if type == 'all':
            width = 48
        else:
            width = 18

        if print_res:
            print('-'*width)        
            print(df_voting)
            print('-'*width)

        return self.results_voting_rule

    
    #Method that can be used to choose some nodes to be eliminated in an automatic way
    #It will choose, by default, the most important node using the voting rule
    #It could choose more nodes to remove
    #It could choose randomly n_candidates to remove from random_range of ranked nodes
    def choose_candidates(self):
        #If voting_rule = 'all', set Borda Count by default
        if self.params['choose_candidate']['voting_rule'] == 'all':
            self.params['choose_candidate']['voting_rule'] = 'borda_count'

        blacklist = []
        keys = list(self.results_voting_rule[ self.params['choose_candidate']['voting_rule'] ].keys())

        #If random is false, select the first #candidates nodes
        if self.params['choose_candidate']['random'] == False:
            blacklist = keys[ : self.params['choose_candidate']['candidates'] ]
        else:   #Select #candidates randomly from the first random_range elements
            #Check random range
            if self.params['choose_candidate']['random_range'] > self.params['choose_candidate']['candidates']:
                self.params['choose_candidate']['random_range'] = self.params['choose_candidate']['candidates']
            #Restrict the keys list
            keys = keys[:self.params['choose_candidate']['random_range']]
            #Select #candidates
            for i in range(self.params['choose_candidate']['candidates']):
                rand = randint(0, len(keys) - 1)
                while keys[rand] in blacklist:
                    rand = randint(0, len(keys) - 1)
                blacklist.append(keys[rand])

        #Check consistency between selected and candidates
        if self.params['choose_candidate']['selected'] > self.params['choose_candidate']['candidates']:
            self.params['choose_candidate']['selected'] = self.params['choose_candidate']['candidates']

        #Save the blacklist
        self.blacklist = blacklist[:self.params['choose_candidate']['selected']]





    #Method that return a subgraph, takes a blacklist of nodes as input
    def delete_nodes(self, blacklist = None):
        #Create a list of nodes that do not contains the nodes in the blacklist
        nodes = [node for node in self.graph.iterNodes()]

        #If the blacklist isn't set, set it
        if blacklist == None:
            self.choose_candidates()
            blacklist = self.blacklist

        #Remove the nodes in the blacklist
        for node in blacklist:
            nodes.remove(int(node))

        #Create the subgraph
        subgraph = nk.graphtools.subgraphFromNodes(self.graph, nodes)
        
        #To automatize the process I would write this line, then, I would reexecute compute scores
        #self.graph = subgraph
        #self.compute_scores()

        #Now I just return the graph
        return subgraph


    def print_results(self):
        for key in self.ranking:
            print("Best ", key, " scores: ", self.ranking[key][:5])
            print(key," execution time = ", self.times[key], " sec")
            print("\n")

        

