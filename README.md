# BASIC Interpreter

BASIC Interpreter offers an interactive platform for users to input commands and BASIC code. This project draws
inspiration from
[this tutorial series](https://www.youtube.com/watch?v=hK2OxjhH3dw&list=PLLfIBXQeu3aaEgJeLEcVXP6TNOCifY1CM), with
substantial modifications to introduce object-oriented concepts.

## Installation

To begin, clone this repository, and navigate to the `src` directory:

```bash
$ git clone https://github.com/JayBhatt2021/basic-interpreter.git
$ cd basic-interpreter/src/
```

## Usage

Launch the interpreter with the following command:

```bash
$ python3 Main.py
```

Now, you can input BASIC code like the example below, *or*...

```bash
$ 10 LET a = 3
```

...utilize the following commands:

| **Command** |                **Explanation**               |
|:-----------:|:--------------------------------------------:|
|    clear    |          Clears the terminal screen.         |
|     list    |       Lists the contents of the buffer.      |
|     save    |          Saves the buffer to a file.         |
|     load    |         Loads a file into the buffer.        |
|     new     |              Clears the buffer.              |
|     run     | Runs the BASIC program stored in the buffer. |
|     quit    |        Exits the interpreter terminal.       |
