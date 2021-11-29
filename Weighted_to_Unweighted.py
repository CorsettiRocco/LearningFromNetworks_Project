
file = open("deter4.txt", "r")

line = "s"
params = []
edge_list = []

while line != "":
    line = file.readline()
    params = line.split(" ")
    if len(params) >= 2:
        edge_list.append(params[0] + " " + params[1])

file.close()

new_file = open("prova_grafo_medio.txt", "w")

for e in edge_list:
    new_file.write(e + "\n")

new_file.close()