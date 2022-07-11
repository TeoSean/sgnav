from collections import defaultdict
import csv
import sys

class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

rows = []
with open('mrt.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    for row in reader:
        rows.append(row)
        #print(row[3][:2], row[3][2:])

# for row in rows:
#     print(row[6])

reftab = {}
names = {}
names2id = {}
names2station = {}
for row in rows:
    lis = row[0]
    name = row[1]
    id_ = row[6]
    for station in lis.split(' '):
        reftab[station] = id_
    
    names[id_] = name
    names2id[name] = id_
    names2station[name]='/'.join(lis.split(' '))

# print(reftab)

gweights = []
graph = Graph()
graph2 = Graph()
CCnodes = [('CE2', 'CE1', 1), ('CE1', 'CC4', 1), ('CC1', 'CC2', 1), ('CC2', 'CC3', 1), ('CC3', 'CC4', 1), ('CC4', 'CC5', 1), ('CC5', 'CC6', 1), ('CC6', 'CC7', 1), ('CC7', 'CC8', 1), ('CC8', 'CC9', 1), ('CC9', 'CC10', 1), ('CC10', 'CC11', 1), ('CC11', 'CC12', 1), ('CC12', 'CC13', 1), ('CC13', 'CC14', 1), ('CC14', 'CC15', 1), ('CC15', 'CC16', 1), ('CC16', 'CC17', 1), ('CC17', 'CC19', 1), ('CC19', 'CC20', 1), ('CC20', 'CC21', 1), ('CC21', 'CC22', 1), ('CC22', 'CC23', 1), ('CC23', 'CC24', 1), ('CC24', 'CC25', 1), ('CC25', 'CC26', 1), ('CC26', 'CC27', 1), ('CC27', 'CC28', 1), ('CC28', 'CC29', 1)]
EWnodes = [('CG2', 'CG1', 1), ('CG1', 'CG', 1), ('EW1', 'EW2', 1), ('EW2', 'EW3', 1), ('EW3', 'EW4', 1), ('EW4', 'EW5', 1), ('EW5', 'EW6', 1), ('EW6', 'EW7', 1), ('EW7', 'EW8', 1), ('EW8', 'EW9', 1), ('EW9', 'EW10', 1), ('EW10', 'EW11', 1), ('EW11', 'EW12', 1), ('EW12', 'EW13', 1), ('EW13', 'EW14', 1), ('EW14', 'EW15', 1), ('EW15', 'EW16', 1), ('EW16', 'EW17', 1), ('EW17', 'EW18', 1), ('EW18', 'EW19', 1), ('EW19', 'EW20', 1), ('EW20', 'EW21', 1), ('EW21', 'EW22', 1), ('EW22', 'EW23', 1), ('EW23', 'EW24', 1), ('EW24', 'EW25', 1), ('EW25', 'EW26', 1), ('EW26', 'EW27', 1), ('EW27', 'EW28', 1), ('EW28', 'EW29', 1), ('EW29', 'EW30', 1), ('EW30', 'EW31', 1), ('EW31', 'EW32', 1), ('EW32', 'EW33', 1)]
NSnodes = [('NS1', 'NS2', 1), ('NS2', 'NS3', 1), ('NS3', 'NS4', 1), ('NS4', 'NS5', 1), ('NS5', 'NS6', 1), ('NS6', 'NS7', 1), ('NS7', 'NS8', 1), ('NS8', 'NS9', 1), ('NS9', 'NS10', 1), ('NS10', 'NS11', 1), ('NS11', 'NS12', 1), ('NS12', 'NS13', 1), ('NS13', 'NS14', 1), ('NS14', 'NS15', 1), ('NS15', 'NS16', 1), ('NS16', 'NS17', 1), ('NS17', 'NS18', 1), ('NS18', 'NS19', 1), ('NS19', 'NS20', 1), ('NS20', 'NS21', 1), ('NS21', 'NS22', 1), ('NS22', 'NS23', 1), ('NS23', 'NS24', 1), ('NS24', 'NS25', 1), ('NS25', 'NS26', 1), ('NS26', 'NS27', 1), ('NS27', 'NS28', 1)]
DTnodes = [('DT1', 'DT2', 1), ('DT2', 'DT3', 1), ('DT3', 'DT5', 1), ('DT5', 'DT6', 1), ('DT6', 'DT7', 1), ('DT7', 'DT8', 1), ('DT8', 'DT9', 1), ('DT9', 'DT10', 1), ('DT10', 'DT11', 1), ('DT11', 'DT12', 1), ('DT12', 'DT13', 1), ('DT13', 'DT14', 1), ('DT14', 'DT15', 1), ('DT15', 'DT16', 1), ('DT16', 'DT17', 1), ('DT17', 'DT18', 1), ('DT18', 'DT19', 1), ('DT19', 'DT20', 1), ('DT20', 'DT21', 1), ('DT21', 'DT22', 1), ('DT22', 'DT23', 1), ('DT23', 'DT24', 1), ('DT24', 'DT25', 1), ('DT25', 'DT26', 1), ('DT26', 'DT27', 1), ('DT27', 'DT28', 1), ('DT28', 'DT29', 1), ('DT29', 'DT30', 1), ('DT30', 'DT31', 1), ('DT31', 'DT32', 1), ('DT32', 'DT33', 1), ('DT33', 'DT34', 1), ('DT34', 'DT35', 1)]
NEnodes = [('NE1', 'NE3', 1), ('NE3', 'NE4', 1), ('NE4', 'NE5', 1), ('NE5', 'NE6', 1), ('NE6', 'NE7', 1), ('NE7', 'NE8', 1), ('NE8', 'NE9', 1), ('NE9', 'NE10', 1), ('NE10', 'NE11', 1), ('NE11', 'NE12', 1), ('NE12', 'NE13', 1), ('NE13', 'NE14', 1), ('NE14', 'NE15', 1), ('NE15', 'NE16', 1), ('NE16', 'NE17', 1)]
TEnodes = [('TE1', 'TE2', 1), ('TE2', 'TE3', 1), ('TE3', 'TE4', 1), ('TE4', 'TE5', 1), ('TE5', 'TE6', 1), ('TE6', 'TE7', 1), ('TE7', 'TE8', 1), ('TE8', 'TE9', 1)]

for node in CCnodes+EWnodes+NSnodes+DTnodes+NEnodes+TEnodes:
    graph.add_edge(*(reftab[node[0]], reftab[node[1]], node[2]))
    graph2.add_edge(*node)
rt = []
rt2 = []
from_ = input('From which station: ')
to = input('To which station: ')
r1 = dijsktra(graph, names2id[from_], names2id[to])


for i in r1:
    rt.append(names[i]+' '+names2station[names[i]])


print(' > '.join(rt))