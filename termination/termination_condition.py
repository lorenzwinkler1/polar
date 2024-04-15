from typing import List
from sympy import Poly, simplify
from program.condition.and_cond import And
from program.condition.atom_cond import Atom
from program.condition.condition import Condition
from program.condition.false_cond import FalseCond
from program.condition.true_cond import TrueCond
from termination.termination_condition_witness import TerminationConditionWitness
from utils.expressions import unpack_piecewise


class TerminationCondition:
    def __init__(self, condition: Condition, closed_forms) -> None:
        self.condition = condition
        self.closed_forms = closed_forms

    def get_witness(self) -> TerminationConditionWitness:
        cond_atoms: List[Atom] = self._extract_atoms(self.condition)

        raise NotImplementedError()