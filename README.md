# LearningFromNetworks_Project
To use the code in this repository the istallation of NetworKit is needed (https://networkit.github.io/)

The main class is: Compute_Scores.py

The program Data_Farming.py was created to compute the scores of a list of networks automatically, to use this file the name of the graphs must be insert programmatically. (This code has some strange behaviour given, probably, by the Python interpreter)

To avoid the strange behaviour of Python, we created a second program, Data_Farming_2.py, that, instead of using the class multiple times in the same program, uses the system calls to execute the class multiple times, but in different programs. In this way the code works fine.

To execute the code: python3 Data_Farming_2.py path_of_the_graph_to_analyze [optional: number_of_nodes_to_remove]


The folder in the repository contain the results of the experiments that are in the report.
(Some results are not here, but in a Goolge Drive folder due to the size of the files, link for the folder: https://drive.google.com/drive/folders/1nbg7jnt91s0jDSFb33dmOhcn8zGJlWxR?usp=sharing )
