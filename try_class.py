from Compute_Scores import Scores_Calculator

CS = Scores_Calculator()
CS.read_text_graph("Test/Graphs/prova_grafo_medio.txt")
CS.compute_scores()
scores, times = CS.get_results()

scores['betweenness'].sort()
print("\nAPPROXIMATED VERSION:\n")
print("Best btw scores: ", scores['betweenness'][ len(scores['betweenness']) - 5 : len(scores['betweenness']) ] )
print("Execution time = ", times['betweenness'], " sec")

params = CS.get_params()
params['betweenness']['epsilon'] = 0.01
CS.set_params(params)
scores, times = CS.compute_scores()
scores['betweenness'].sort()
print("\nAPPROXIMATED VERSION WITH LOWER EPSILON:\n")
print("Best btw scores: ", scores['betweenness'][ len(scores['betweenness']) - 5 : len(scores['betweenness']) ] )
print("Execution time = ", times['betweenness'], " sec")

#All equivalent to modify a parameter

#CS.set_approx(False)   #All the algorithms are no longer approximated

#params = CS.get_params()
#params['betweenness']['approx'] = False
#CS.set_params(params)

CS.set_param_value('betweenness', 'approx', False)

scores, times = CS.compute_scores()
scores['betweenness'].sort()
print("\nEXACT VERSION:\n")
print("Best btw scores: ", scores['betweenness'][ len(scores['betweenness']) - 5 : len(scores['betweenness']) ] )
print("Execution time = ", times['betweenness'], " sec")

CS.export_scores("csv/btw_middle_graph.csv", "betweenness")


