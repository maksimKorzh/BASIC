import os

buffer = {}
variables = {'numone': 10, 'numtwo': 6}
token = ''

def execute(num, line):
  try: 
    line = [c for c in line]; scan(line)
    if token == 'PRINT': print_statement(line); scan(line)
  except: 
    print('Line ' + str(num) + ': ', end='')
    print("Execution failed!")

def print_statement(line):
  line = [c for c in ''.join(line).strip()]; scan(line)
  if type(token) == str and token[0] == '"':
    print(token[1:-1], end=' '); scan(line)
  else: 
    line = [c for c in ''.join(line).replace(' ', '')]
    print(calc(line), end=' ')
  if token == ',': print_statement(line)
  else: print()
  
def calc(line):
  try: 
    result = expression(line)
    if result is not None: return result
    else: print("Bad expression")
  except: print("Execution failed!")

def expression(line):
  a = term(line)
  while True:
    if token == '+': scan(line); b = term(line); a = a + b
    elif token == '-': scan(line); b = term(line); a = a - b
    else: return a

def term(line):
  a = factor(line)
  while True:
    scan(line)
    if token == '*': scan(line); b = factor(line); a = a * b
    elif token == '/': scan(line); b = factor(line); a = int(a / b)
    else: return a

def factor(line):
  if type(token) == int: return token
  if token == '(':
    scan(line); a = expression(line)
    if a == None: return None
    if token == ')': return a
    else: return None
  elif token == '-': scan(line); return -factor(line)
  else: return None

def number(line):
  num = 0; tok = ''
  while len(line) and line[0].isdigit():
    tok += line[0]; del line[0]; num = int(tok)
  return num

def variable(line):
  name = ''
  while len(line) and line[0].islower():
    name += line[0]; del line[0]
  if name not in variables:
    print('Variable "' + name + '" is not defined!')
  return variables[name]

def statement(line):
  keyword = ''
  while len(line) and line[0].isupper():
    keyword += line[0]; del line[0]
  if keyword not in ['PRINT', 'IF', 'GOTO']:
    print('Unknown keyword "' + keyword + '"!')
    raise ValueError
  else: return keyword

def operator(line):
  op = line[0]
  del line[0]
  return op

def string(line):
  msg = ''; del line[0]
  while len(line) and line[0] != '"':
    msg += line[0]; del line[0]
  if not len(line):
    print('Missing closing \'"\'!')
    raise ValueError
  else: del line[0]; return '"' + msg + '"'

def scan(line):
  global token
  if len(line) and line[0].isdigit(): token = number(line)
  elif len(line) and line[0].islower(): token = variable(line);
  elif len(line) and line[0].isupper(): token = statement(line)
  elif len(line) and line[0] in '+-*/(),': token = operator(line)
  elif len(line) and line[0] == '"': token = string(line)

#e = [i for i in '-(-((((7 + 2) * 5) / (numone - 5)) + ((numtwo * 4) - (9 / 3))) - ((((8 + 2) - 1) * (4 + numtwo)) / (9 - 3)))'.replace(' ', '')]
#print(calc(e))

os.system('clear')
while True:
  line = input('> ')
  if line == 'quit': break
  elif line == 'run': [execute(num, line) for num, line in sorted(buffer.items())]
  elif line == 'list': [print(num, line) for num, line in sorted(buffer.items())]
  elif line == 'clear': os.system('clear')
  else: 
    try:
      line_num = int(line.split(' ')[0])
      if line_num < len(buffer): buffer[line_num] = line
      else: buffer[line_num] = ''.join(line.split(' ')[1:])
    except: execute(0, line)
