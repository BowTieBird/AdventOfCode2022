file = open("input.txt")

monkeys_txt = ''.join(file.readlines()).split('\n\n')
monkeys_txt = [ monkey.split('\n') for monkey in monkeys_txt ]

items = [ [int(worry) for worry in monkey[1].split(':')[1].split(',')] for monkey in monkeys_txt]
inspectCount = [ 0 for _ in monkeys_txt ]

bigMod = 2*3*5*7*11*13*13*17*19*23 # All primes included in input (could get programmatically)

# for j in range(20):
for j in range(10000):
    for i in range(len(monkeys_txt)):
        monkey = monkeys_txt[i]
        while len(items[i]) > 0:
            old = items[i].pop(0)
            old = old % bigMod
            # inspect
            new = -1
            exec(monkey[2].split(':')[1].strip())
            assert new >= 0
            inspectCount[i] += 1
            # relief
            # new = new // 3
            new = new % bigMod

            # test
            div = int(monkey[3][21:])
            
            assert bigMod % div == 0
            test = new % div == 0
            # throw
            if (test):
                throwee = int(monkey[4][29:])
            else:
                throwee = int(monkey[5][30:])
            items[throwee].append(new)
    if j+1 in [1, 20, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
        print(inspectCount)

sortedInspectCount = sorted(inspectCount)
print(sortedInspectCount[-2] * sortedInspectCount[-1])