from lib2to3.pytree import Node
from Compute_Scores import Scores_Calculator
import os
import sys
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

    list_of_names.append('voting_results/votes_pre_elem_'+name+'.csv')
    list_of_names.append('pre_elem_'+name)
    list_of_names.append('post_elem_'+name)
    list_of_names.append('diff_scores_'+name)
    list_of_names.append('voting_results/votes_post_elem_'+name+'.csv')

    return list_of_names

def voting_results(file, voting_rule = "borda_count"):
    df = pd.read_csv(file)
    return df.iloc[:,0].tolist()


#Take the inputs
if len(sys.argv) < 2:
    print("Usage: python3 Data_Farming_2.py graph_path")
    quit()

#Compute the first set of scores
cmd = "python3 Remove_and_Scores.py "
cmd += sys.argv[1]
os.system(cmd)

#Compute the second set of scores
list_of_names = generate_name(sys.argv[1])
df = pd.read_csv(list_of_names[0])
node_to_remove = df.iat[0,0]
cmd = "python3 Remove_and_Scores.py "
cmd += sys.argv[1] + " "
cmd += str(node_to_remove)
os.system(cmd)

#Check for improvements
scores_diff([node_to_remove], 'csv/'+list_of_names[1]+'.csv','csv/'+list_of_names[2]+'.csv',list_of_names[3])
improved = improved_nodes(voting_results(list_of_names[0]), voting_results(list_of_names[4]))
improved.sort(key = lambda imp_tuple: imp_tuple[1], reverse = True)
for i in improved:
        print("Node ", i[0], " improved by ", i[1], " positions in the ranking")
