from sympy import Poly
from program.condition.condition import Condition
from termination.termination_witness import TerminationWitness


class AsymptoticTerminationWitness(TerminationWitness):
    def __init__(self, condition: Condition, polynomial: Poly) -> None:
        self.condition = condition
        self.polynomial = polynomial

    def is_termination_witness(self):
        return True

    def __str__(self) -> str:
        return f"""The condition {self.condition} eventually (asymptotically) becomes false, 
        as the coefficient of the n with the highest is negative in it's close form"""