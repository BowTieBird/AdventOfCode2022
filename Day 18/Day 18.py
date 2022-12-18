import functools
from math import floor

file = open("input.txt")
rocks_file = open("rocks.txt")

rocks = [ rock.split('\n') for rock in ''.join(rocks_file.readlines()).split('\n\n')]
rock_index = 0

jets = file.readlines()[0]
jet_index = 0

chamber_width = 7

chamber = [[False for _ in range(chamber_width)] for _ in range(1000000)] # y from bottom, x from left

def getLeftRightCollision(rock, dir):
    collision = []
    for i in range(len(rock)):
        for j in range(len(rock[i])):
            ind = j if dir < 0 else len(rock[i])-1 - j
            if rock[i][ind] == '#':
                collision.append(ind)
                break
    return collision

def getDownCollision(rock):
    collision = []
    for j in range(len(rock[0])):
        for i in range(len(rock)): # from bottom
            ind = len(rock) -1 - i
            if rock[ind][j] == '#':
                collision.append(ind)
                break
    return collision

# print(getLeftRightCollision(rocks[1], -1))
# print(getDownCollision(rocks[1]))

def checkMoveLeftRight(rock, rock_left, rock_bottom, dir):
    if (rock_left <= 0 and dir == -1)  or (rock_left + len(rock[0]) >= chamber_width and dir == +1):
        return False
    collision = getLeftRightCollision(rock, dir)
    for i in range(len(rock)):
        x = rock_left + collision[i] + dir
        y = rock_bottom + len(rock) - i - 1
        if chamber[y][x]:
            # print("collision:", x, y)
            return False
    return True

def checkMoveDown(rock, rock_left, rock_bottom):
    if rock_bottom-1 < 0:
        return False
    collision = getDownCollision(rock)
    for j in range(len(rock[0])):
        x = rock_left + j
        y = (rock_bottom + len(rock) - collision[j] - 1)  - 1
        if chamber[y][x]:
            # print("collision:", x, y)
            return False
    return True

# for x in range(chamber_width//2):
#     chamber[0][2*x] = True
# print(checkMoveDown(rocks[3], 1, 1))
# print(checkMoveLeftRight(rocks[0], 3, 0, -1))

def printChamber(height):
    for y in range(height, height-10,-1):
        for x in range(chamber_width):
            print('#' if chamber[y][x] else '.', end = '')
        print()
    print()

def dropRock(rock, rock_left, rock_bottom):
    global jet_index    
    while True: # Drop rock
        # Move left/right
        jet = jets[jet_index]
        jet_index += 1
        if jet_index >= len(jets): jet_index = 0
        dir = +1 if jet == '>' else -1 # Right
        if checkMoveLeftRight(rock, rock_left, rock_bottom, dir):
            # print(f"moving in dir {dir}")
            rock_left += dir
        else:
            # print(f"Not moving {dir}")
            pass
        if checkMoveDown(rock, rock_left, rock_bottom):
            rock_bottom-=1
        else:
            # print(f"rock {rock_index-1} settled at ", rock_left, rock_bottom)
            for i in range(len(rock)):
                for j in range(len(rock[i])):
                    if rock[i][j] == '#':
                        chamber[rock_bottom + len(rock) - 1 - i][rock_left + j] = True
            break

# print(dropBlock(2022)) # Part 1
height = 0
rocks_dropped = 0

jet_indices = [0]
heights = [0]
counter = 0
while True:
    for rock in rocks:
        while True: # Find empty row
            if not any(chamber[height]):
                break
            height += 1
        rock_left = 2
        rock_bottom = height + 3

        dropRock(rock, rock_left, rock_bottom)

        while True: # Find empty row
            if not any(chamber[height]):
                break
            height += 1
        heights.append(height)

        rocks_dropped += 1

    if jet_index in jet_indices:
        print("found!")
        print(jets[jet_index:jet_index+5])
        printChamber(height-1)
        offset = jet_indices.index(jet_index)
        counter += 1
        if counter >= 4: # Chosen so that the `restart` of the block is the same as the first time around
            break
    else:
        jet_indices.append(jet_index)

last_jet_index = jet_index
rocks_offset = offset * len(rocks)
height_offset =  heights[rocks_offset]

total_rocks = 1000000000000
block_size = rocks_dropped - rocks_offset
block_height = height - height_offset

num_blocks = (total_rocks - rocks_offset) // block_size
remainder = (total_rocks - rocks_offset) - num_blocks * block_size 

print(rocks_dropped, offset, rocks_offset, block_size, block_height, num_blocks, remainder)
assert num_blocks * block_size + remainder + rocks_offset == 1000000000000

remainder_height = heights[rocks_offset + remainder] - height_offset # height - current_height
print(height_offset + block_height * num_blocks + remainder_height)

    