file = open("input.txt")

_txt = ''.join(file.readlines()).split('\n\n')
_txt = [ monkey.split('\n') for monkey in _txt ]