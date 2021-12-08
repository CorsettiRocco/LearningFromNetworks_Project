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
    CS = Scores_Calculator()
    CS.read_text_graph(g) 
    CS.set_approx(False)    #To remove in the future, after the correction of voting_rule
    CS.compute_scores()
    results = CS.voting_rule(print_res = False)
    print(list(results['borda_count'].keys()))
    
    subgraph = CS.delete_nodes()
    
    CS_sub = Scores_Calculator(graph = subgraph)
    CS_sub.set_approx(False)
    CS_sub.compute_scores()
    results_sub = CS_sub.voting_rule(print_res = False)
    print("\n",list(results_sub['borda_count'].keys()))

    print("Improved:\n", improved_nodes( list(results['borda_count'].keys()), list(results_sub['borda_count'].keys()) ) )
