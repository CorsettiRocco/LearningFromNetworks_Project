from Compute_Scores import Scores_Calculator


#The print_results function it's now embedded in the class

    
#ENTIRE PIPELINE

#Init
CS = Scores_Calculator(name='road-italy-osm')
CS.read_text_graph("Graphs/road-italy-osm.edges")

#Compute scores and analyze                                      
CS.compute_scores(print_log = True)
#CS.print_results()
rvr = CS.voting_rule(type = 'borda_count', print_res = False)
print(rvr['borda_count'].keys())

#Remove node(s)
CS.set_param_value('choose_candidate', 'random', True)
CS.set_param_value('choose_candidate', 'selected', 1)
subgraph = CS.delete_nodes()

#Recompute scores and analyze
CS_sub = Scores_Calculator(graph = subgraph, name = 'btw_small_subgraph')
#CS_sub.set_approx(False)
CS_sub.compute_scores()
CS_sub.print_results()
rvr_sub = CS_sub.voting_rule(type = 'borda_count', print_res = False)
print(rvr_sub['borda_count'].keys())




#Old tries
"""
print("\nAPPROXIMATED VERSION:\n")
print_results(CS)


params = CS.get_params()
params['betweenness']['epsilon'] = 0.01
params['closeness']['epsilon'] = 0.01
CS.set_params(params)
CS.compute_scores()
print("\nAPPROXIMATED VERSION WITH LOWER EPSILON:\n")
print_results(CS)

#All equivalent to modify a parameter

CS.set_approx(False)   #All the algorithms are no longer approximated

#params = CS.get_params()
#params['betweenness']['approx'] = False
#CS.set_params(params)

#CS.set_param_value('betweenness', 'approx', False)

CS.compute_scores()

CS.voting_rule()

CS.export_scores("csv/", "betweenness")
#test new column
CS.export_scores("csv/", "closeness")

print("\nEXACT VERSION:\n")
#print_results(CS)

print("\nWITH LESS NODES\n")
CS.delete_nodes([1170, 1171, 1174])
#print_results(CS)


print("Original #nodes = ", CS.get_graph().numberOfNodes())
print("Original #edges = ", CS.get_graph().numberOfEdges())
CS.set_param_value('choose_candidate', 'random', True)
CS.set_param_value('choose_candidate', 'selected', 3)
sub = CS.delete_nodes()
print("Nodes after = ", sub.numberOfNodes())
print("Edges after = ", sub.numberOfEdges())


print("\nENTIRE PIPELINE\n")
CS.compute_scores()
print_results(CS)
CS.voting_rule(type = 'all')

subgraph = CS.delete_nodes()
CS_sub = Scores_Calculator(name = "small_sub_graph")
CS_sub.set_graph(subgraph)
CS_sub.compute_scores()
print_results(CS_sub)
CS_sub.voting_rule(type = 'all')
"""


