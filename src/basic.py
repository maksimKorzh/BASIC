buffer = []
variables = {
  'numOne': 10,
  'numTwo': 6
}; token = ''

def expression(expr):
  a = term(expr)
  while True:
    if token == '+': scan(expr); b = term(expr); a = a + b
    elif token == '-': scan(expr); b = term(expr); a = a - b
    else: return a

def term(expr):
  a = factor(expr)
  while True:
    scan(expr)
    if token == '*': scan(expr); b = factor(expr); a = a * b
    elif token == '/': scan(expr); b = factor(expr); a = int(a / b)
    else: return a

def factor(expr):
  if type(token) == int: return token
  if token == '(':
    scan(expr); a = expression(expr)
    if a == None: return None
    if token == ')': return a
    else: return None
  elif token == '-': scan(expr); return -factor(expr)
  else: return None

def number(expr):
  num = 0; tok = ''
  while len(expr) and expr[0].isdigit():
    tok += expr[0]; del expr[0]; num = int(tok)
  return num

def variable(expr):
  name = ''
  while len(expr) and expr[0].isalpha():
    name += expr[0]; del expr[0]
  if name not in variables: print('Variable "' + name + '" is not defined!')
  return variables[name]

def operator(expr):
  op = expr[0]
  del expr[0]
  return op

def scan(expr):
  global token
  if len(expr) and expr[0].isdigit(): token = number(expr)
  elif len(expr) and expr[0].isalpha(): token = variable(expr);
  elif len(expr) and expr[0] in '+-*/()': token = operator(expr)

def calc(expr):
  #try: 
    scan(e); result = expression(expr)
    if result is not None: return result
    else: print("Bad expressionession")
  #except: print("Execution failed!")

e = [i for i in '-(-((((7 + 2) * 5) / (numOne - 5)) + ((numTwo * 4) - (9 / 3))) - ((((8 + 2) - 1) * (4 + numTwo)) / (9 - 3)))'.replace(' ', '')]
print(calc(e))
