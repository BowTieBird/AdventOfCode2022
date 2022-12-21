from collections import deque

file = open("input.txt")

lines = [  line.split()  for line in ''.join(file.readlines()).split('\n') ]
valves = [ line[1] for line in lines ]
flowRates = { line[1]: int(line[4][5:-1]) for line in lines }
tunnels = { line[1]: [valve[:2] for valve in line[9:]] for line in lines }

# Check symmetric graph
for v in valves:
    for w in valves:
        assert (w in tunnels[v]) == (v in tunnels[w])

# Breadth first search to get distance to/from each node
d = {}
for valve in valves:
    d[valve] = {valve:0}
    remaining = [ valve ]
    visited = [ valve ]
    while len(remaining) > 0:
        vert = remaining.pop(0)
        for neighbour in tunnels[vert]:
            if neighbour not in visited:
                d[valve][neighbour] = d[valve][vert] + 1
                visited.append(neighbour)
                remaining.append(neighbour)
            else:
                assert d[valve][neighbour] <= d[valve][vert] + 1

for v in valves:
    for w in valves:
        assert d[v][w] == d[w][v]

def getPaths(pos, t, turned_on):
    """Run a single person simulation from node pos with time t REMAINING."""
    # print(f"Call:   pos: {pos}    t: {t}    turned_on: {turned_on}")
    next_possibilities = [next_pos for next_pos, tn in turned_on.items() if not tn and t - d[pos][next_pos] - 1 > 0] + [None]

    return_paths = [[0, [pos]]]
    for next_pos in next_possibilities:
        if next_pos is None:
            continue
        next_turned_on = { v:True if v == next_pos else tn for v, tn in turned_on.items() }
        next_t =  t - d[pos][next_pos] - 1
        next_paths = getPaths(next_pos, next_t, next_turned_on)
        for path in next_paths:
            path[0] += flowRates[next_pos]*next_t
            path[1] = [pos] + path[1]
        return_paths.extend(next_paths)

    return return_paths

turned_on = { v:False for v, f in flowRates.items() if f > 0 }
print(max([path[0] for path in getPaths('AA', 30, turned_on)]))

turned_on = { v:False for v, f in flowRates.items() if f > 0 }
paths = getPaths('AA', 26, turned_on)
one_person_max = max([path[0] for path in paths])
print(max([path[0] + elephant_path[0] for path in paths for elephant_path in paths if path[0] + elephant_path[0] >= one_person_max and len(set.intersection(set(path[1]), set(elephant_path[1]))) == 1])) # 1 for 'AA'
