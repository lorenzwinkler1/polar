from abc import ABC, abstractmethod
from typing import List

from sympy import Poly
from sympy.core.relational import Relational


class TerminationWitness(ABC):
    @abstractmethod
    def is_termination_witness(self):
        pass

    def is_nontermination_witness(self):
        return not self.is_termination_witness()
