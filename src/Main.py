from BasicInterpreter import BasicInterpreter
from CommandInterpreter import CommandInterpreter
from CommandProcessor import CommandProcessor


def main() -> None:
    """Main function for the interactive interpreter.

    Creates instances of BasicInterpreter, CommandProcessor, and
    CommandInterpreter to interpret user commands and BASIC code.

    :return: None
    """
    basic_interpreter = BasicInterpreter()
    command_processor = CommandProcessor()
    command_interpreter = CommandInterpreter(
        basic_interpreter,
        command_processor,
    )

    try:
        # Continuously takes inputs from the user and interprets them
        while True:
            user_input = input("> ")
            command_interpreter.interpret_command(user_input)
    except KeyboardInterrupt:
        print("\nExiting the interpreter.")


if __name__ == "__main__":
    main()
