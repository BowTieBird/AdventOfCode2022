file = open("input.txt")
import re

lines = ''.join(file.readlines()).split('\n')

maxlen = max([len(line) for line in lines[:-2]])+1 # Include a row / column of ' ' for ease
grid = [ [line[x] if x < len(line) else ' ' for x in range(maxlen)] for line in lines[:-1]]
instructions_line = lines[-1]

# print(instructions)
# regexp = re.compile(r'(\d*)([A-Z]\d*)+')
# instructions = regexp.search(instructions)

i = 0
dir_instructions = []
steps_instructions = []
for j in range(len(instructions_line)):
    if not instructions_line[i: j+1].isdigit():
        steps_instructions.append(int(instructions_line[i: j]))
        dir_instructions.append(instructions_line[j])
        i = j+1
steps_instructions.append(int(instructions_line[i:j+1])) 

def printGrid():
    for line in grid:
        print(''.join(line))

pos = [grid[0].index('.'), 0] # Leftmost top
directions = [[1,0], [0, 1], [-1, 0], [0, -1]]
arrows = ['>', 'v', '<', '^']
ind = 0 # Right
direction = [1, 0] # Right


def searchRight(y):
    for _x in range(len(grid[y])):
        if grid[y][_x] != ' ':
            return _x,  [1, 0]
    assert False

def searchLeft(y):
    for _x in range(len(grid[y])-1, 0, -1):
        if grid[y][_x] != ' ':
            return _x , [-1, 0]
    assert False

def searchDown(x):
    for _y in range(len(grid)):
        if grid[_y][x] != ' ':
            return _y,  [0, 1]
    assert False

def searchUp(x):
    for _y in range(len(grid)-1, 0, -1):
        if grid[_y][x] != ' ':
            return _y, [0, -1]
    assert False

for instr_index in range(len(steps_instructions)):
    # Move steps
    steps = steps_instructions[instr_index]
    for _ in range(steps):
        ind = directions.index(direction)
        grid[pos[1]][pos[0]] = arrows[ind]  

        x, y = [a+b for a,b in zip(pos, direction)]
        new_direction = None
        if grid[y][x] == ' ':
            if direction == [1, 0]:
                # 1
                if 0 <= y < 50 or 100 <= y < 150: 
                    y = 150 - y - 1
                    x, new_direction = searchLeft(y) 
                # 2
                elif 50 <= y < 100:
                    x = 100 + (y-50)
                    y, new_direction = searchUp(x)
                # 3
                elif 150 <= y < 200:
                    x = 50 + (y-150)
                    y, new_direction = searchUp(x)
            elif direction == [-1, 0]:
                # 4
                if 0 <= y < 50 or 100 <= y < 150:
                    y = 150 - y -1
                    x, new_direction = searchRight(y)
                # 5
                elif 50 <= y < 100:
                    x = y - 50
                    y, new_direction = searchDown(x)
                # 6
                elif 150 <= y < 200:
                    x = 50 + (y - 150)
                    y, new_direction = searchDown(x)
            elif direction == [0, 1]:
                # 7
                if 0 <= x < 50:
                    x = 100 + x
                    y, new_direction = searchDown(x)   
                # 3
                elif 50 <= x < 100:
                    y = 150 + (x-50)
                    x, new_direction = searchLeft(y)
                # 2
                elif 100 <= x < 150:
                    y = 50 + (x-100)
                    x, new_direction = searchLeft(y) 
            elif direction == [0, -1]:
                # 5
                if 0 <= x < 50:
                    y = 50 + x
                    x, new_direction = searchRight(y)
                # 6
                elif 50 <= x < 100:
                    y = 150 + (x-50)
                    x, new_direction = searchRight(y)
                # 7
                elif 100 <= x < 150:
                    x = x - 100
                    y, new_direction = searchUp(x)           
            assert new_direction is not None

            # Uncomment for part 1
            # if direction == [1, 0]:
            #     x, new_direction = searchRight(y)
            # elif direction == [-1, 0]:
            #     x, new_direction = searchLeft(y)
            # elif direction == [0, 1]:
            #     y, new_direction = searchDown(x)
            # elif direction == [0, -1]:
            #     y, new_direction = searchUp(x)
        if grid[y][x] == '#':
            break
        if new_direction is not None:
            direction = new_direction                 
        pos = [x, y]
    
    # Change direction
    if instr_index == len(steps_instructions)-1:
        continue
    ind = directions.index(direction)
    if dir_instructions[instr_index] == 'R':
        direction = directions[(ind + 4 + 1) % 4]
    elif dir_instructions[instr_index] == 'L':
        direction = directions[(ind + 4 - 1) % 4]
    else:
        assert False
    # printGrid()
    # input()

grid[pos[1]][pos[0]] = '@'   
printGrid()
print(1000 * (1+pos[1]) + 4 * (1+pos[0]) + directions.index(direction)) #103134


