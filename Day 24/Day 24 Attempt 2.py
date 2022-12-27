from typing import Dict, List
from math import lcm

file = open("input.txt")
directions = [(1,0), (0, 1), (0,0), (0, -1), (-1, 0)]
arrows = ['>', 'v', '.', '^', '<']

lines = ''.join(file.readlines()).split('\n')

max_x, max_y = len(lines[0]), len(lines)
max_t = lcm(max_x-2, max_y-2)
blizzards_at_time: List[Dict[tuple,List[str]]] = []

def outOfBounds(x,y):
    return (x <= 0 or x >= max_x-1 or y <= 0 or y >= max_y-1) and (x,y) not in [(1,0), (max_x-2, max_y-1)]

def printGrid(pos, blizzards):
    print(pos)
    for y in range(max_y):
        for x in range(max_x):
            char = '#' if outOfBounds(x,y)  else '.'
            if (x,y) in blizzards.keys():
                if len(blizzards[(x,y)]) > 1:
                    char = len(blizzards[(x,y)])
                else:
                    char = blizzards[(x,y)][0]
            if pos == (x,y):
                char = 'E'
                assert (x,y) not in blizzards.keys()
            print(char, end = '')
        print()
    print()

# Compute blizzard positions beforehand
initial_blizzards: Dict[tuple,List[str]] = {}
for y in range(1,max_y-1):
    for x in range(1,max_x-1):
        if lines[y][x] != '.':
            initial_blizzards[(x,y)] = [lines[y][x]]
blizzards_at_time.append(initial_blizzards)


for i in range(1,max_t):
    # Move blizzards
    print (f"Generating blizzards {i+1}/{max_t}", end = '\r')
    new_blizzards = {}
    for square, arrow_set in initial_blizzards.items():
        for arrow in arrow_set:
            ind = arrows.index(arrow)
            direction = directions[ind]
            x, y = [a+b for a,b in zip(square, direction)]
            if x == 0: x = max_x - 2
            if x == max_x-1: x = 1
            if y == 0: y = max_y - 2
            if y == max_y-1: y = 1
            if (x,y) in new_blizzards.keys():
                new_blizzards[(x,y)].append(arrow)
            else:
                new_blizzards[(x,y)] = [arrow]
    initial_blizzards = new_blizzards
    blizzards_at_time.append(new_blizzards)
assert max_t == len(blizzards_at_time)
print()

steps = { (x,y,t,z): 0 if (x,y,t,z) == (1,0,0,0) else -1 for x in range(max_x) for y in range(max_y) for t in range(max_t) if not outOfBounds(x,y) for z in range(3) }
prev = { (x,y,t,z): (x,y, t-1,z) if (x,y) == (1,0) and t > 0 else None for x in range(max_x) for y in range(max_y) for t in range(max_t) if not outOfBounds(x,y) for z in range(3) }

result = None
queue = []
queue.append((1, 0, 0, 0))

# Dijkstra
while len(queue) > 0:
    # Find minimum
    queue = list(sorted(queue, key = lambda v: steps[v]))
    min_Q = queue.pop(0)

    q_x, q_y, q_t, q_z = min_Q
    t = (q_t + 1) % max_t
    z = q_z
    if (q_x, q_y) == (max_x-2, max_y-1):
        if q_z == 2:
            result = steps[q_x, q_y, q_t, q_z]
            print(result)
            break
        elif q_z == 0:
            z = 1
    elif (q_x, q_y) == (1, 0):
        if q_z == 1:
            z = 2
    new_steps = steps[q_x,q_y,q_t,q_z] + 1

    # Check for moves
    # printGrid((q_x, q_y), blizzards_at_time[q_t])
    for direction in directions:
        x, y = q_x + direction[0], q_y + direction[1]
        if not outOfBounds(x,y) and (x,y) not in blizzards_at_time[t].keys():
            if (new_steps < steps[x,y,t,z] or steps[x,y,t,z] == -1):
                steps[x,y,t,z] = new_steps
                prev[x,y,t,z] = min_Q
                queue.append((x,y,t,z))

# Retrieve path:
assert result is not None
x, y, t, z = max_x-2, max_y-1, result % max_t, 2
prev[x,y,t,z] = (max_x-2, max_y-2, t-1, 2)
path = ''
while (x,y,t,z) != (1, 0, 0, 0):
    # print(steps[x,y,t])
    # printGrid((x,y), blizzards_at_time[t])
    # input()
    prev_square = prev[x,y,t,z][:2]
    direction = tuple(a-b for a,b in zip((x,y), prev_square))
    path = arrows[directions.index(direction)] + path
    x,y,t,_z = prev[x,y,t,z]
    if _z != z: path = '\n' + path
    z = _z
print(path)
