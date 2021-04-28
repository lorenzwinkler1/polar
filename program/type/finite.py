from typing import Set
from symengine.lib.symengine_wrapper import sympify, Expr
from .type import Type


class Finite(Type):
    values: Set[Expr]

    def __init__(self, parameters, variable=None):
        if len(parameters) == 0:
            raise RuntimeError("Finite type requires >=1 parameters")
        self.values = {sympify(p) for p in parameters}
        if variable:
            self.variable = sympify(variable)

    def __str__(self):
        return f"{self.variable} : Finite({', '.join([str(v) for v in self.values])})"
