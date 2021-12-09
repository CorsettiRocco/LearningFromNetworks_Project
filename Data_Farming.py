from Compute_Scores import Scores_Calculator

def find(element, element_list):
    for i in range(len(element_list)):
        if element_list[i] == element:
            return i
    return -1

def improved_nodes(best_nodes, best_sub_nodes):
    improved = []
    for i in range(len(best_sub_nodes)):
        pos = find(best_sub_nodes[i], best_nodes)
        if pos != -1 and i < pos:
            improved.append( (best_sub_nodes[i], pos - i) )
    return improved


#MAIN PIPELINE

#Input phase ( Insert different graphs )
graph_list = ["Test/Graphs/prova_grafo_piccolo.edges"]  #Add more here

#Computation
#I dind't know how to automatize the name choice =)
for g in graph_list:
    #Create a new object each time to avoid problems
    CS = Scores_Calculator()
    #Read the graph and compute the scores and the rank
    CS.read_text_graph(g) 
    CS.set_approx(False)    #To remove in the future, after the correction of voting_rule
    CS.compute_scores()
    res = CS.voting_rule(print_res = False)
    results = res.copy()    #To solve the copy problem
    
    #Delete the node
    subgraph = CS.delete_nodes()
   
    #Create a new class that takes the subgraph as input and redo calculations
    CS_sub = Scores_Calculator(graph = subgraph)
    CS_sub.set_approx(False)
    CS_sub.compute_scores()
    res = CS_sub.voting_rule(print_res = False)
    results_sub = res.copy()

    #Example of results printing
    print(list(results['borda_count'].keys()))
    print("\n",list(results_sub['borda_count'].keys()))

    #Check which nodes are the most influent after the elimination
    improved = improved_nodes( list(results['borda_count'].keys()), list(results_sub['borda_count'].keys()) )
    improved.sort(key = lambda imp_tuple: imp_tuple[1], reverse = True)
    #Print the improved nodes
    #print("Improved:\n", improved )
    for i in improved:
        print("Node ", i[0], " improved by ", i[1], " positions in the ranking")
    
