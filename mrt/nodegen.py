import sys

nodes = []

for i in range(1, int(sys.argv[1])):
    nodes.append((f'{sys.argv[2]}{i}', f'{sys.argv[2]}{i+1}', 1))

print(nodes)