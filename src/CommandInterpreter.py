from BasicInterpreter import BasicInterpreter
from CommandProcessor import CommandProcessor


class CommandInterpreter:
    """A class for interpreting user commands for the BasicInterpreter."""

    def __init__(
        self,
        basic_interpreter: BasicInterpreter,
        command_processor: CommandProcessor,
    ) -> None:
        """Initialize the CommandInterpreter.

        :param basic_interpreter: An instance of BasicInterpreter.
        :param command_processor: An instance of CommandProcessor.
        :return: None
        """
        self.basic_interpreter = basic_interpreter
        """Contains an instance of BasicInterpreter."""

        self.command_processor = command_processor
        """Contains an instance of CommandProcessor."""

        self.commands = {
            "clear": self.command_processor.clear_screen,
            "list": lambda: self.command_processor.list_buffer(
                self.basic_interpreter.buffer
            ),
            "save": lambda: self.command_processor.save_file(
                self.basic_interpreter.buffer
            ),
            "load": lambda: self.command_processor.load_file(
                self.basic_interpreter.buffer
            ),
            "new": self.basic_interpreter.buffer.clear,
            "run": self.basic_interpreter.run,
            "quit": exit,
        }
        """Maps the commands to their corresponding functions."""

    def interpret_command(self, user_input: str) -> None:
        """Interpret a user command.

        :param user_input: The user input to interpret.
        :return: None
        """
        try:
            if user_input in self.commands:
                self.execute_command(user_input)
            else:
                self.process_basic_code(user_input)
        except Exception as e:
            print(f'The command failed for the following reason: "{e}".')

    def execute_command(self, command: str) -> None:
        """Execute a predefined command.

        :param command: The command to execute.
        :return: None
        """
        command_function = self.commands.get(command)
        if command_function:
            command_function()

    def process_basic_code(self, user_input: str) -> None:
        """Treat user input as BASIC code and store it in the buffer.

        :param user_input: The user input to store in the buffer.
        :return: None
        """
        try:
            line_number, line_code = map(str.strip, user_input.split(" ", 1))
            self.basic_interpreter.buffer[int(line_number)] = line_code
        except Exception as e:
            print(f'Error processing BASIC code: "{e}".')
