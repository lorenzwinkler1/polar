from typing import List, Optional
from sympy.core.relational import Relational
from program.condition.condition import Condition
from termination.termination_witness import TerminationWitness


class ExactWitness(TerminationWitness):
    def __init__(self, condition: Condition, zeros: List[float], first_false_integer: Optional[int]) -> None:
        super().__init__()
        self.condition = condition
        self.zeros = zeros
        self.first_false_integer = first_false_integer

    def is_termination_witness(self):
        return self.first_false_integer is not None
    
    def __str__(self) -> str:
        if self.is_termination_witness():
            return f"The condition {self.condition} was found to be false for the loop iteration {self.first_false_integer}.\nIt's zeros are: {self.zeros}"
    
    