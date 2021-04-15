from diofant import sympify, Expr
from .distribution import Distribution


class Laplace(Distribution):
    mu: Expr
    b: Expr

    def set_parameters(self, parameters):
        if len(parameters) != 2:
            raise RuntimeError("Laplace distribution requires 2 parameters")
        self.mu = sympify(parameters[0])
        self.b = sympify(parameters[1])

    def get_moment(self, k: int):
        #TODO
        pass

    def is_discrete(self):
        return False

    def subs(self, substitutions):
        self.mu = self.mu.subs(substitutions)
        self.b = self.b.subs(substitutions)

    def __str__(self):
        return f"Laplace({self.mu}, {self.b})"
