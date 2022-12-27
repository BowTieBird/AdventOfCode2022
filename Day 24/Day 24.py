from typing import Dict, List

file = open("input.txt")

lines = ''.join(file.readlines()).split('\n')

blizzards: Dict[tuple,List[str]] = {}
max_x, max_y = len(lines[0]), len(lines)
for y in range(1,max_y-1):
    for x in range(1,max_x-1):
        if lines[y][x] != '.':
            blizzards[(x,y)] = [lines[y][x]]

print(blizzards)

def outOfBounds(x,y):
    return (x <= 0 or x >= max_x-1 or y <= 0 or y >= max_y-1) and (x,y) not in [(1,0), (max_x-2, max_y-1)]

def printGrid(pos, blizzards):
    print(pos)
    for y in range(max_y):
        for x in range(max_x):
            char = '#' if outOfBounds(x,y) else '.'
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

directions = [(1,0), (0, 1), (0,0), (0, -1), (-1, 0)]
arrows = ['>', 'v', '.', '^', '<']

def doExpedition(pos, blizzards, steps=0, min_steps_left=None):
    # print(steps)
    # printGrid(pos, blizzards)
    # input()

    # If in bottom right corner, done!
    if pos == (max_x-2, max_y-2):
        print(f"Done in {steps + 1}")
        return steps + 1
    # If exceeded a previously found minimum, done.
    if min_steps_left is not None and steps+1 > min_steps_left:
        return min_steps_left

    # Move blizzards
    new_blizzards = {}
    for square, arrow_set in blizzards.items():
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

    # Check for moves
    for direction in directions:
        x, y = [a+b for a,b in zip(pos, direction)]
        if not outOfBounds(x,y) and (x, y) not in new_blizzards.keys():
            # print(f"Moving in direction: {arrows[directions.index(direction)]}")
            min_steps_left = doExpedition((x,y), new_blizzards, steps=steps+1, min_steps_left=min_steps_left)   
    return min_steps_left

print(doExpedition(pos=(1, 0), blizzards=blizzards))