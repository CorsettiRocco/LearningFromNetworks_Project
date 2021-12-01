from Compute_Scores import Scores_Calculator

CS = Scores_Calculator(name='btw_small_graph')
CS.read_text_graph("Test/Graphs/prova_grafo_piccolo.edges")
CS.compute_scores()

scores, ranking, times = CS.get_results()

scores['betweenness'].sort()
scores['closeness'].sort()
print("\nAPPROXIMATED VERSION:\n")
print("Best btw scores: ", scores['betweenness'][ len(scores['betweenness']) - 5 : len(scores['betweenness']) ] )
print("Best cln scores: ", scores['closeness'][ len(scores['closeness']) - 5 : len(scores['closeness']) ] )
print("Best btw scores through ranking: ", ranking['betweenness'][:5])
print("Best cln scores through ranking: ", ranking['closeness'][:5])
print("BTW Execution time = ", times['betweenness'], " sec")
print("CLN Execution time = ", times['closeness'], " sec")


params = CS.get_params()
params['betweenness']['epsilon'] = 0.01
params['closeness']['epsilon'] = 0.01
CS.set_params(params)
scores, ranking, times = CS.compute_scores()
scores['betweenness'].sort()
scores['closeness'].sort()
print("\nAPPROXIMATED VERSION WITH LOWER EPSILON:\n")
print("Best btw scores: ", scores['betweenness'][ len(scores['betweenness']) - 5 : len(scores['betweenness']) ] )
print("Best cln scores: ", scores['closeness'][ len(scores['closeness']) - 5 : len(scores['closeness']) ] )
print("Best btw scores through ranking: ", ranking['betweenness'][:5])
print("Best cln scores through ranking: ", ranking['closeness'][:5])
print("BTW Execution time = ", times['betweenness'], " sec")
print("CLN Execution time = ", times['closeness'], " sec")

#All equivalent to modify a parameter

CS.set_approx(False)   #All the algorithms are no longer approximated

#params = CS.get_params()
#params['betweenness']['approx'] = False
#CS.set_params(params)

#CS.set_param_value('betweenness', 'approx', False)

scores, ranking, times = CS.compute_scores()
scores['betweenness'].sort()
scores['closeness'].sort()
print("\nEXACT VERSION:\n")
print("Best btw scores: ", scores['betweenness'][ len(scores['betweenness']) - 5 : len(scores['betweenness']) ] )
print("Best cln scores: ", scores['closeness'][ len(scores['closeness']) - 5 : len(scores['closeness']) ] )
print("Best btw scores through ranking: ", ranking['betweenness'][:5])
print("Best cln scores through ranking: ", ranking['closeness'][:5])
print("BTW Execution time = ", times['betweenness'], " sec")
print("CLN Execution time = ", times['closeness'], " sec")

CS.export_scores("csv/", "betweenness")
#test new column
CS.export_scores("csv/", "betweenness")
