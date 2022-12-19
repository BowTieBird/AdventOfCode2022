from collections import deque

file = open("input.txt")

lines = [  line.split()  for line in ''.join(file.readlines()).split('\n') ]
valves = [ line[1] for line in lines ]
flowRates = { line[1]: int(line[4][5:-1]) for line in lines }
tunnels = { line[1]: [valve[:2] for valve in line[9:]] for line in lines }


for v in valves:
    for w in valves:
        assert (w in tunnels[v]) == (v in tunnels[w])

d = {}
for valve in valves:
    # Breadth first search to get distance to/from each node.
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

def runFrom(pos, t, turned_on, pressure):
    # print(f"Call:   pos: {pos}    t: {t}    turned_on: {turned_on}    pressure {pressure}")
    global T
    next_possibilities = [next_pos for next_pos, tn in turned_on.items() if not tn and t + d[pos][next_pos] + 1 <= T]

    return_path = pos
    max_next_pressure = 0
    for next_pos in next_possibilities:
        next_turned_on = { v:True if v == next_pos else tn for v, tn in turned_on.items() }
        next_t =  t + d[pos][next_pos] + 1
        next_pressure, next_return_path = runFrom(next_pos, next_t, next_turned_on, flowRates[next_pos]*(T-next_t))
        if next_pressure > max_next_pressure:
            max_next_pressure = next_pressure
            return_path = pos + next_return_path

    return pressure + max_next_pressure, return_path

def putOnPath(pos, target_pos, steps):
    for new_pos in valves:
        if d[pos][new_pos] == steps and steps + d[new_pos][target_pos] == d[pos][target_pos]:
            return new_pos
    assert False

# print(putOnPath('MV', 'XU', 1))

def runElephantFrom(you_pos, elephant_pos, t, turned_on, pressure):
    # print(f"Call:   pos: {pos}    t: {t}    turned_on: {turned_on}    pressure {pressure}")
    global T
    you_next_possibilities = [next_pos for next_pos, tn in turned_on.items() if not tn and t + d[you_pos][next_pos] + 1 <= T]
    elephant_next_possibilities = [next_pos for next_pos, tn in turned_on.items() if not tn and t + d[elephant_pos][next_pos] + 1 <= T]


    you_return_path = you_pos
    elephant_return_path = elephant_pos
    max_next_pressure = 0
    if len(you_next_possibilities) > 0 and len(elephant_next_possibilities) > 0:
        for you_next_pos in you_next_possibilities:
            for elephant_next_pos in elephant_next_possibilities:
                if d[you_pos][you_next_pos] == d[elephant_pos][elephant_next_pos]:
                    next_t =  t + d[you_pos][you_next_pos] + 1
                    next_turned_on = { v:True if v == you_next_pos or v == elephant_next_pos else tn for v, tn in turned_on.items() }
                    next_pressure, next_you_path, next_elephant_path = runElephantFrom(you_next_pos, elephant_next_pos, next_t, next_turned_on, (flowRates[you_next_pos] + flowRates[elephant_next_pos] if you_next_pos != elephant_next_pos else flowRates[you_next_pos])*(T-next_t))
                elif d[you_pos][you_next_pos] < d[elephant_pos][elephant_next_pos]:
                    next_turned_on = { v:True if v == you_next_pos else tn for v, tn in turned_on.items() }
                    next_t =  t + d[you_pos][you_next_pos] + 1
                    # TODO: PLACE THE ELEPHANT ON THE WAY TO elephant_next_pos
                    elephant_half_pos = putOnPath(elephant_pos, elephant_next_pos, next_t - t)
                    next_pressure, next_you_path, next_elephant_path = runElephantFrom(you_next_pos, elephant_half_pos, next_t, next_turned_on, flowRates[you_next_pos]*(T-next_t))
                elif d[you_pos][you_next_pos] > d[elephant_pos][elephant_next_pos]:
                    next_turned_on = { v:True if v == elephant_next_pos else tn for v, tn in turned_on.items() }
                    next_t =  t + d[elephant_pos][elephant_next_pos] + 1
                    # TODO: PLACE YOU ON THE WAY TO elephant_next_pos
                    you_half_pos = putOnPath(you_pos, you_next_pos, next_t - t)
                    next_pressure, next_you_path, next_elephant_path = runElephantFrom(you_half_pos, elephant_next_pos, next_t, next_turned_on, flowRates[elephant_next_pos]*(T-next_t))
                else:
                    assert False
                    
                if next_pressure > max_next_pressure:
                    max_next_pressure = next_pressure
                    you_return_path = you_pos + next_you_path
                    elephant_return_path = elephant_pos + next_elephant_path
    else:
        if len(you_next_possibilities) > 0:
            for next_pos in you_next_possibilities:
                next_turned_on = { v:True if v == next_pos else tn for v, tn in turned_on.items() }
                next_t =  t + d[you_pos][next_pos] + 1
                next_pressure, next_you_path = runFrom(next_pos, next_t, next_turned_on, flowRates[next_pos]*(T-next_t))
                if next_pressure > max_next_pressure:
                    max_next_pressure = next_pressure
                    you_return_path = you_pos + next_you_path
        elif len(elephant_next_possibilities) > 0:
            for next_pos in elephant_next_possibilities:
                next_turned_on = { v:True if v == next_pos else tn for v, tn in turned_on.items() }
                next_t =  t + d[elephant_pos][next_pos] + 1
                next_pressure, next_elephant_path = runFrom(next_pos, next_t, next_turned_on, flowRates[next_pos]*(T-next_t))
                if next_pressure > max_next_pressure:
                    max_next_pressure = next_pressure
                    elephant_return_path = elephant_pos + next_elephant_path

    return pressure + max_next_pressure, you_return_path, elephant_return_path

T = 30
turned_on = { v:False for v, f in flowRates.items() if f > 0 }
print(runFrom('AA', 0, turned_on, 0))


T = 26 
turned_on = { v:False for v, f in flowRates.items() if f > 0 }
print(runElephantFrom('AA', 'AA', 0, turned_on, 0))


    

