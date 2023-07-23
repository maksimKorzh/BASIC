# BASIC interpreter

token = ''
variables = {
  'a': '10',
  'b': '6',
  'num': 'a'
}


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

def operator(line):
  op = line[0]
  del line[0]
  return op

def scan(line):
  global token
  if len(line) and line[0].isdigit(): token = number(line)
  elif len(line) and line[0].islower(): token = variable(line)
  elif len(line) and line[0] in '+-*/()=<>': token = operator(line)

line = '-((12+12)/4 + a * (b-17)) + num'
line = [c for c in line.replace(' ', '')]
scan(line)
print('Result:', calc(line))


