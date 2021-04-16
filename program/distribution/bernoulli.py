from diofant import sympify, Expr
from .distribution import Distribution
from program.type import Finite


class Bernoulli(Distribution):
    p: Expr

    def set_parameters(self, parameters):
        if len(parameters) != 1:
            raise RuntimeError("Bernoulli distribution requires 1 parameter")
        self.p = sympify(parameters[0])

    def get_moment(self, k: int):
        #TODO
        pass

    def get_type(self) -> Finite:
        return Finite([0, 1])

    def is_discrete(self):
        return True

    def subs(self, substitutions):
        self.p = self.p.subs(substitutions)

    def __str__(self):
        return f"Bernoulli({self.p})"
