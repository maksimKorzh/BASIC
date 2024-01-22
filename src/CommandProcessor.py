import os


class CommandProcessor:
    """"""
    @staticmethod
    def clear_screen():
        """

        :return:
        """
        os.system("clear")

    @staticmethod
    def list_buffer(buffer):
        """

        :param buffer:
        :return:
        """
        for line_number, line_code in sorted(buffer.items()):
            print(line_number, line_code)

    @staticmethod
    def save_file(buffer):
        """

        :param buffer:
        :return:
        """
        try:
            file_name = input("File name: ")
            with open(f"./basic-files/{file_name}", "w") as file:
                for line_number, line_code in buffer.items():
                    file.write(f"{line_number} {line_code}\n")
        except Exception as e:
            print(f'The file failed to save for the following reason: "{e}".')

    @staticmethod
    def load_file(buffer):
        """

        :param buffer:
        :return:
        """
        try:
            file_name = input("File name: ")
            with open(f"./basic-files/{file_name}") as file:
                buffer.clear()
                for file_line in file.read().split("\n"):
                    try:
                        line_number, line_code = map(str.strip, file_line.split(" ", 1))
                        buffer[int(line_number)] = line_code
                    except Exception:
                        raise Exception
        except Exception as e:
            print(f'The file failed to save for the following reason: "{e}".')
