file = open("input.txt")

lines = ''.join(file.readlines()).split('\n')
char_to_digit = {'2':2, '1':1, '0':0, '-':-1, '=':-2}
digit_to_char = {2:'2', 1:'1', 0:'0', -1:'-', -2:'='}

decimals = []
for snafu in lines:
    exp = 1
    decimal = 0
    snafu = [ char for char in snafu ]
    snafu.reverse()
    for char in snafu:
        digit = char_to_digit[char]
        decimal = decimal + exp*digit
        exp *= 5
    decimals.append(decimal)
    print(decimal)
    
sum_decimals = sum(decimals)
print(sum_decimals)

snafu = ''
while sum_decimals > 0:
    mod = sum_decimals % 5
    if mod >= 3:
        mod -= 5
    char = digit_to_char[mod]
    snafu = char + snafu
    sum_decimals -= mod
    assert sum_decimals % 5 == 0
    sum_decimals = sum_decimals // 5
print(snafu)