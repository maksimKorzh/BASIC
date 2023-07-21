
#src = [i for i in '-(-((((7 + 2) * 5) / (10 - 5)) + ((6 * 4) - (9 / 3))) - ((((8 + 2) - 1) * (4 + 6)) / (9 - 3)))'.replace(' ', '')]
src = [i for i in '-(-((((7 + 2) * 5) / (numOne - 5)) + ((numTwo * 4) - (9 / 3))) - ((((8 + 2) - 1) * (4 + numTwo)) / (9 - 3)))'.replace(' ', '')]
#src = [i for i in '((10-5)+20/2)*4-(23+17)']
#src = [i for i in '((12+5)*(13-6))+10']  # works
#src = [i for i in '((12+5)*-(-13-6))+10']  # works
#src = [i for i in '2*10*3*5/3/20*10']  # works
#src = [i for i in '12+34-7+117-24']    # works
#src = [i for i in '2*10*3*5/3/20*10+10+34-7+117-24']  # works
#src = [i for i in '23*(17-5)-42/7+(342-456)*5']  # works
#src = [i for i in '(1+2+3)*(2+4)-6']  # works

#src = [i for i in '2+']  # works

buffer = []
variables = {
  'numOne': 10,
  'numTwo': 6
}; token = ''

def expr():
  a = term()
  while True:
    if token == '+': scan(); b = term(); a = a + b
    elif token == '-': scan(); b = term(); a = a - b
    else: return a  # check for errors if NULL

def term():
  a = factor()
  while True:
    scan()
    if token == '*': scan(); b = factor(); a = a * b
    elif token == '/': scan(); b = factor(); a = int(a / b)
    else: return a  # check for errors if NULL

def factor():
  if type(token) == int: return token
  if token == '(':
    scan(); a = expr()
    if a == None: return None
    if token == ')': return a
    else: return None
  elif token == '-': scan(); return -factor()
  else: return None

def number():
  num = 0; tok = ''
  while len(src) and src[0].isdigit():
    tok += src[0]; del src[0]; num = int(tok)
  return num

def variable():
  name = ''
  while len(src) and src[0].isalpha():
    name += src[0]; del src[0]
  if name not in variables: print('Variable "' + name + '" is not defined!')
  return variables[name]

def operator():
  op = src[0]
  del src[0]
  return op

def scan():
  global token
  if len(src) and src[0].isalpha(): token = variable();
  elif len(src) and src[0].isdigit(): token = number()
  elif len(src) and src[0] in '+-*/()': token = operator()

# main
print('EXPR:', ''.join(src))
#print('eval()', eval(''.join(src)))


try: 
  scan(); result = expr()
  if result is not None: print('expr()', result)
  else: print("Bad expression")
except: print("Execution failed!")

