import re

file = open("input.txt")

lines = ''.join(file.readlines()).split('\n')

directions = [[[0, -1], [1, -1], [-1, -1]], [[0, 1], [1, 1], [-1, 1]], [[-1, 0], [-1, 1], [-1, -1]], [[1, 0], [1, 1], [1, -1]]]
start_dir_index = 0

elves = {}
for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] == '#':
            elves[(x,y)] = None
# grid = [ [line[x] if x < len(line) else ' ' for x in range(len(line)+1)] for line in lines]

def printElves(elves):
    min_x = min([elf[0] for elf in elves.keys()])
    max_x = max([elf[0] for elf in elves.keys()])
    min_y = min([elf[1] for elf in elves.keys()])
    max_y = max([elf[1] for elf in elves.keys()])
    count = 0
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            count += 0 if (x,y) in elves.keys() else 1
            print('#' if (x,y) in elves.keys() else '.', end = '')
        print()
    print()
    return count
# printElves(elves)

elfMoved = True
round = 0
# for _ in range(10):
while elfMoved:
    elfMoved = False
    round += 1

    # Consider moves
    for elf in elves.keys():
        elves[elf] = None
        canMove = False
        # Check all other spaces for elves
        for offset_y in [-1, 0, 1]:
            for offset_x in [-1, 0, 1]:
                if offset_x != 0 or offset_y != 0:
                    if (elf[0] + offset_x, elf[1] + offset_y) in elves.keys():
                        canMove = True
                        break
        # print(f"{elf}: {canMove}")
        if not canMove:
            continue
        
        # Propose direction        
        for dir_index in range(start_dir_index, start_dir_index+4):
            direction = directions[dir_index % 4]
            canMove = True
            for offset in direction:
                space = tuple(a+b for a,b in zip(elf, offset))
                if space in elves.keys():
                    canMove = False
                    break
            if canMove:
                offset = directions[dir_index % 4][0]
                elves[elf] = tuple(a+b for a,b in zip(elf, offset))
                break
    
    # Attempt Moves
    newElves = {}
    for elf in elves:
        if elves[elf] != None:
            willMove = True
            for other_elf in elves:
                if elf != other_elf and elves[elf] == elves[other_elf]:
                    willMove = False
                    break
            # print(f"{elf}: {elves[elf]}, {willMove}")
            if willMove:
                elfMoved = True
                space = elves[elf]
                newElves[space] = None
            else:
                newElves[elf] = None
        else:
            newElves[elf] = None
    elves = newElves
    start_dir_index = (start_dir_index + 1) % 4

print(printElves(elves))
print(round)


