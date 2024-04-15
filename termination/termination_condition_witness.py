from abc import ABC, abstractmethod
from typing import List

from sympy import Poly
from sympy.core.relational import Relational


class TerminationConditionWitness(ABC):
    @abstractmethod
    def is_truth_witness(self):
        pass

    def is_false_witness(self) -> bool:
        return not self.is_termination_witness()

    @abstractmethod
    def get_interval(self) -> List[Relational | bool]:
        pass
