"""
Intcode computer implementation.
"""

import intcode02


class Intcode(intcode02.Intcode):
    """
    Intcode computer.
    """

    def __init__(self, mem, inp, out):
        super().__init__(mem)
        if isinstance(inp, str):
            inp = [int(v.strip()) for v in inp.split()]
        self.inp = inp
        self.out = out

    @staticmethod
    def _get_argtype(args_len, types, argi):
        """
        Return the type of argument `argi`.
        """
        fmt = f"{{types:0{args_len}d}}"
        return int(fmt.format(types=types)[args_len - argi])

    def _get_arg(self, args_len, types, p, argi):
        """
        Return argument.

        :param args_len: An `int` number of arguments.
        :param types: An `int` describing parameters (i.e., opcode without
            the last two digits.
        :param p: An `int` position of the opcode.
        :param argi: A one-based index of the argument.
        """
        value = self.mem[p + argi]
        arg_type = self._get_argtype(args_len, types, argi)
        return self.mem[value] if arg_type == 0 else value

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
        else:
            self.mem[p + argi] = value

    def op1(self, types, p):
        """
        Operator 1: addition.
        """
        result = self._get_arg(3, types, p, 1) + self._get_arg(3, types, p, 2)
        self._set_arg(3, types, p, 3, result)
        return p + 4

    def op2(self, types, p):
        """
        Operator 2: multiplication.
        """
        result = self._get_arg(3, types, p, 1) * self._get_arg(3, types, p, 2)
        self._set_arg(3, types, p, 3, result)
        return p + 4

    def op3(self, types, p):
        """
        Operator 3: read value from input.
        """
        self._set_arg(1, types, p, 1, self.inp.pop(0))
        return p + 2

    def op4(self, types, p):
        """
        Operator 4: output value to output.
        """
        self.out.append(self._get_arg(1, types, p, 1))
        return p + 2

    def op5(self, types, p):
        """
        Operator 5: jump-if-true.
        """
        value = self._get_arg(2, types, p, 1)
        return self._get_arg(2, types, p, 2) if value else p + 3

    def op6(self, types, p):
        """
        Operator 6: jump-if-false.
        """
        value = self._get_arg(2, types, p, 1)
        return p + 3 if value else self._get_arg(2, types, p, 2)

    def op7(self, types, p):
        """
        Operator 7: less than.
        """
        first = self._get_arg(3, types, p, 1)
        second = self._get_arg(3, types, p, 2)
        self._set_arg(3, types, p, 3, int(first < second))
        return p + 4

    def op8(self, types, p):
        """
        Operator 8: equals.
        """
        first = self._get_arg(3, types, p, 1)
        second = self._get_arg(3, types, p, 2)
        self._set_arg(3, types, p, 3, int(first == second))
        return p + 4

    def exec_op(self, op, p):
        """
        Execute one operator.
        """
        types = op // 100
        fun_name = f"op{op % 100}"
        try:
            fun = getattr(self, fun_name)
        except AttributeError:
            raise intcode02.InvalidProgram(
                f"invalid operator {op} at position {p}",
            )
        else:
            new_p = fun(types, p)
            return new_p if self.mem[p] == op else p
