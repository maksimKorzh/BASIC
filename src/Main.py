from BasicInterpreter import BasicInterpreter
from CommandInterpreter import CommandInterpreter
from CommandProcessor import CommandProcessor


def main() -> None:
    """Represent the main function of the application.

    :return: None.
    """
    basic_interpreter = BasicInterpreter()
    command_processor = CommandProcessor()
    command_interpreter = CommandInterpreter(
        basic_interpreter,
        command_processor,
    )

    # Continuously takes in inputs from the user and interprets them
    while True:
        user_input = input("> ")
        command_interpreter.interpret_command(user_input)


if __name__ == "__main__":
    main()
