from math import floor, ceil

file = open("input.txt")

lines = [  line.split()  for line in ''.join(file.readlines()).split('\n') ]
sensors = [ [int(line[2][2:-1]), int(line[3][2:-1])] for line in lines ]
beacons = [ [int(line[-2][2:-1]), int(line[-1][2:])] for line in lines ]
def taxicab(w,z):
    return sum([abs(a - b) for a,b in zip(w,z)])
radii = [ taxicab(beacon, sensor) for beacon,sensor in zip(beacons, sensors) ]

# Boundary Method
boundary = 4000000 # 20 for Part 1

def checkLine(start, finish):
    print(f"Checking line: {start}, {finish}")
    x1, y1 = start
    x2, y2 = finish
    assert abs(x1 - x2) == abs(y1 - y2) # Gradient = +1 or -1
    assert x1 < x2
    m = +1 if y2 > y1 else -1 # Gradient
    c = y1 - m*x1 # y-intercept
    assert y2 == m*x2 + c

    # Use coords u = x + y
    #            v = x - y
    # Could combine m == 1 and m == -1 throughout, but I think it's clearer 
    if m == +1:
        canBeBeacon = { x+y: True for x,y in zip(range(x1, x2+1), range(y1,y2+1)) if 0 <= x <= boundary and 0 <= y <= boundary } # index by u
    else:
        canBeBeacon = { x-y: True for x,y in zip(range(x1, x2+1), range(y1,y2-1,-1)) if 0 <= x <= boundary and 0 <= y <= boundary } # index by v

    for sensor, radius in zip(sensors, radii):
        sx, sy = sensor
        sc = sy - m*sx 
        dist = abs(sc - c)
        rem = radius - dist 
        # print(f"sensor: {sx, sy}", radius, dist, rem)
        if rem < 0:
            continue
        u_s = sx + sy
        v_s = sx - sy
        # Calculate line overlap range
        if m == +1:
            left = u_s - radius
            right = u_s + radius + 1
        else:
            left = v_s - radius
            right = v_s + radius + 1
        for w in range(left, right):
            if w in canBeBeacon.keys():
                canBeBeacon[w] = False

    if any(canBeBeacon.values()):
        w = [z for z, val in canBeBeacon.items() if val].pop()
        if m == +1:
            x = (w + x1 - y1) // 2
            y = (w - x1 + y1) // 2
        else:
            x = (x1 + y1 + w) // 2
            y = (x1 + y1 - w) // 2
        print(f"Found  {x, y}!")
        print(4000000*x + y)
        return True
    return False

# print(checkLine([2, 18], [10,10]))

            # for y in range(sensor[1] - taxicab, sensor[1] + taxicab + 1):
            # left, right = calculateRowRange(sensor[0], sensor[1], taxicab, y)
            # for x in range(left, right):
            #     canBeBeacon[(x, y)] = False
            # # drawCoverage(canBeBeacon)
            # markComplete = True
            # for cont in canBeBeacon:
            #     if cont:
            #         markComplete = False
            #         break
            # if markComplete:
            #     rowsComplete[y] = True
            #     break
            # drawCoverage(canBeBeacon)
            # for cont in canBeBeacon:
            #     if cont:
            #         markComplete = False
            #         break
            # if markComplete:
            #     break

for sensor, radius in zip(sensors, radii):
    sx, sy = sensor
    # print(f"Sensor: {sensor}, radius: {radius}")
    if (checkLine([sx, sy - radius - 1], [sx + radius + 1, sy]) or checkLine([sx, sy + radius + 1], [sx + radius + 1, sy]) or checkLine([sx - radius - 1, sy], [sx, sy + radius + 1]) or checkLine([sx - radius - 1, sy], [sx, sy - radius - 1])):
        break

# def checkPoint(point):
#     if not (0 <= point[0] <= boundary): return False 
#     if not (0 <= point[1] <= boundary): return False 
#     foundSensor = False
#     for sensor, beacon in zip(sensors, beacons):
#         t = taxicab(point, sensor)
#         if t <= taxicab(sensor, beacon):
#             foundSensor = True
#             break
#     if not foundSensor:
#         print(point[0]*4000000 + point[1])
#         return True
#     return False

# shapes = []
# def compareShapes(shape1, shape2):
#     return None
# for sensor, radius in zip(sensors, radii):
#     # Add shape
#     sx, sy = sensor
#     newShape = [[sx, sy - radius], [sx + radius, sy], [sx, sy + radius], [sx - radius, sy]]
#     shapesToRemove = []
#     for shape in shapes:
#         # Compare shape and newShape
#         if (mergedShape := compareShapes(shape, newShape)) != None:
#             newShape = mergedShape
#             shapesToRemove.append(shape)
#     for shape in shapesToRemove:
#         shapes.remove(shape)     

    



# beaconExistsMegaGrid = [ [ True for y in range(0, 2000+1) ] for x in range(0, 2000+1) ]
# TODO: Tidy up other comments
# megaStep = 2000
# # Megagrid[x, y] = (megaStep*x, megaStep*y)        -- (megaStep*x + megaStep-1, megaStep*y)
# #                       |                               |
# #                  (megaStep*x, megaStep*y + megaStep-1) -- (megaStep*x + megaStep-1, megaStep*y + megaStep-1)
# def checkSquareCouldContainBeacon(topLeft, size):
#     for index in range(len(sensors)):
#         sx, sy = sensors[index]
#         st = taxicab(sensors[index], beacons[index])
#         topRight = [topLeft[0]+size-1, topLeft[1]]
#         bottomLeft = [topLeft[0], topLeft[1]+size-1]
#         bottomRight = [topLeft[0]+size-1,  topLeft[1]+size-1]
#         # Test left side
#         if sx > topLeft[0] + size//2: # sensor on the right
#             t1 = taxicab(sensors[index], topLeft) # Dist from top left
#             t2 = taxicab(sensors[index], bottomLeft) # Dist from bottom left
#             if st >= t1 and st >= t2:
#                 # print(sensors[index], topLeft, st, t1, t2, " left side")
#                 return False
#         # Test right side
#         if sx < topLeft[0] + size//2: # sensor on the left
#             t1 = taxicab(sensors[index], topRight) # Dist from top right
#             t2 = taxicab(sensors[index], bottomRight) # Dist from bottom right
#             if st >= t1 and st >= t2:
#                 # print(sensors[index], topLeft, st, t1, t2, "right side")
#                 return False
#         # Test top side
#         if sy > topLeft[1] + size//2: # sensor below
#             t1 = taxicab(sensors[index], topRight)
#             t2 = taxicab(sensors[index], topLeft)
#             if st >= t1 and st >= t2:
#                 # print(sensors[index], topLeft, st, t1, t2, "t top side")
#                 return False
#         # Test bottom
#         if sy < topLeft[1] + size//2: # sensor above
#             t1 = taxicab(sensors[index], bottomLeft) # Dist from bottom left
#             t2 = taxicab(sensors[index], bottomRight) # Dist from bottom right
#             if st >= t1 and st >= t2:
#                 # print(sensors[index], topLeft, st, t1, t2, "est bottom")
#                 return False
#     return True

# def divideSquare(topLeft, bigSize):
#     # assert size*10 == bigSize
#     if bigSize <= 4:
#         for j in range(bigSize):
#             for i in range(bigSize):
#                 if checkPoint([topLeft[0] + i, topLeft[1] + j]): return [topLeft[0] + i, topLeft[1] + j]

#     size = bigSize//2
#     for j in range(2):
#         for i in range(2):
#             x = topLeft[0]+i*size
#             y = topLeft[1]+j*size
#             smallSquare = checkSquareCouldContainBeacon([x, y], size)
#             if (smallSquare):
#                 # print(f"Zooming in at {x}, {y}", end = '')
#                 if (pos := divideSquare([x, y], size)) != False:
#                     return pos
#     return False

# print(' ')
# print(divideSquare([0,0], 4000000))
        
#         # # print('#' if (beaconExistsMegaGrid[mx][my]) else '.', end = '')
#         # if (beaconExistsMegaGrid[mx][my]):
#         #     print(f"Trying sensors at {mx}, {my}")
#         #     for y in range(my*megaStep, (my+1)*megaStep):
#         #         for x in range(mx*megaStep, (mx+1)*megaStep):
#         #             






# for x in range(0, 4000000):
#     for y in range(0, 4000000):
#         foundSensor = False
#         for i in range(len(sensors)):
#             sensor = sensors[i]
#             t = taxicab([x,y], sensor)
#             if t <= taxicab(sensor, beacons[i]):
#                 foundSensor = True
#                 break
#         if not foundSensor:
#             print(x*4000000 + y)
#             break


# row = 2000000
# maxY = 4000000
# maxX1 = max([sensor[0] for sensor in sensors])
# maxX2 = max([beacon[0] for beacon in beacons])
# maxX = maxX2 if maxX2 > maxX1 else (2 * maxX1) - maxX2
# minX1 = min([sensor[0] for sensor in sensors])
# minX2 = min([beacon[0] for beacon in beacons])
# minX = minX2 if minX2 < minX1 else (2 * minX1) - minX2
# canBeBeacon = { (x, y) : True for x in range(minX-1, maxX+1) for y in range(0, maxY+1) }
# rowsComplete = [ False for y in range(0, maxY+1)]

# # def drawCoverage(canBeBeacon):
# #     for x in canBeBeacon.values():
# #         print('#' if not x else '.', end = '')
# #     print('')

# def calculateRowRange(x, y, t, row):
#     rowDist = abs(row - y)
#     left = x - t + rowDist
#     right = x + t - rowDist + 1
#     return left, right

# def getBeaconPlaces():
#     for i in range(len(sensors)):
#         sensor = sensors[i]
#         beacon = beacons[i]
#         taxicab = sum([abs(s - b) for s,b in zip(sensor,beacon)])
#         for y in range(sensor[1] - taxicab, sensor[1] + taxicab + 1):
#             if not rowsComplete[y]:
#                 left, right = calculateRowRange(sensor[0], sensor[1], taxicab, y)
#                 for x in range(left, right):
#                     canBeBeacon[(x, y)] = False
#                 # drawCoverage(canBeBeacon)
#                 markComplete = True
#                 for cont in canBeBeacon:
#                     if cont:
#                         markComplete = False
#                         break
#                 if markComplete:
#                     rowsComplete[y] = True
#                     break

#     # for i in range(len(beacons)):
#     #     beacon = beacons[i]
#     #     if beacon[1] == row:
#     #         canBeBeacon[beacon[0]] = True

#     return canBeBeacon

# # canBeBeacon = getBeaconPlaces(2000000)
# # # drawCoverage(canBeBeacon)
# # print(sum([not x for x in canBeBeacon.values()]))

# found = False
# for y in range(maxY+1):
#     canBeBeacon = getBeaconPlaces()
#     for x in range(maxY):
#         if canBeBeacon[(x, y)]:
#             print(x, y)
#             print(4000000 * x + y)
#             found = True
#             break
#     if found:
#         break
#     # drawCoverage(canBeBeacon)
