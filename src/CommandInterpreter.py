class CommandInterpreter:
    """"""
    def __init__(self, basic_interpreter, command_processor):
        """

        :param basic_interpreter:
        :param command_processor:
        """
        self.basic_interpreter = basic_interpreter
        self.command_processor = command_processor
        self.commands = {
            "clear": self.command_processor.clear_screen,
            "list": lambda: self.command_processor.list_buffer(self.basic_interpreter.buffer),
            "save": lambda: self.command_processor.save_file(self.basic_interpreter.buffer),
            "load": lambda: self.command_processor.load_file(self.basic_interpreter.buffer),
            "new": lambda: self.basic_interpreter.buffer.clear(),
            "run": self.basic_interpreter.run,
            "quit": lambda: exit(),
        }

    def interpret_command(self, user_input):
        """

        :param user_input:
        :return:
        """
        if user_input in self.commands:
            try:
                self.commands[user_input]()
            except Exception as e:
                print(f'The command failed for the following reason: "{e}".')
        else:
            try:
                line_number, line_code = map(str.strip, user_input.split(" ", 1))
                self.basic_interpreter.buffer[int(line_number)] = line_code
            except Exception:
                self.basic_interpreter.execute(0, user_input)
                raise Exception
