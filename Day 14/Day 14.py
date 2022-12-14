file = open("input.txt")

VERBOSE = True # False

structures = [ [ [ int(x) for x in vertex.split(',') ] for vertex in structure.split(" -> ") ] for structure in ''.join(file.readlines()).split('\n') ]

minX = min([vertex[0] for structure in structures for vertex in structure])
maxX = max([vertex[0] for structure in structures for vertex in structure])
maxY = max([vertex[1] for structure in structures for vertex in structure])

# Add floor
structures.append([[500 -maxY - 4, maxY + 2], [500 +maxY + 4, maxY + 2]])
minX = min([vertex[0] for structure in structures for vertex in structure])
maxX = max([vertex[0] for structure in structures for vertex in structure])
maxY = max([vertex[1] for structure in structures for vertex in structure])

initialGrid = [[False for _ in range(minX, maxX+1)] for _ in range(0, maxY+1)]
leftGrains = [[False for _ in range(0, maxY+1)]]
rightGrains = [[False for _ in range(0, maxY+1)]]

for structure in structures:
    startVertex = structure[0]
    for vertex in structure[1:]:
        x1 = vertex[0] - minX
        x2 = startVertex[0] - minX
        y1 = vertex[1]
        y2 = startVertex[1]
        if x1 == x2:
            if y1 > y2:
                for y in range(y2, y1+1):
                    initialGrid[y][x1] = True
            elif y1 < y2:
                for y in range(y1, y2+1):
                    initialGrid[y][x1] = True
            else:
                assert False
        elif y1 == y2:
            if x1 > x2:
                for x in range(x2, x1+1):
                    initialGrid[y1][x] = True
            elif x1 < x2:
                for x in range(x1, x2+1):
                    initialGrid[y1][x] = True
            else:
                assert False
        else:
            assert False
        startVertex = vertex

grid = [[x for x in row] for row in initialGrid]

def printGrid():
    for y in range(0, maxY+1):
        for x in range(0, maxX-minX+1):
            print(f'{"#" if initialGrid[y][x] else "o" if grid[y][x] else "."}', end='')
        print('')

if (VERBOSE):
    printGrid()
    print(" ")

grains = 0
def dropGrain():
    # returns whether the grain fell forever
    pos = [500 - minX, 0]
    while True:
        pos[1] += 1
        if pos[1] > maxY:
            return True, "Reached maxY"
        elif not grid[pos[1]][pos[0]]:
            continue
        else:
            pos[0] -= 1
            if pos[0] < 0:
                # Attempt to calculate efficiently
                # if not leftGrains[pos[1]]:
                #     addToCount = (pos[1] * (pos[1] + 1)) / 2
                #     print(addToCount)
                #     grains += addToCount
                #     leftGrains[pos[1]] = True
                # else:
                #     addToCount = (pos[1] * (pos[1] + 1)) / 2
                #     print(addToCount)
                #     grains += addToCount
                #     leftGrains[pos[1]] = True
                return True, "Reached minX"
            elif not grid[pos[1]][pos[0]]:
                continue
            else:
                pos[0] += 2
                if pos[0] >= maxX - minX + 1:
                    return True, "Reached maxX"
                elif not grid[pos[1]][pos[0]]:
                    continue
                else:
                    pos[0] -= 1
                    pos[1] -= 1
                    grid[pos[1]][pos[0]] = True
                    return False, pos

# while True:
#     reachedBottom = dropGrain()
#     if reachedBottom[0] == True:
#         printGrid()
#         print(reachedBottom[1])
#         print(grains)
#         break
#     grains += 1

while not grid[0][500 - minX]:
    reachedBottom = dropGrain()
    grains += 1

if (VERBOSE): printGrid()
print(grains)




