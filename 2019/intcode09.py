"""
Intcode computer implementation.
"""

import intcode07
from intcode07 import MissingInputError  # noqa


class Intcode(intcode07.Intcode):
    """
    Intcode computer.
    """

    def __init__(self, mem, inp, out):
        super().__init__(mem, inp, out)
        self.mem = dict(enumerate(mem))
        self.relative_base = 0

    def _get_arg(self, args_len, types, p, argi):
        """
        Return argument.

        :param args_len: An `int` number of arguments.
        :param types: An `int` describing parameters (i.e., opcode without
            the last two digits.
        :param p: An `int` position of the opcode.
        :param argi: A one-based index of the argument.
        """
        value = self.mem.get(p + argi, 0)
        arg_type = self._get_argtype(args_len, types, argi)
        if arg_type == 0:
            return self.mem.get(value, 0)
        elif arg_type == 1:
            return value
        elif arg_type == 2:
            return self.mem.get(self.relative_base + value, 0)
        else:
            raise ValueError("invalid type {arg_type}")

    def _set_arg(self, args_len, types, p, argi, value):
        """
        Set value of an argument.

        :param args_len: An `int` number of arguments.
        :param types: An `int` describing parameters (i.e., opcode without
            the last two digits.
        :param p: An `int` position of the opcode.
        :param argi: A one-based index of the argument.
        """
        arg_type = self._get_argtype(args_len, types, argi)
        if arg_type == 0:
            self.mem[self.mem[p + argi]] = value
        elif arg_type == 1:
            self.mem[p + argi] = value
        elif arg_type == 2:
            self.mem[self.relative_base + self.mem[p + argi]] = value
        else:
            raise ValueError("invalid type {arg_type}")

    def op9(self, types, p):
        """
        Operator 9: adjust the relative base.
        """
        self.relative_base += self._get_arg(1, types, p, 1)
        return p + 2
