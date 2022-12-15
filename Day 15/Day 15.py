file = open("input.txt")

lines = [  line.split()  for line in ''.join(file.readlines()).split('\n') ]
sensors = [ [int(line[2][2:-1]), int(line[3][2:-1])] for line in lines ]
beacons = [ [int(line[-2][2:-1]), int(line[-1][2:])] for line in lines ]

beaconExistsMegaGrid = [ [ True for y in range(0, 2000+1) ] for x in range(0, 2000+1) ]


def taxicab(w,z):
    return sum([abs(a - b) for a,b in zip(w,z)])


megaStep = 2000
# Megagrid[x, y] = (megaStep*x, megaStep*y)        -- (megaStep*x + megaStep-1, megaStep*y)
#                       |                               |
#                  (megaStep*x, megaStep*y + megaStep-1) -- (megaStep*x + megaStep-1, megaStep*y + megaStep-1)
for my in range(0, megaStep+1):
    for mx in range(0, megaStep+1):
        for index in range(len(sensors)):
            sx, sy = sensors[index]
            st = taxicab(sensors[index], beacons[index])
            topLeft = [megaStep*mx, megaStep*my]
            topRight = [megaStep*mx + megaStep-1, megaStep*my]
            bottomLeft = [megaStep*mx, megaStep*my + megaStep-1]
            bottomRight = [megaStep*mx + megaStep-1, megaStep*my + megaStep-1]
            # Test left side
            if sx >= megaStep*mx + megaStep-1: # sensor on the right
                t1 = taxicab([sx,sy], topLeft) # Dist from top left
                t2 = taxicab([sx,sy], bottomLeft) # Dist from bottom left
                if st >= t1 >= 2000 and st >= t2 >= 2000:
                    beaconExistsMegaGrid[mx][my] = False
                    break
            # Test right side
            if sx <= megaStep*mx: # sensor on the left
                t1 = taxicab([sx,sy], topRight) # Dist from top right
                t2 = taxicab([sx,sy], bottomRight) # Dist from bottom right
                if st >= t1 >= 2000 and st >= t2 >= 2000:
                    beaconExistsMegaGrid[mx][my] = False
                    break
            # Test top side
            if sy >= megaStep*my + megaStep-1: # sensor below
                t1 = taxicab([sx,sy], topRight)
                t2 = taxicab([sx,sy], topLeft)
                if st >= t1 >= 2000 and st >= t2 >= 2000:
                    beaconExistsMegaGrid[mx][my] = False
                    break
            # Test bottom
            if sy <= megaStep*my: # sensor above
                t = taxicab([sx,sy], bottomLeft) # Dist from bottom left
                t = taxicab([sx,sy], bottomRight) # Dist from bottom right
                if st >= t1 >= 2000 and st >= t2 >= 2000:
                    beaconExistsMegaGrid[mx][my] = False
                    break
        # print('#' if (beaconExistsMegaGrid[mx][my]) else '.', end = '')
        if (beaconExistsMegaGrid[mx][my]):
            print(f"Trying sensors at {mx}, {my}")
            for y in range(my*megaStep, (my+1)*megaStep):
                for x in range(mx*megaStep, (mx+1)*megaStep):
                    foundSensor = False
                    for i in range(len(sensors)):
                        sensor = sensors[i]
                        t = taxicab([x,y], sensor)
                        if t <= taxicab(sensor, beacons[i]):
                            foundSensor = True
                            break
                    if not foundSensor:
                        print(x*4000000 + y)
                        break






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
