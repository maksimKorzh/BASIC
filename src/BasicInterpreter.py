from typing import Dict, List


class BasicInterpreter:
    """A simple interpreter class for the BASIC programming language."""

    def __init__(self):
        """Initialize the BasicInterpreter."""
        self.token: str = ""
        """Represents the current token."""

        self.line_number: int = 0
        """Represents the current line number of the BASIC program."""

        self.goto: bool = False
        """Determines if a GOTO statement has been reached."""

        self.variables: Dict[str, int] = {}
        """Stores variable names and their corresponding integer values."""

        self.buffer: Dict[int, str] = {}
        """Stores the BASIC program's lines numbers and their corresponding
        source code.
        """

    def run(self) -> None:
        """Run the BASIC program.

        :return: None
        """
        # Initializes the line_iterator and goto flag
        line_iterator = iter(self.buffer)
        self.goto = False

        while True:
            try:
                if self.goto:
                    # Resets the goto flag
                    self.goto = False

                    # Obtains the current iterator and line
                    current_iterator = iter(self.buffer)
                    current_line = next(current_iterator)

                    # Navigates to the BASIC line specified by the GOTO
                    # statement
                    while current_line != self.line_number:
                        current_line = next(current_iterator)

                    # Sets line_iterator to current_iterator
                    line_iterator = current_iterator
                else:
                    # Sets line_number to the sequentially-next line number
                    self.line_number = next(line_iterator)

                # Obtains the BASIC line specified by its line number and
                # executes it
                line_str = self.buffer.get(self.line_number, "")
                self.execute(line_str)
            except StopIteration:
                break

    def execute(self, line_str: str) -> None:
        """Execute a line of BASIC code.

        :param line_str: A BASIC file line.
        :return: None
        """
        try:
            # Converts line_str to List[str]
            line_list = list(line_str)

            # Obtains the current token
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
            print(f'Execution failed on line {self.line_number}: "{e}".')

    def print_statement(self, line_list: List[str]) -> None:
        """Handle a PRINT statement.

        :param line_list: A BASIC file line as a list of characters.
        :return: None
        """
        line_list = list("".join(line_list).strip())

        # Obtains the current token
        self.scan(line_list)

        # Truncates the first argument and stores the remaining args
        remaining_args = list(",".join("".join(line_list).split(",")[1:]))

        if isinstance(self.token, str) and self.token[0] == '"':
            # Prints the characters in between the quotes
            print(self.token[1:-1], end="")

            # Obtains the current token
            self.scan(line_list)
        else:
            line_list = list("".join(line_list).replace(" ", ""))

            # Prints the calculated result of the expression(s)
            print(self.calculate(line_list), end="")

        # Continues to print the remaining args if the current token is a comma
        self.print_statement(remaining_args) if self.token == "," else print()

    def let_statement(self, line_list: List[str]) -> None:
        """Handle a LET statement.

        :param line_list: A BASIC file line as a list of characters.
        :return: None
        """
        line_str = "".join(line_list).replace(" ", "")

        if "=" not in line_str:
            print('Missing "=" in variable definition!')
            raise ValueError('Missing "=" in variable definition!')

        # Obtains the variable name and value
        name, val = map(str.strip, line_str.split("="))

        if not val:
            print("Missing variable value!")
            raise ValueError("Missing variable value!")
        elif val == "INPUT":
            try:
                # Stores the inputted variable name and value
                self.variables[name] = int(input())
            except ValueError:
                print("Input must be an integer!")
                raise ValueError("Input must be an integer!")
        else:
            val_list = list(val)

            # Obtains the current token
            self.scan(val_list)

            # Stores the variable name and its calculated value
            self.variables[name] = self.calculate(val_list)

    def if_statement(self, line_list: List[str]) -> None:
        """Handle an IF statement.

        :param line_list: A BASIC file line as a list of characters.
        :return: None
        """
        # Obtains the conditional and then clauses
        parts = "".join(line_list).split("THEN")

        if len(parts) != 2:
            print('Missing "THEN" after condition!')
            raise ValueError('Missing "THEN" after condition!')

        conditional_clause = list("".join(parts[0]).replace(" ", ""))
        then_clause = list("".join(parts[1].strip()))

        # Combines the conditional_clause and then_clause lists
        line_list = conditional_clause + then_clause

        # Gets the current token and evaluates the left conditional expression
        self.scan(line_list)
        left_expression = self.calculate(line_list)

        # Gets the operator and current token
        operator = self.token
        self.scan(line_list)

        # Evaluates the right conditional expression and gets the current token
        right_expression = self.calculate(line_list)
        self.scan(line_list)

        # Evaluates the entire conditional clause
        condition = False
        if operator == ">":
            condition = left_expression > right_expression
        elif operator == "<":
            condition = left_expression < right_expression
        elif operator == "=":
            condition = left_expression == right_expression

        # Executes the current BASIC line from the above condition
        if condition:
            self.execute(f'{self.token} {"".join(line_list)}')

    def goto_statement(self, line_list: List[str]) -> None:
        """Handle a GOTO statement.

        :param line_list: A BASIC file line as a list of characters.
        :return: None
        """
        line_list = list("".join(line_list).replace(" ", ""))

        # Obtains the current token and line number
        self.scan(line_list)
        self.line_number = self.calculate(line_list)

        # Sets the goto flag to True
        self.goto = True

    def calculate(self, line_list: List[str]) -> int:
        """Evaluate mathematical expressions.

        :param line_list: A BASIC file line as a list of characters.
        :return: The integer representation of the evaluated expression(s).
        """
        try:
            # Calculates the result of the expression(s)
            result = self.expression(line_list)

            if result is None:
                print("Invalid expression!")
            else:
                return result
        except Exception as e:
            print(f'Calculation failed: "{e}".')

    def expression(self, line_list: List[str]) -> int | None:
        """Handle mathematical expressions.

        :param line_list: A BASIC file line as a list of characters.
        :return: The integer representation of the expression or None.
        """
        # Evaluates the first term in this expression
        a = self.term(line_list)

        while True:
            if self.token == "+":
                # Obtains the current token
                self.scan(line_list)

                # Evaluates the next term in this expression
                b = self.term(line_list)

                # Obtains the sum of the terms
                a += b
            elif self.token == "-":
                # Obtains the current token
                self.scan(line_list)

                # Evaluates the next term in this expression
                b = self.term(line_list)

                # Obtains the difference of the terms
                a -= b
            else:
                # Returns the integer representation of the expression or None
                return a

    def term(self, line_list: List[str]) -> int | None:
        """Handle term operations.

        :param line_list: A BASIC file line as a list of characters.
        :return: The integer representation of the term or None.
        """
        # Evaluates the first factor in this term
        a = self.factor(line_list)

        while True:
            # Obtains the current token
            self.scan(line_list)

            if self.token == "*":
                # Obtains the current token
                self.scan(line_list)

                # Evaluates the next factor in this term
                b = self.factor(line_list)

                # Obtains the product of the factors
                a *= b
            elif self.token == "/":
                # Obtains the current token
                self.scan(line_list)

                # Evaluates the next factor in this term
                b = self.factor(line_list)

                # Obtains the integer quotient of the factors
                a = int(a / b)
            else:
                # Returns the integer representation of the term or None
                return a

    def factor(self, line_list: List[str]) -> int | None:
        """Handle factors in expressions.

        :param line_list: A BASIC file line as a list of characters.
        :return: The integer representation of the factor or None.
        """
        if isinstance(self.token, int):
            return self.token

        if self.token == "(":
            # Obtains the current token
            self.scan(line_list)

            # Evaluates the expression between the parentheses
            a = self.expression(line_list)

            # Returns the evaluated expression or None
            if a is None:
                return None
            elif self.token == ")":
                return a
            else:
                return None
        elif self.token == "-":
            # Obtains the current token
            self.scan(line_list)

            # Returns the negated factor
            return -self.factor(line_list)
        else:
            return None

    def scan(self, line_list: List[str]) -> None:
        """Tokenize a portion of the input line according to its syntax.

        :param line_list: A BASIC file line as a list of characters.
        :return: None
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
    def number(line_list: List[str]) -> int:
        """Resolve the token as a number.

        :param line_list: A BASIC file line as a list of characters.
        :return: A BASIC integer.
        """
        # Builds the BASIC integer to be returned
        num_str = ""
        while line_list and line_list[0].isdigit():
            num_str += line_list.pop(0)

        return int(num_str)

    def variable(self, line_list: List[str]) -> int:
        """Resolve the token as a variable.

        :param line_list: A BASIC file line as a list of characters.
        :return: The integer value of a BASIC variable.
        """
        # Builds the name of the BASIC variable
        var_name = ""
        while line_list and line_list[0].islower():
            var_name += line_list.pop(0)

        if var_name not in self.variables:
            print(f'Variable "{var_name}" is not defined!')

        try:
            # Returns the corresponding integer value from the variable's name
            return int(self.variables[var_name])
        except KeyError:
            raise KeyError(f'Variable "{var_name}" is not defined!')

    @staticmethod
    def statement(line_list: List[str]) -> str:
        """Resolve the token as a keyword.

        :param line_list: A BASIC file line as a list of characters.
        :return: A BASIC keyword.
        """
        # Builds the BASIC keyword to be returned
        keyword = ""
        while line_list and line_list[0].isupper():
            keyword += line_list.pop(0)

        if keyword not in ["PRINT", "LET", "IF", "THEN", "GOTO"]:
            print(f'Unknown keyword "{keyword}"!')
            raise ValueError(f'Unknown keyword "{keyword}"!')
        else:
            return keyword

    @staticmethod
    def operator(line_list: List[str]) -> str:
        """Resolve the token as an operator.

        :param line_list: A BASIC file line as a list of characters.
        :return: A BASIC operator.
        """
        return line_list.pop(0)

    @staticmethod
    def string(line_list: List[str]) -> str:
        """Resolve the token as a string.

        :param line_list: A BASIC file line as a list of characters.
        :return: A BASIC string.
        """
        # Removes the opening quote from line_list
        line_list.pop(0)

        # Builds the BASIC string to be returned
        str_val = ""
        while line_list and line_list[0] != '"':
            str_val += line_list.pop(0)

        if not line_list:
            # Notifies the user of the missing closing quote
            print('Missing closing quote (")!')
            raise ValueError('Missing closing quote (")!')
        else:
            # Removes the closing quote from line_list
            line_list.pop(0)

            # Returns the entire BASIC string
            return f'"{str_val}"'
