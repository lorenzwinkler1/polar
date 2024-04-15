from typing import List
from sympy.core.relational import Relational
from termination.termination_condition_witness import TerminationConditionWitness


class TrivialWitness(TerminationConditionWitness):
    def __init__(self, truth_witness: bool, always_satisfies: bool) -> None:
        super().__init__()
        self.truth_witness = truth_witness
        self.always_satisfied = always_satisfies

    def is_truth_witness(self):
        return self.truth_witness
    
    def get_termination_intervals(self) -> List[Relational | bool]:
        return self.always_satisfied