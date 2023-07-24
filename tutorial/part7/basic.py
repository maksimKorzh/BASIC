# BASIC interpreter
import os

token = ''
buffer = {
  10: 'PRINT "Count program"',
  20: 'LET count = 0',
  30: 'PRINT "Count: ", count',
  40: 'LET count = count + 1',
  50: 'IF count < 10 THEN GOTO 30',
  60: 'PRINT "All done!"'
}
variables = {}
line_number = 0
goto = False

def run():
  global line_number, goto
  line_iterator = iter(buffer)
  goto = False
  while True:
    try: 
      if goto == False: line_number = next(line_iterator)
      if goto == True:
        goto = False
        current_iterator = iter(buffer)
        current_line = next(current_iterator)
        while line_number != current_line:
          current_line = next(current_iterator)
        line_iterator = current_iterator
      line = buffer[line_number]
      execute(line_number, line)
    except: break

def execute(num, line):
  try: 
    line = [c for c in line]
    scan(line)
    if   token == 'PRINT': print_statement(line)
    elif token == 'GOTO': goto_statement(line)
    elif token == 'LET': let_statement(line)
    elif token == 'IF': if_statement(num, line)
  except: 
    print('Line ' + str(num) + ': ', end='')
    print('Execution failed!')

def print_statement(line):
  line = [c for c in ''.join(line).strip()]
  scan(line);
  args = ','.join(''.join(line).split(',')[1:])
  if type(token) == str and token[0] == '"':
    print(token[1:-1], end='')
    scan(line);
  else: 
    line = [c for c in ''.join(line).replace(' ', '')]
    print(calc(line), end='')
  if token == ',': print_statement(args)
  else: print()

def goto_statement(line):
  global line_number, goto
  line = [c for c in ''.join(line).replace(' ','')]
  scan(line)
  line_number = calc(line)
  goto = True

def let_statement(line):
  line = ''.join(line).replace(' ', '')
  if '=' not in line:
    print('Missing "=" in variable definition!')
    raise ValueError
  name = line.split('=')[0]
  val = line.split('=')[1]
  if val == '':
    print('Missing variable value!')
    raise ValueError
  elif val == 'INPUT':
    try: variables[name] = int(input())
    except: 
      print('Input must be an integer!')
      raise ValueError
  else: 
    val = [c for c in val]
    scan(val)
    variables[name] = calc(val)

def if_statement(num, line):
  line = ''.join(line).split('THEN')
  if len(line) != 2:
    print('Missing "THEN" after condition!')
    raise ValueError
  line[0] = [c for c in ''.join(line[0]).replace(' ', '')]
  line[1] = [c for c in ''.join(line[1].strip())]
  line = line[0] + line[1]
  scan(line)
  left_expr = calc(line)
  op = token
  scan(line)
  right_expr = calc(line)
  scan(line)
  condition = False
  if op == '>': condition = left_expr > right_expr
  if op == '<': condition = left_expr < right_expr
  if op == '=': condition = left_expr == right_expr
  if condition == True: execute(num, token + ' ' + ''.join(line))

def calc(line):
  try: 
    result = expression(line)
    if result is not None: return result
    else: print('Bad expression!')
  except: print('Execution failed!')

def expression(line):
  a = term(line)
  while True:
    if token == '+':
      scan(line)
      b = term(line)
      a = a + b
    elif token == '-':
      scan(line)
      b = term(line)
      a = a - b
    else: return a

def term(line):
  a = factor(line)
  while True:
    scan(line)
    if token == '*':
      scan(line)
      b = factor(line)
      a = a * b
    elif token == '/':
      scan(line)
      b = factor(line)
      a = int(a / b)
    else: return a

def factor(line):
  if type(token) == int: return token
  if token == '(':
    scan(line); a = expression(line)
    if a == None: return None
    if token == ')': return a
    else: return None
  elif token == '-':
    scan(line)
    return -factor(line)
  else: return None

def number(line):
  num = 0; tok = ''
  while len(line) and line[0].isdigit():
    tok += line[0]
    del line[0]
    num = int(tok)
  return num

def variable(line):
  name = ''
  while len(line) and line[0].islower():
    name += line[0]
    del line[0]
  if name not in variables:
    print('Variable "' + name + '" is not defined!')
  try: return int(variables[name])
  except: return int(variables[variables[name]])

def statement(line):
  keyword = ''
  while len(line) and line[0].isupper():
    keyword += line[0]
    del line[0]
  if keyword not in ['PRINT', 'LET', 'IF', 'THEN', 'GOTO']:
    print('Unknown keyword "' + keyword + '"')
    raise ValueError
  else: return keyword

def operator(line):
  op = line[0]
  del line[0]
  return op

def string(line):
  msg = ''; del line[0]
  while len(line) and line[0] != '"':
    msg += line[0]
    del line[0]
  if not len(line):
    print('Missing closing \'"\'!')
    raise ValueError
  else: del line[0]; return '"' + msg + '"'

def scan(line):
  global token
  if len(line) and line[0].isdigit(): token = number(line)
  elif len(line) and line[0].islower(): token = variable(line)
  elif len(line) and line[0].isupper(): token = statement(line)
  elif len(line) and line[0] in '+-*/()=<>,': token = operator(line)
  elif len(line) and line[0] == '"': token = string(line)

os.system('clear')
while True:
  line = input('> ')
  if line == 'quit': break
  elif line == 'run': run()
  elif line == 'new': buffer = {}
  elif line == 'load':
    try: 
      filename = input('Filename: ')
      with open(filename) as f:
        buffer = {}
        for line in f.read().split('\n'):
          try: 
            num = int(line.split(' ')[0])
            src = ' '.join(line.split(' ')[1:])
            buffer[num] = src
          except: pass
    except: print('Failed to load file!')
  elif line == 'save':
    try: 
      filename = input('Filename: ')
      with open(filename, 'w') as f:
        for num, line in buffer.items():
          f.write(str(num) + ' ' + line + '\n')
    except: print('Failed to save file!')
  elif line == 'list': [print(num, line) for num, line in buffer.items()]
  elif line == 'clear': os.system('clear')
  else: 
    try: 
      line_num = int(line.split(' ')[0])
      if line_num < len(buffer): buffer[line_num] = line
      else: buffer[line_num] = ' '.join(line.split(' ')[1:])
    except: execute(0, line)
