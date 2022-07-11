import json
from collections import defaultdict

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

routedata = json.loads(open('/home/sawntoe/projects/sgnav/bus/routedata.json', 'r').read())
f_routedata = {}
for bus in routedata:
    route = routedata[bus]
    f_route = []
    for stop in route:
        try:
            name = stop.split(' - ')[1]
            name= name.split(' (')[0]
            f_route.append(name)
        except:
            f_route.append(stop)
    f_routedata[bus]=f_route

graph =  Graph()
stops = []
buses = {}
for bus in f_routedata:
    route = f_routedata[bus]
    for i in range(len(route)-1):
        graph.add_edge(*(route[i], route[i+1], 2))
    for i in route:
        stops.append(i)
        if not i in buses:
            buses[i] = []
        buses[i].append(bus)



from_ = input('From: ').lower()
to = input('To: ').lower()
for i in stops:
    if i.lower() == from_:
        from_=i
    if i.lower() == to:
        to=i

rt = dijsktra(graph, from_, to)

for i in range(len(rt)-1):
    buses_1 = buses[rt[i]]
    buses_2 = buses[rt[i+1]]
    similarities = []
    for n in buses_1:
        if n in buses_2:
            similarities.append(n)

    similarities = '/'.join(similarities)
    print(f'{rt[i]} {similarities} >', end=' ')

print(rt[-1:][0])
    