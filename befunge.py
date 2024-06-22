import argparse
import random


class Interpreter:
    class End(Exception):
        pass

    def __init__(self, filename, input_source: "Input"):
        self.input_source = input_source
        self.stack = []
        self.ip = (0, 0)
        self.delta = (1, 0)
        self.dim = (0, 0)
        self.string_mode = False

        with open(filename) as f:
            self.cells = [list(map(ord, line.rstrip("\n"))) for line in f.readlines()]
        self.reformat_cells(max(map(len, self.cells)), len(self.cells))

    def parse(self):
        while True:
            x, y = self.ip
            cell = self.cells[y][x]
            try:
                self.parse_symbol(chr(cell))
            except SyntaxError:
                # Command not found
                return
            except ValueError:
                # Couldn't convert symbol to char
                return
            except self.End:
                return
            self.update_ip()

    def parse_symbol(self, symbol):
        if symbol == "@":
            raise self.End
        if symbol == '"':
            self.str_mode()
        elif self.string_mode:
            self.push(ord(symbol))
        elif symbol in "0123456789":
            self.push(int(symbol))
        elif symbol.isspace():
            pass
        else:
            command = self.get_command(symbol)
            if command is None:
                raise SyntaxError
            command()

    def get_command(self, symbol):
        return {
            ">": self.mv_right,
            "v": self.mv_down,
            "<": self.mv_left,
            "^": self.mv_up,
            "?": self.mv_rand,
            ".": self.out_int,
            ",": self.out_char,
            "&": self.in_int,
            "~": self.in_char,
            "+": self.op_add,
            "-": self.op_sub,
            "*": self.op_mult,
            "/": self.op_div,
            "%": self.op_mod,
            "`": self.op_gt,
            "!": self.op_not,
            "_": self.if_hor,
            "|": self.if_ver,
            ":": self.stk_dup,
            "\\": self.stk_swap,
            "$": self.stk_pop,
            '"': self.str_mode,
            "#": self.bridge,
            "g": self.code_get,
            "p": self.code_put,
        }.get(symbol)

    def update_ip(self):
        self.ip = (
            (self.ip[0] + self.delta[0]) % len(self.cells[0]),
            (self.ip[1] + self.delta[1]) % len(self.cells),
        )

    def push(self, v):
        self.stack.append(v)

    def pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            return 0

    def reformat_cells(self, x, y):
        self.dim = (x, y)
        self.cells.extend([[]] * (y - len(self.cells)))
        for row in self.cells:
            row.extend([ord(" ")] * (x - len(row)))

    # Commands

    def mv_right(self):
        self.delta = (1, 0)

    def mv_down(self):
        self.delta = (0, 1)

    def mv_left(self):
        self.delta = (-1, 0)

    def mv_up(self):
        self.delta = (0, -1)

    def mv_rand(self):
        random.choice((self.mv_right, self.mv_down, self.mv_left, self.mv_up))()

    def out_int(self):
        print(self.pop())

    def out_char(self):
        try:
            print(chr(self.pop()), end="")
        except ValueError:
            # Out of range
            print(0)

    def in_int(self):
        try:
            self.push(self.input_source.get_next_int())
        except ValueError:
            self.push(0)
        except EOFError:
            self.push(-1)

    def in_char(self):
        try:
            self.push(ord(self.input_source.get_next_char()))
        except EOFError:
            self.push(-1)

    def op_add(self):
        self.push(self.pop() + self.pop())

    def op_sub(self):
        self.push(-self.pop() + self.pop())

    def op_mult(self):
        self.push(self.pop() * self.pop())

    def op_div(self):
        x = self.pop()
        y = self.pop()
        try:
            self.push(y / x)
        except ZeroDivisionError:
            self.push(0)

    def op_mod(self):
        x = self.pop()
        y = self.pop()
        try:
            self.push(y % x)
        except ZeroDivisionError:
            self.push(0)

    def op_gt(self):
        self.push(int(self.pop() < self.pop()))

    def op_not(self):
        self.push(int(not self.pop()))

    def if_hor(self):
        if self.pop():
            self.mv_left()
        else:
            self.mv_right()

    def if_ver(self):
        if self.pop():
            self.mv_up()
        else:
            self.mv_down()

    def stk_dup(self):
        v = self.pop()
        self.push(v)
        self.push(v)

    def stk_swap(self):
        a = self.pop()
        b = self.pop()
        self.push(a)
        self.push(b)

    def stk_pop(self):
        self.pop()

    def str_mode(self):
        self.string_mode = not self.string_mode

    def bridge(self):
        self.update_ip()

    def code_get(self):
        y = self.pop()
        x = self.pop()
        try:
            self.push(self.cells[y][x])
        except IndexError:
            self.push(0)

    def code_put(self):
        y = self.pop()
        x = self.pop()
        v = self.pop()
        try:
            self.cells[y][x] = v
        except IndexError:
            if x < 0 or y < 0:
                return
            self.reformat_cells(max(self.dim[0], x + 1), max(self.dim[1], y + 1))
            self.cells[y][x] = v


class Input:
    def get_next_char(self) -> str:
        pass

    def get_next_int(self) -> int:
        pass


class UserInput(Input):
    def get_next_char(self) -> str:
        return (input("char: ") or "\n")[0]

    def get_next_int(self) -> int:
        return int(input("int: "))


class FileInput(Input):
    def __init__(self, file):
        self.file = file
        self.done = False
        self.user_input = UserInput()

    def get_next_char(self) -> str:
        if self.done:
            return self.user_input.get_next_char()
        char = self.file.read(1)
        if char != "":
            return char
        self.done = True
        raise EOFError

    def get_next_int(self) -> int:
        if self.done:
            return self.user_input.get_next_int()
        return int(self.get_next_char())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=False)
    parser.add_argument("program")
    args = parser.parse_args()
    if args.input is not None:
        input_source = FileInput(open(args.input))
    else:
        input_source = UserInput()
    Interpreter(args.program, input_source).parse()


if __name__ == "__main__":
    main()
