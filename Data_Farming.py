from Compute_Scores import Scores_Calculator
import pandas as pd


#method for computing and saving scores differences
#diff: (sc0 - sc1)^2
def scores_diff(black_list,pre_elem_data,post_elem_data,name):

    #load dataframes from csv files
    pre_sc_df = pd.read_csv(pre_elem_data)
    post_sc_df = pd.read_csv(post_elem_data)

    #drop rows of black list
    pre_sc_df=pre_sc_df.drop(labels = [(int(x)) for x in black_list],axis=0)
    post_sc_df=post_sc_df.drop(labels = [(int(x)) for x in black_list],axis=0)

    cols = list(pre_sc_df.columns)

    scores_diff_df = pd.DataFrame(columns = cols)

    #column id 
    scores_diff_df['id'] = pre_sc_df['id']

    #score difference
    cols.remove('id')
    for i in cols:
        scores_diff_df[i] = (pre_sc_df[i] - post_sc_df[i])**2

    #save inside scores_diff folder
    scores_diff_df.to_csv('scores_diff/'+name,index = False)
    


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


#generate name from path
def generate_name(path):
    list_of_names = []
    n=len(path)-1
    for i in range(n,0,-1):
        if(path[i] == '.'):
            end = i
        if(path[i] == '/'):
            start = i + 1
            break

    name=path[start: end:]

    list_of_names.append('pre_elem_'+name)
    list_of_names.append('post_elem_'+name)
    list_of_names.append('diff_scores_'+name)

    return list_of_names


#MAIN PIPELINE

#Input phase ( Insert different graphs )
graph_list = ['Test/Graphs/prova_grafo_piccolo.edges']  #Add more here

#Computation
#I dind't know how to automatize the name choice =)
for g in graph_list:
    list_of_names = generate_name(g)
    #Create a new object each time to avoid problems
    CS = Scores_Calculator(name = list_of_names[0])
    #Read the graph and compute the scores and the rank
    CS.read_text_graph(g) 
    #CS.set_approx(False)    #To remove in the future, after the correction of voting_rule
    CS.compute_scores()
    res = CS.voting_rule(print_res = False)
    results = res.copy()    #To solve the copy problem
    
    #Delete the node
    subgraph = CS.delete_nodes()
   
    #Create a new class that takes the subgraph as input and redo calculations
    CS_sub = Scores_Calculator(graph = subgraph,name = list_of_names[1])
    #CS_sub.set_approx(False)
    CS_sub.compute_scores()
    res = CS_sub.voting_rule(print_res = False)
    results_sub = res.copy()

    #Compute scores difference
    scores_diff(CS.return_blacklist(),'csv/'+list_of_names[0]+'.csv','csv/'+list_of_names[1]+'.csv',list_of_names[2])

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
    