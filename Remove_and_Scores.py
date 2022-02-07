from Compute_Scores import Scores_Calculator
import sys

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

    return list_of_names


#Read the graph path
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: python3 Remove_and_Scores.py graph_path [optional: node_to_remove]")
    quit()

graph_path = sys.argv[1]
list_of_names = generate_name(graph_path)
if len(sys.argv) == 3:
    node_to_remove = [sys.argv[2]]
    graph_name = list_of_names[1]
else:
    graph_name = list_of_names[0]
    

#Create the class, read the file and remove the node
CS = Scores_Calculator(name = graph_name)
CS.read_text_graph(graph_path)
if len(sys.argv) == 3:
    CS.delete_nodes(substitute = True, blacklist = node_to_remove)

#Compute Scores
CS.compute_scores(print_log = True)

#Apply voting rule
CS.voting_rule(print_res = True)


