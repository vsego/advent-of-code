"""
Intcode computer implementation.
"""


class InvalidProgram(Exception):
    """
    Exception raised when an invalid program is ran.
    """


class Intcode:
    """
    Intcode computer.
    """

    def __init__(self, mem):
        self.mem = mem[:]
        self.p = 0

    def op1(self, p):
        """
        Operator 1: addition.
        """
        mem = self.mem
        mem[mem[p + 3]] = mem[mem[p + 1]] + mem[mem[p + 2]]
        return p + 4

    def op2(self, p):
        """
        Operator 2: multiplication.
        """
        mem = self.mem
        mem[mem[p + 3]] = mem[mem[p + 1]] * mem[mem[p + 2]]
        return p + 4

    def exec_op(self, op, p):
        """
        Execute one operator.
        """
        try:
            fun = getattr(self, f"op{op}")
        except AttributeError:
            raise InvalidProgram(f"invalid operator {op} at position {p}")
        else:
            return fun(p)

    def run(self):
        """
        Run the progrom.
        """
        while True:
            try:
                op = self.mem[self.p]
            except IndexError:
                raise InvalidProgram(
                    f"program not properly terminated at position {self.p}",
                )
            if op == 99:
                return
            self.p = self.exec_op(op, self.p)
