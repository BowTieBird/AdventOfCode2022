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

def runFrom(pos, t, turned_on):
    """Run a single person simulation from node pos with time t REMAINING."""
    # print(f"Call:   pos: {pos}    t: {t}    turned_on: {turned_on}")
    next_possibilities = [next_pos for next_pos, tn in turned_on.items() if not tn and t - d[pos][next_pos] - 1 >= 0]

    return_path = [pos]
    max_next_pressure = 0
    for next_pos in next_possibilities:
        next_turned_on = { v:True if v == next_pos else tn for v, tn in turned_on.items() }
        next_t =  t - d[pos][next_pos] - 1
        next_pressure, next_return_path = runFrom(next_pos, next_t, next_turned_on)
        next_pressure += flowRates[next_pos]*next_t
        if next_pressure > max_next_pressure:
            max_next_pressure = next_pressure
            return_path = [pos] + next_return_path

    return max_next_pressure, return_path

def putOnPath(pos, target_pos, s):
    """Return the pos obtained from walking s steps from pos to target_pos"""
    for new_pos in valves:
        if d[pos][new_pos] == s and s + d[new_pos][target_pos] == d[pos][target_pos]:
            return new_pos
    assert False

def runElephantFrom(you_pos, elephant_pos, you_target, elephant_target, t, turned_on):
    """Run a person and elephant simulation from node pos with time t REMAINING.
    If you_target is provided, then the person must be travelling to you_target, and similarly for the elephant."""
    # print(f"Call:   pos: {pos}    t: {t}    turned_on: {turned_on}")

    # Possibility choosing
    if you_target is None:
        you_next_possibilities = [next_pos for next_pos, tn in turned_on.items() if not tn and t - d[you_pos][next_pos] - 1 >= 0 \
            and next_pos != elephant_target]
    else:
        you_next_possibilities = [you_target]

    if elephant_target is None:
        elephant_next_possibilities = [next_pos for next_pos, tn in turned_on.items() if not tn and t - d[elephant_pos][next_pos] - 1 >= 0 \
            and next_pos != you_target]
    else:
        elephant_next_possibilities = [elephant_target]


    you_return_path = [you_pos]
    elephant_return_path = [elephant_pos]
    max_next_pressure = 0
    if len(you_next_possibilities) > 0 and len(elephant_next_possibilities) > 0:
        for you_next_pos in you_next_possibilities:
            for elephant_next_pos in elephant_next_possibilities:
                if you_next_pos == elephant_next_pos:
                    # Need to fix this
                    # if len(you_next_possibilities) == len(elephant_next_possibilities) == 1:
                    #     pass
                    # else:
                    continue
                if d[you_pos][you_next_pos] == d[elephant_pos][elephant_next_pos]:
                    next_t =  t - d[you_pos][you_next_pos] - 1
                    next_turned_on = { v:True if v == you_next_pos or v == elephant_next_pos else tn for v, tn in turned_on.items() }
                    next_pressure, next_you_path, next_elephant_path = runElephantFrom(you_next_pos, elephant_next_pos, None, None, next_t, next_turned_on)
                    next_pressure += (flowRates[you_next_pos] + flowRates[elephant_next_pos] if you_next_pos != elephant_next_pos else flowRates[you_next_pos])*next_t
                elif d[you_pos][you_next_pos] < d[elephant_pos][elephant_next_pos]:
                    next_turned_on = { v:True if v == you_next_pos else tn for v, tn in turned_on.items() }
                    next_t =  t - d[you_pos][you_next_pos] - 1
                    # TODO: PLACE THE ELEPHANT ON THE WAY TO elephant_next_pos
                    elephant_half_pos = putOnPath(elephant_pos, elephant_next_pos, t - next_t)
                    next_pressure, next_you_path, next_elephant_path = runElephantFrom(you_next_pos, elephant_half_pos, None, elephant_next_pos, next_t, next_turned_on)
                    next_pressure += flowRates[you_next_pos]*next_t
                elif d[you_pos][you_next_pos] > d[elephant_pos][elephant_next_pos]:
                    next_turned_on = { v:True if v == elephant_next_pos else tn for v, tn in turned_on.items() }
                    next_t =  t - d[elephant_pos][elephant_next_pos] - 1
                    # TODO: PLACE YOU ON THE WAY TO elephant_next_pos
                    you_half_pos = putOnPath(you_pos, you_next_pos, t - next_t)
                    next_pressure, next_you_path, next_elephant_path = runElephantFrom(you_half_pos, elephant_next_pos, you_next_pos, None, next_t, next_turned_on)
                    next_pressure += flowRates[elephant_next_pos]*next_t
                else:
                    assert False

                if next_pressure > max_next_pressure:
                    max_next_pressure = next_pressure
                    # Something fishy going on
                    you_return_path = [you_pos] + next_you_path
                    elephant_return_path = [elephant_pos] + next_elephant_path
    else:
        if len(you_next_possibilities) > 0:
            for next_pos in you_next_possibilities:
                next_turned_on = { v:True if v == next_pos else tn for v, tn in turned_on.items() }
                next_t =  t - d[you_pos][next_pos] - 1
                next_pressure, next_you_path = runFrom(next_pos, next_t, next_turned_on)
                next_pressure += flowRates[next_pos]*next_t
                if next_pressure > max_next_pressure:
                    max_next_pressure = next_pressure
                    you_return_path = [you_pos] + next_you_path
        elif len(elephant_next_possibilities) > 0:
            for next_pos in elephant_next_possibilities:
                next_turned_on = { v:True if v == next_pos else tn for v, tn in turned_on.items() }
                next_t =  t - d[elephant_pos][next_pos] - 1
                next_pressure, next_elephant_path = runFrom(next_pos, next_t, next_turned_on)
                next_pressure += flowRates[next_pos]*next_t
                if next_pressure > max_next_pressure:
                    max_next_pressure = next_pressure
                    elephant_return_path = [elephant_pos] + next_elephant_path

    return max_next_pressure, you_return_path, elephant_return_path

turned_on = { v:False for v, f in flowRates.items() if f > 0 }
print(runFrom('AA', 30, turned_on))

turned_on = { v:False for v, f in flowRates.items() if f > 0 }
print(runElephantFrom('AA', 'AA', None, None, 26, turned_on))
