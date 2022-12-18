file = open("input.txt")

lines = [  line.split()  for line in ''.join(file.readlines()).split('\n') ]
sensors = [ [int(line[2][2:-1]), int(line[3][2:-1])] for line in lines ]
beacons = [ [int(line[-2][2:-1]), int(line[-1][2:])] for line in lines ]
def taxicab(w,z):
    return sum([abs(a - b) for a,b in zip(w,z)])
radii = [ taxicab(beacon, sensor) for beacon,sensor in zip(beacons, sensors) ]

maxX1 = max([sensor[0] for sensor in sensors])
maxX2 = max([beacon[0] for beacon in beacons])
maxX = maxX2 if maxX2 > maxX1 else (2 * maxX1) - maxX2
minX1 = min([sensor[0] for sensor in sensors])
minX2 = min([beacon[0] for beacon in beacons])
minX = minX2 if minX2 < minX1 else (2 * minX1) - minX2
canBeBeacon = { x : True for x in range(minX-1, maxX+1) }
# rowsComplete = [ False for y in range(0, maxY+1)]

def drawCoverage(canBeBeacon):
    for x in canBeBeacon.values():
        print('#' if not x else '.', end = '')
    print('')

def calculateRowRange(x, y, t, row):
    rowDist = abs(row - y)
    left = x - t + rowDist
    right = x + t - rowDist + 1
    return left, right

def getBeaconPlaces(row):
    for sensor, radius in zip(sensors, radii):
        sx, sy = sensor
        left, right = calculateRowRange(sx, sy, radius, row)
        for x in range(left, right):
            canBeBeacon[x] = False
        # drawCoverage(canBeBeacon)

    for beacon in beacons:
        if beacon[1] == row:
            canBeBeacon[beacon[0]] = True

    return canBeBeacon

canBeBeacon = getBeaconPlaces(2000000)
print(sum([not x for x in canBeBeacon.values()]))
