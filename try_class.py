from Compute_Scores import Scores_Calculator

def print_results(CS):
    scores, ranking, times = CS.get_results()
    for key in scores:
        scores[key].sort()
        print("Best ", key, " scores: ", scores[key][ len(scores[key] ) - 5 : len(scores[key])])
        print("Best ", key, " scores through ranking: ", ranking[key][:5])
        print(key," execution time = ", times[key], " sec")
        print("\n")


    

CS = Scores_Calculator(name='btw_small_graph')
CS.read_text_graph("Test/Graphs/prova_grafo_piccolo.edges")
CS.compute_scores()

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

CS.voting_rule(type = 'all')

CS.export_scores("csv/", "betweenness")
#test new column
CS.export_scores("csv/", "closeness")

print("\nEXACT VERSION:\n")
#print_results(CS)

print("\nWITH LESS NODES\n")
CS.delete_nodes([1170, 1171, 1174])
#print_results(CS)


