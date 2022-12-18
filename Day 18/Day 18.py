file = open("input.txt")

cubes = [ tuple(int(w) for w in cube.split(',')) for cube in ''.join(file.readlines()).split('\n')]

sortedCubes = sorted(cubes)
minima = [min([cube[i] for cube in sortedCubes]) for i in range(len(sortedCubes[0]))]
maxima = [max([cube[i] for cube in sortedCubes]) for i in range(len(sortedCubes[0]))]
# print(sortedCubes)

def nextTo(w,z):
    return sum([abs(a-b) for a,b in zip(w,z)]) == 1
def vecAdd(w,z):
    return tuple(a+b for a,b in zip(w,z))

# Part 1
surfaceArea = 6 * len(sortedCubes)
for i in range(len(sortedCubes)):
    for j in range(i, len(sortedCubes)):
        if nextTo(sortedCubes[i], sortedCubes[j]):
            surfaceArea -= 2
print(surfaceArea)

# Part 2
reached_vertices = {(0,0,0)}
explored_vertices = set()
surfaceArea = 0
while len(reached_vertices) > 0:
    vert = reached_vertices.pop()
    for i in range(3):
        if vert[i] >= minima[i]: # Can go one space outside the minima
            if (neighbour := vecAdd(vert, tuple(-1 if i == j else 0 for j in range(3)))) in sortedCubes:
                surfaceArea += 1
            else:
                if neighbour not in explored_vertices:
                    reached_vertices.add(neighbour)
        if vert[i] <= maxima[i]:
            if (neighbour := vecAdd(vert, tuple(1 if i == j else 0 for j in range(3)))) in sortedCubes:
                surfaceArea += 1
            else:
                if neighbour not in explored_vertices:
                    reached_vertices.add(neighbour)
    explored_vertices.add(vert)
print(surfaceArea)
            

