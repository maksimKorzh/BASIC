import BasicInterpreter
import CommandProcessor
import CommandInterpreter


def main():
    basic_interpreter = BasicInterpreter()
    command_processor = CommandProcessor()
    command_interpreter = CommandInterpreter(basic_interpreter, command_processor)

    while True:
        user_input = input("> ")
        command_interpreter.process_command(user_input)


if __name__ == "__main__":
    main()
