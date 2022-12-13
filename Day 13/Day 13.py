import functools

file = open("input.txt")

pairs_txt = ''.join(file.readlines()).split('\n\n')
packets_txt = ('\n'.join(pairs_txt)).split('\n')
pairs_lists = [ comparison.split('\n') for comparison in pairs_txt ]

packets = []
for x in packets_txt:
    exec('x = ' + x)
    packets.append(x)

divider1 = [[2]]
divider2 = [[6]]
packets.append(divider1)
packets.append(divider2)

def compare(x, y):
    if not isinstance(x, list):
        if not isinstance(y, list):
            # Both integers
            if x < y:
                return -1 # "Right Order"
            if x > y:
                return 1 # "Wrong Order"
            if x == y:
                return 0 # "Equal"
        else:
            # x int, y list
            x = [x]
            return compare(x, y)
    else:
        if not isinstance(y, list):
            # x list, y int
            y = [y]
            return compare(x, y)
        else:
            # Both lists
            ind = 0
            while True:
                if len(x) == ind and len(y) == ind:
                    return 0 # "Equal"
                elif len(x) == ind and len(y) > ind:
                    return -1 # "Right Order"
                elif len(x) > ind and len(y) == ind:
                    return 1 # "Wrong Order"
                else:
                    res = compare(x[ind], y[ind])
                    if res != 0: # "Equal"
                        return res
                ind += 1
            

sum = 0
for i in range(len(pairs_lists)):
    pair = pairs_lists[i]
    x = 0
    y = 0
    exec('x = ' + pair[0])
    exec('y = ' + pair[1])
    if(compare(x, y) == -1): sum += i+1
print(sum)

sortedList = sorted(packets, key = functools.cmp_to_key(compare))
print((sortedList.index(divider1)+1) * (sortedList.index(divider2)+1))

    
    
