from typing import Dict, List


class BasicInterpreter:
    """A simple interpreter class for the BASIC programming language."""

    def __init__(self) -> None:
        """Initialize the BasicInterpreter.

        :return: None
        """
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
        self.goto = False

        # Constructs an iterator for buffer's keys (line numbers)
        line_num_iterator = iter(self.buffer)

        while True:
            try:
                if self.goto:
                    # Resets goto and line_num_iterator to their initial values
                    self.goto = False
                    line_num_iterator = iter(self.buffer)

                    # Go to the BASIC line specified by the GOTO statement
                    while next(line_num_iterator) != self.line_number:
                        pass
                else:
                    self.line_number = next(line_num_iterator)

                # Executes the BASIC line specified by its line number
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
            line_list = list(line_str)

            # Sets the token to a BASIC keyword
            self.scan(line_list)

            # Executes the appropriate BASIC statement
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

        # Sets the token to the first print arg
        self.scan(line_list)

        # Truncates the first print arg and stores the remaining print args
        remaining_args = list(",".join("".join(line_list).split(",")[1:]))

        if isinstance(self.token, str) and self.token[0] == '"':
            # Prints the characters between the quotes
            print(self.token[1:-1], end="")

            # Sets the token to a comma if there are multiple print args
            self.scan(line_list)
        else:
            line_list = list("".join(line_list).replace(" ", ""))

            # Prints the calculated result of the expression
            print(self.calculate(line_list), end="")

        # Continues to print the remaining args
        self.print_statement(remaining_args) if self.token == "," else print()

    def let_statement(self, line_list: List[str]) -> None:
        """Handle a LET statement.

        :param line_list: A BASIC file line as a list of characters.
        :return: None
        """
        line_str = "".join(line_list).replace(" ", "")

        # Checks if "=" is missing in the variable definition
        if "=" not in line_str:
            raise ValueError('Missing "=" in variable definition!')

        # Obtains the variable name and value
        name, val = map(str.strip, line_str.split("="))

        # Checks if the variable value is missing
        if not val:
            raise ValueError("Missing variable value!")

        if val == "INPUT":
            try:
                # Stores the inputted variable name and value
                self.variables[name] = int(input())
            except ValueError:
                raise ValueError("Input must be an integer!")
        else:
            val_list = list(val)

            # Sets the token to the first value of the expression
            self.scan(val_list)

            # Stores the variable name and its calculated value
            self.variables[name] = self.calculate(val_list)

    def if_statement(self, line_list: List[str]) -> None:
        """Handle an IF statement.

        :param line_list: A BASIC file line as a list of characters.
        :return: None
        """
        # Extracts the conditional and then clauses
        parts = "".join(line_list).split("THEN")

        if len(parts) != 2:
            raise ValueError('Missing "THEN" after condition!')

        # Processes the conditional and then clauses
        conditional_clause = list("".join(parts[0]).replace(" ", ""))
        then_clause = list("".join(parts[1].strip()))
        line_list = conditional_clause + then_clause

        # Sets the token to the first value of the left conditional operand
        self.scan(line_list)

        # Evaluates the left conditional operand
        left_operand = self.calculate(line_list)

        # Gets the comparison operator from the token
        operator = self.token

        # Sets the token to the first value of the right conditional operand
        self.scan(line_list)

        # Evaluates the right conditional operand
        right_operand = self.calculate(line_list)

        # Advances the token to the first value in the THEN clause
        self.scan(line_list)

        # Evaluates the entire conditional clause
        condition = self.evaluate_condition(
            left_operand,
            operator,
            right_operand,
        )

        # Executes the THEN clause if the condition is true
        if condition:
            self.execute(f'{self.token} {"".join(line_list)}')

    @staticmethod
    def evaluate_condition(
        left_operand: int, operator: str, right_operand: int
    ) -> bool:
        """Evaluate a conditional expression.

        :param left_operand: The left operand.
        :param operator: The comparison operator.
        :param right_operand: The right operand.
        :return: The result of the condition.
        """
        if operator == ">":
            return left_operand > right_operand
        elif operator == "<":
            return left_operand < right_operand
        elif operator == "=":
            return left_operand == right_operand
        else:
            raise ValueError(f'Invalid comparison operator: "{operator}".')

    def goto_statement(self, line_list: List[str]) -> None:
        """Handle a GOTO statement.

        :param line_list: A BASIC file line as a list of characters.
        :return: None
        """
        # Extracts the line number from the GOTO statement
        line_list = list("".join(line_list).replace(" ", ""))
        self.scan(line_list)
        target_line_number = self.calculate(line_list)

        # Updates the line number and sets the goto flag
        self.line_number = target_line_number
        self.goto = True

    def calculate(self, line_list: List[str]) -> int:
        """Evaluate a mathematical expression.

        :param line_list: A BASIC file line as a list of characters.
        :return: The integer representation of the evaluated expression.
        """
        try:
            result = self.expression(line_list)

            if result is None:
                print("Invalid expression!")
            else:
                return result
        except Exception as e:
            print(f'Calculation failed: "{e}".')

    def expression(self, line_list: List[str]) -> int | None:
        """Handle a mathematical expression.

        :param line_list: A BASIC file line as a list of characters.
        :return: The integer representation of the expression or None.
        """
        # Evaluates the first term in the expression
        a = self.term(line_list)

        # Continues evaluating terms as long as the token is "+" or "-"
        while self.token in ["+", "-"]:
            # Gets the plus/minus operator from the token
            operator = self.token

            # Sets the token to the next term in the expression
            self.scan(line_list)

            # Evaluates the next term in the expression
            b = self.term(line_list)

            # Updates the result based on the operator
            if operator == "+":
                a += b
            elif operator == "-":
                a -= b

        return a

    def term(self, line_list: List[str]) -> int | None:
        """Handle term operations.

        :param line_list: A BASIC file line as a list of characters.
        :return: The integer representation of the term or None.
        """
        # Evaluates the first factor in the term
        a = self.factor(line_list)

        # Moves to the next token
        self.scan(line_list)

        # Continues evaluating factors as long as the token is "*" or "/"
        while self.token in ["*", "/"]:
            # Gets the multiplication/division operator from the token
            operator = self.token

            # Sets the token to the next factor in the term
            self.scan(line_list)

            # Evaluates the next factor in the term
            b = self.factor(line_list)

            # Updates the result based on the operator
            if operator == "*":
                a *= b
            elif operator == "/":
                a = int(a / b)

        return a

    def factor(self, line_list: List[str]) -> int | None:
        """Handle factors in an expression.

        :param line_list: A BASIC file line as a list of characters.
        :return: The integer representation of the factor or None.
        """
        if isinstance(self.token, int):
            return self.token

        if self.token == "(":
            # Sets the token to the first value of the factor expression
            self.scan(line_list)

            # Evaluates the factor expression between the parentheses
            factor_expression = self.expression(line_list)

            # Returns the evaluated expression or None if not properly closed
            return factor_expression if self.token == ")" else None

        if self.token == "-":
            # Sets the token to the first value of the factor expression
            self.scan(line_list)

            # Returns the negated factor expression
            return -self.factor(line_list)

        # Returns None if the token is not recognized as a factor
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
