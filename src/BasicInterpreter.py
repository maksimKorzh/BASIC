class BasicInterpreter:
    """"""

    def __init__(self):
        """"""
        self.token = ""
        self.line_number = 0
        self.goto = False
        self.variables = {}
        self.buffer = {}

    def run(self):
        """

        :return:
        """
        line_iterator = iter(self.buffer)
        self.goto = False

        while True:
            try:
                if self.goto:
                    self.goto = False
                    current_iterator = iter(self.buffer)
                    current_line = next(current_iterator)

                    while self.line_number != current_line:
                        current_line = next(current_iterator)
                    line_iterator = current_iterator
                else:
                    self.line_number = next(line_iterator)

                line_str = self.buffer[self.line_number]
                self.execute(line_str)
            except Exception:
                raise Exception

    def execute(self, line_str):
        """

        :param line_str:
        :return:
        """
        try:
            line_list = list(line_str)
            self.scan(line_list)

            if self.token == "PRINT":
                self.print_statement(line_list)
            elif self.token == "LET":
                self.let_statement(line_list)
            elif self.token == "IF":
                self.if_statement(line_list)
            elif self.token == "GOTO":
                self.goto_statement(line_list)
        except Exception as e:
            print(
                f'The execution has failed on line {self.line_number} due to the following error: "{e}".'
            )

    def print_statement(self, line_list):
        """

        :param line_list:
        :return:
        """
        line_str = "".join(line_list).strip()
        line_list = list(line_str)
        self.scan(line_list)

        if isinstance(self.token, str) and self.token[0] == '"':
            print(self.token[1:-1], end="")
            self.scan(line_list)
        else:
            line_list = list(line_str.replace(" ", ""))
            print(self.calculate(line_list), end="")

        remaining_args = ",".join(line_str.split(",")[1:])
        self.print_statement(remaining_args) if self.token == "," else print()

    def let_statement(self, line_list):
        """

        :param line_list:
        :return:
        """
        line_str = "".join(line_list).replace(" ", "")

        if "=" not in line_str:
            print('The "=" is missing in the variable definition!')
            raise ValueError

        name, val = map(str.strip, line_str.split("="))

        if not val:
            print("The variable value is missing!")
            raise ValueError
        elif val == "INPUT":
            try:
                self.variables[name] = int(input())
            except ValueError:
                print("The input must be an integer!")
                raise ValueError
        else:
            val_list = list(val)
            self.scan(val_list)

            self.variables[name] = self.calculate(val_list)

    def if_statement(self, line_list):
        """

        :param line_list:
        :return:
        """
        parts = "".join(line_list).split("THEN")

        if len(parts) != 2:
            print('The "THEN" keyword is missing after the condition!')
            raise ValueError

        condition_clause = list("".join(parts[0]).replace(" ", ""))
        then_clause = list("".join(parts[1].strip()))
        line_list = condition_clause + then_clause

        self.scan(line_list)
        left_expression = self.calculate(line_list)

        operator = self.token
        self.scan(line_list)

        right_expression = self.calculate(line_list)
        self.scan(line_list)

        condition = False
        if operator == ">":
            condition = left_expression > right_expression
        elif operator == "<":
            condition = left_expression < right_expression
        elif operator == "=":
            condition = left_expression == right_expression

        if condition:
            self.execute(f'{self.token} {"".join(line_list)}')

    def goto_statement(self, line_list):
        """

        :param line_list:
        :return:
        """
        line_list = list("".join(line_list).replace(" ", ""))
        self.scan(line_list)

        self.line_number = self.calculate(line_list)
        self.goto = True

    def calculate(self, line_list):
        """

        :param line_list:
        :return:
        """
        try:
            result = self.expression(line_list)

            if result is None:
                print(f"An invalid expression is found on line {self.line_number}!")
            else:
                return result
        except Exception as e:
            print(f'The calculation has failed due to the following error: "{e}".')

    def expression(self, line_list):
        """

        :param line_list:
        :return:
        """
        a = self.term(line_list)

        while True:
            if self.token == "+":
                self.scan(line_list)
                b = self.term(line_list)

                a += b
            elif self.token == "-":
                self.scan(line_list)
                b = self.term(line_list)

                a -= b
            else:
                return a

    def term(self, line_list):
        """

        :param line_list:
        :return:
        """
        a = self.factor(line_list)

        while True:
            self.scan(line_list)

            if self.token == "*":
                self.scan(line_list)
                b = self.factor(line_list)

                a *= b
            elif self.token == "/":
                self.scan(line_list)
                b = self.factor(line_list)

                a = int(a / b)
            else:
                return a

    def factor(self, line_list):
        """

        :param line_list:
        :return:
        """
        if isinstance(self.token, int):
            return self.token

        if self.token == "(":
            self.scan(line_list)
            a = self.expression(line_list)

            if a is None:
                return None
            elif self.token == ")":
                return a
            else:
                return None
        elif self.token == "-":
            self.scan(line_list)

            return -self.factor(line_list)
        else:
            return None

    def scan(self, line_list):
        """

        :param line_list:
        :return:
        """
        if line_list and (first_char := line_list[0]):
            if first_char.isdigit():
                self.token = self.number(line_list)
            elif first_char.islower():
                self.token = self.variable(line_list)
            elif first_char.isupper():
                self.token = self.statement(line_list)
            elif first_char in "+-*/()=<>,":
                self.token = self.operator(line_list)
            elif first_char == '"':
                self.token = self.string(line_list)

    @staticmethod
    def number(line_list):
        """

        :param line_list:
        :return:
        """
        num_str = ""
        while line_list and line_list[0].isdigit():
            num_str += line_list.pop(0)

        return int(num_str)

    def variable(self, line_list):
        """

        :param line_list:
        :return:
        """
        var_name = ""
        while line_list and line_list[0].islower():
            var_name += line_list.pop(0)

        if var_name not in self.variables:
            print(f'Variable "{var_name}" is not defined!')

        try:
            return int(self.variables[var_name])
        except KeyError:
            raise KeyError

    @staticmethod
    def statement(line_list):
        """

        :param line_list:
        :return:
        """
        keyword = ""
        while line_list and line_list[0].isupper():
            keyword += line_list.pop(0)

        if keyword not in ["PRINT", "LET", "IF", "THEN", "GOTO"]:
            print(f'"{keyword}" is an unknown keyword!')
            raise ValueError
        else:
            return keyword

    @staticmethod
    def operator(line_list):
        """

        :param line_list:
        :return:
        """
        return line_list.pop(0)

    @staticmethod
    def string(line_list):
        """

        :param line_list:
        :return:
        """
        line_list.pop(0)

        str_val = ""
        while line_list and line_list[0] != '"':
            str_val += line_list.pop(0)

        if not line_list:
            print("The closing '\"' is missing!")
            raise ValueError
        else:
            line_list.pop(0)
            return f'"{str_val}"'
