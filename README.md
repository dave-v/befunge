# Befunge

[Befunge](https://esolangs.org/wiki/Befunge) is an esoteric programming
language in which a program is a 2-dimensional grid of cells with
instructions on them. The instruction pointer may traverse the cells in
the four cardinal directions, executing the instructions contained within
the cells as they are read. The central memory structure of the language
is a stack which most operations either push to or pop from. The language
is also self-modifying, in that there exist instructions to read and write
the program's source while it is running (this allows for using cells as
an alternative to the stack for storage).

This version should be Turing-complete.
The playfield is unbounded (until you run out of memory anyway).
Rather than ASCII values, the cells are represented as Python integers
which have arbitrary precision, so there is (basically) no limitation on
values that cells can hold.

## Usage

Given a file called `{filename}` containing a Befunge program:

```shell
python befunge.py {filename}
```

Whenever the interpreter requires user input, it will prompt you.
Enter EOF (usually CTRL+D) to register a value of -1, which can be
used to exit otherwise infinite input loops.

Alternatively, you can supply an input file that will provide the
inputs automatically until the end of the file, at which point it
switches back to prompting for user input. (This doesn't work so well
for integer inputs as it only looks one character at a time so can't
handle integers with more than one digit.)

```shell
python befunge.py {filename} --input {input-filename}
```

## Example programs

Some example Befunge programs are included.

Some highlights are described here.

### `selfinterpreter.bf`

This is a Befunge interpreter written in Befunge. It works be exploiting
the self-modifying nature of Befunge to write the input into its own
source code and then directing the instruction pointer into the newly
written block. The interpreter code and the location it writes the input
to are diagonally connected such that the input program can never get
back into the interpreter block.

It can be run with another example program like so:

```shell
python befunge.py selfinterpreter.bf --input factorial.bf
```

This sneaky self-interpreter does have a flaw... because the input
program is offset from the top-left cell, the `g` and `p` commands will
not be referencing the right cells, which could break the program (but
is often fine).

### `brainfuck.bf`

This is a [brainfuck](https://esolangs.org/wiki/Brainfuck) interpreter
written in Befunge. It will (hopefully) report errors such as unbalanced
brackets.

It can be run like so:

```shell
python befunge.py brainfuck.bf --input helloworld.fk
```

(You can run it without an input file if you are feeling masochistic and
want to enter each character one-by-one at the prompt.)

Devastatingly, the aforementioned limitation with the `g` and `p`
instructions that the self-interpreter has prevents you from running the
brainfuck interpreter through the self-interpreter and manually entering
a brainfuck program like so:

```shell
python befunge.py selfinterpreter.bf --input brainfuck.bf
```

This is because the brainfuck interpreter works by looking at specific
cells to check the instruction characters, and also uses cells that
overlap with the self-interpreter cells to represent the tape, so it
starts out with non-zero initial values.
