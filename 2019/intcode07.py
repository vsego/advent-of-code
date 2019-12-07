"""
Intcode computer implementation.
"""

import intcode05


class MissingInputError(Exception):
    """
    Exception to raise when attempting to read from empty input.
    """


class Intcode(intcode05.Intcode):
    """
    Intcode computer.
    """

    def op3(self, types, p):
        """
        Operator 3: read value from input.
        """
        try:
            self._set_arg(1, types, p, 1, self.inp.pop(0))
        except IndexError:
            raise MissingInputError("input is empty")
        return p + 2
