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

    #Parameters for the approximated algorithm
    params = {
        'betweenness' : {'approx' : True , 'epsilon' : 0.1 , 'delta' : 0.1 , 'normalized' : True},
        'closeness' : {'approx' : True, 'epsilon' : 0.1, 'normalized' : True, 'nSamples' : 10, 'variant' : 1},   #Variant 1 ==> Generalized, 0 ==> Standard (Standard non feasible for disconnected graphs)
        'degree' : {'normalized' : True},
        'eigenvector': {'tolerance' : 1e-9},
        'page' : {'damp' : 0.85, 'tolerance' : 1e-9, 'maxIterations' : -1, 'norm' : 'l2'},
        'clustering' : {'turbo' : True},
        'katz' : {'alpha' : 5e-4, 'beta' : 0.1, 'tolerance' : 1e-8}
    }

    #voting rule results
    results_voting_rule = {
        'borda_count' : {},
        'single_count': {}
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

    #voting rule to identify the most influential nodes in the network based on the scores(voters) and nodes(candidates)
    def voting_rule(self,type = 'borda_count',voters = 5):

        if type == 'borda_count' or 'all':        
            for ranks in self.ranking:
                for i in range(voters):
                    if str(self.ranking[ranks][i][0]) in self.results_voting_rule['borda_count']:
                        self.results_voting_rule['borda_count'][str(self.ranking[ranks][i][0])] += (voters - i)
                    else:
                        self.results_voting_rule['borda_count'][str(self.ranking[ranks][i][0])] = 1
        if type == 'single_count' or 'all':
            for ranks in self.ranking:
                for i in range(voters):
                    if str(self.ranking[ranks][i][0]) in self.results_voting_rule['single_count']:
                        self.results_voting_rule['single_count'][str(self.ranking[ranks][i][0])] += 1
                    else:
                        self.results_voting_rule['single_count'][str(self.ranking[ranks][i][0])] = 1


        #sort the voting 
        for counts in self.results_voting_rule:
            print(counts)
            self.results_voting_rule[counts]={k: v for k, v in sorted(self.results_voting_rule[counts].items(), key=lambda item: item[1], reverse = True)}

        df_voting = pd.DataFrame(self.results_voting_rule)

        #save to .csv in /voting_results/
        df_voting.to_csv('voting_results/'+'votes_'+self.name+'.csv')
        
        #print results
        width = 50
        print('-'*width)        
        print(df_voting)
        print('-'*width)

    #Method that return a subgraph, takes a blacklist of nodes as input
    def delete_nodes(self, blacklist = None):
        #Create a list of nodes that do not contains the nodes in the blacklist
        nodes = [node for node in self.graph.iterNodes()]
    
        #Remove the nodes in the blacklist
        for node in blacklist:
            nodes.remove(node)

        #Create the subgraph
        subgraph = nk.graphtools.subgraphFromNodes(self.graph, nodes)
        
        #To automatize the process I would write this line, then, I would reexecute compute scores
        #self.graph = subgraph
        #self.compute_scores()

        #Now I just return the graph
        return subgraph

