import os
from typing import Dict


class CommandProcessor:
    """
    A class for processing commands related to the BasicInterpreter buffer.
    """

    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen.

        :return: None
        """
        os.system("clear")

    @staticmethod
    def list_buffer(buffer: Dict[int, str]) -> None:
        """List the contents of the buffer.

        :param buffer: The buffer to list.
        :return: None
        """
        for line_number, line_code in sorted(buffer.items()):
            print(line_number, line_code)

    @staticmethod
    def save_file(buffer: Dict[int, str]) -> None:
        """Save the buffer to a file.

        :param buffer: The buffer to save.
        :return: None
        """
        try:
            file_name = input("File name: ")
            file_path = f"./basic-files/{file_name}"
            with open(file_path, "w") as file:
                for line_number, line_code in buffer.items():
                    file.write(f"{line_number} {line_code}\n")
            print(f'Buffer saved to "{file_path}".')
        except Exception as e:
            print(f'Failed to save file: "{e}".')

    @staticmethod
    def load_file(buffer: Dict[int, str]) -> None:
        """Load a file into the buffer.

        :param buffer: The buffer to load the file into.
        :return: None
        """
        try:
            file_name = input("File name: ")
            file_path = f"./basic-files/{file_name}"
            with open(file_path) as file:
                buffer.clear()
                for file_line in file.read().split("\n"):
                    try:
                        line_number, line_code = map(
                            str.strip,
                            file_line.split(" ", 1),
                        )
                        buffer[int(line_number)] = line_code
                    except Exception:
                        raise Exception
            print(f'File "{file_name}" loaded into the buffer.')
        except Exception as e:
            print(f'Failed to load file: "{e}".')
