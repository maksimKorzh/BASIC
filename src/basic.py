import os

token = ''
line_number = 0
goto = False
variables = {}
buffer = {}


def run():
    global line_number, goto

    line_iterator = iter(buffer)
    goto = False

    while True:
        try:
            if goto:
                goto = False
                current_iterator = iter(buffer)
                current_line = next(current_iterator)

                while line_number != current_line:
                    current_line = next(current_iterator)
                line_iterator = current_iterator
            else:
                line_number = next(line_iterator)

            line = buffer[line_number]
            execute(line_number, line)
        except:
            break


def execute(line_num, line):
    try:
        line_list = list(line)
        scan(line_list)

        if token == "PRINT":
            print_statement(line_list)
        elif token == "LET":
            let_statement(line_list)
        elif token == 'IF':
            if_statement(line_num, line_list)
        elif token == "GOTO":
            goto_statement(line_list)
    except:
        print(f"Line {line_num}: Execution failed!")


def print_statement(line):
    line_str = "".join(line).strip()
    args = ",".join(line_str.split(",")[1:])

    line_list = list(line_str)
    scan(line_list)

    if isinstance(token, str) and token[0] == '"':
        print(token[1:-1], end="")
        scan(line_list)
    else:
        line_list = list(line_str.replace(" ", ""))
        print(calculate(line_list), end="")

    print_statement(args) if token == "," else print()


def let_statement(line):
    line_str = "".join(line).replace(" ", "")

    if "=" not in line_str:
        print('Missing "=" in variable definition!')
        raise ValueError

    name, val = map(str.strip, line_str.split("="))

    if not val:
        print("Missing variable value!")
        raise ValueError
    elif val == "INPUT":
        try:
            variables[name] = int(user_input())
        except:
            print("Input must be an integer!")
            raise ValueError
    else:
        val_list = list(val)
        scan(val_list)

        variables[name] = calculate(val_list)


def if_statement(line_num, line):
    # Split the line into parts based on "THEN"
    parts = "".join(line).split("THEN")

    # Check if there are exactly two parts
    if len(parts) != 2:
        print('Missing "THEN" after condition!')
        raise ValueError

    condition_clause = list("".join(parts[0]).replace(" ", ""))
    then_clause = list("".join(parts[1].strip()))
    line_list = condition_clause + then_clause

    scan(line_list)
    left_expr = calculate(line_list)

    operator = token
    scan(line_list)

    right_expr = calculate(line_list)
    scan(line_list)

    # Evaluate the condition
    condition = False
    if operator == ">":
        condition = left_expr > right_expr
    elif operator == "<":
        condition = left_expr < right_expr
    elif operator == "=":
        condition = left_expr == right_expr

    # Execute the line if the condition is true
    if condition:
        execute(line_num, f'{token} {"".join(line_list)}')


def goto_statement(line):
    global line_number, goto

    line_list = list("".join(line).replace(" ", ""))
    scan(line_list)

    # Calculate the line number
    line_number = calculate(line_list)

    # Set the goto flag to True
    goto = True


def calculate(line):
    try:
        result = expression(line)

        if result is not None:
            return result
        else:
            print("Invalid expression!")
    except:
        print("Calculation failed!")


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
        else:
            return a


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
        else:
            return a


def factor(line):
    if isinstance(token, int):
        return token

    if token == '(':
        scan(line)
        a = expression(line)

        if a is None:
            return None
        elif token == ')':
            return a
        else:
            return None
    elif token == '-':
        scan(line)

        return -factor(line)
    else:
        return None


def scan(line):
    global token
    if line and (first_char := line[0]):
        if first_char.isdigit():
            token = number(line)
        elif first_char.islower():
            token = variable(line)
        elif first_char.isupper():
            token = statement(line)
        elif first_char in "+-*/()=<>,":
            token = operator(line)
        elif first_char == '"':
            token = string(line)


def number(line):
    num_str = ""
    while line and line[0].isdigit():
        num_str += line.pop(0)

    return int(num_str)


def variable(line):
    var_name = ""
    while line and line[0].islower():
        var_name += line.pop(0)

    if var_name not in variables:
        print(f'Variable "{var_name}" is not defined!')

    try:
        return int(variables[var_name])
    except:
        return int(variables[variables[var_name]])


def statement(line):
    keyword = ""
    while line and line[0].isupper():
        keyword += line.pop(0)

    if keyword not in ["PRINT", "LET", "IF", "THEN", "GOTO"]:
        print(f'Unknown keyword "{keyword}"!')
        raise ValueError
    else:
        return keyword


def operator(line):
    return line.pop(0)


def string(line):
    line.pop(0)

    str_val = ""
    while line and line[0] != '"':
        str_val += line.pop(0)

    if not line:
        print('Missing closing \'"\'!')
        raise ValueError
    else:
        line.pop(0)
        return f'"{str_val}"'


def clear_screen():
    os.system("clear")


def load_file():
    try:
        file_name = input("File name: ")
        with open(file_name) as file:
            buffer.clear()
            for file_line in file.read().split("\n"):
                try:
                    line_number, line_code = map(str.strip,
                                                 file_line.split(" ", 1))
                    buffer[int(line_number)] = line_code
                except:
                    pass
    except:
        print(f"Failed to load file!")


def save_file():
    try:
        file_name = input("File name: ")
        with open(file_name, "w") as file:
            for line_number, line_code in buffer.items():
                file.write(f"{line_number} {line_code}\n")
    except:
        print(f"Failed to save file!")


def list_buffer():
    for line_number, line_code in sorted(buffer.items()):
        print(line_number, line_code)


commands = {
    "quit": lambda: exit(),
    "run": run,
    "new": lambda: buffer.clear(),
    "load": load_file,
    "save": save_file,
    "list": list_buffer,
    "clear": clear_screen,
}

while True:
    user_input = input("> ")

    if user_input in commands:
        try:
            commands[user_input]()
        except:
            pass
    else:
        try:
            line_number, line_code = map(str.strip, user_input.split(" ", 1))
            buffer[int(line_number)] = line_code
        except:
            execute(0, user_input)
