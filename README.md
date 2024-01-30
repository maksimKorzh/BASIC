# BASIC Interpreter

BASIC Interpreter provides an interactive interpreter for processing commands and BASIC code entered by the user. The
project is inspired by the tutorial series available
[here](https://www.youtube.com/watch?v=hK2OxjhH3dw&list=PLLfIBXQeu3aaEgJeLEcVXP6TNOCifY1CM), with the code heavily
modified to incorporate object-oriented concepts.

## Installation

To get started, clone this repository and navigate to the `src` directory:

```bash
$ git clone https://github.com/JayBhatt2021/basic-interpreter.git
$ cd basic-interpreter/src/
```

## Usage

Launch the interpreter with the following command:

```bash
$ python3 Main.py
```

Now, you can input BASIC code like the following, *or*...

```bash
$ 10 LET a = 3
```

...use the following commands:

| **Command** |                 **Explanation**                 |
|:-----------:|:-----------------------------------------------:|
|    clear    |          It clears the terminal screen.         |
|     list    |       It lists the contents of the buffer.      |
|     save    |          It saves the buffer to a file.         |
|     load    |         It loads a file into the buffer.        |
|     new     |              It clears the buffer.              |
|     run     | It runs the BASIC program stored in the buffer. |
|     quit    |        It exits the interpreter terminal.       |
