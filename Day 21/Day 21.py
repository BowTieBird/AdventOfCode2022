import sympy as sym
file = open("input.txt")

lines = ''.join(file.readlines()).split('\n')

monkey_functions = set()

for line in lines:
    monkey, instruction = line.split(': ')

    if not instruction.isdigit():
        instruction = instruction.split()
        instruction[0] += '()'
        instruction[2] += '()'
        instruction = ' '.join(instruction)

    # Comment out for part 1
    if monkey == 'humn':
        instruction = "sym.Symbol('x')"        
    if monkey == 'root':
        instruction = instruction.split()
        exec(f"def {monkey}():\n"
            f"   return sym.solve({instruction[0]} - {instruction[2]},'x')\n"
            f"monkey_functions.add({monkey})")

    # This is so janky; I love it.
    exec(f"def {monkey}():\n"
        f"   return {instruction}\n"
        f"monkey_functions.add({monkey})")

for f in monkey_functions:
    if f.__name__ == 'root':
        print(f())


        






