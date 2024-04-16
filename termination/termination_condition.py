from typing import List, Tuple, cast
import numpy as np
from sympy import Poly, Symbol, simplify
from program.condition.and_cond import And
from program.condition.atom_cond import Atom
from program.condition.condition import Condition
from program.condition.false_cond import FalseCond
from program.condition.true_cond import TrueCond
from termination.exact_termination_witness import ExactWitness
from termination.termination_witness import TerminationWitness
from utils.expressions import unpack_piecewise
import numpy.polynomial.polynomial as np_poly


class TerminationCondition:
    def __init__(self, condition: Condition, closed_forms) -> None:
        self.condition = condition
        self.closed_forms = closed_forms

    def get_witness(self) -> TerminationWitness:
        termination_witness = self._get_termination_witness_for_atom(self.condition)

        if termination_witness is not None and termination_witness:
            return termination_witness
        
        # nontermination_witness = self._get_termination_witness_for_atom(self.condition, True)
    
    def _get_termination_witness_for_atom(self, condition: Condition) -> TerminationWitness:
        if not isinstance(condition, Atom):
            raise NotImplementedError()
        
        condition = cast(Atom, condition)

        poly, terminates_on_zero, terminates_negative = self._normalize_atom(condition)
        n = Symbol('n', integer=True)
        closed_forms = {k: unpack_piecewise(self.closed_forms[k]) for k in self.closed_forms}
        poly=Poly(poly.subs(closed_forms))
        print(f"Normalized polynomial of loop guard {poly}")

        if len(poly.free_symbols) > 1:
            return None
        
        
        # extract coefficients
        coeffs = [float(coeff) for coeff in poly.all_coeffs()]
        zeros = cast(np.ndarray, np_poly.polyroots(list(reversed(coeffs))))
        print(f"Found zeros: {zeros}")

        ns_to_check = [int(zero) for zero in zeros] + [int(zero)+1 for zero in zeros]
        ns_to_check.sort()

        first_n = None
        for n in ns_to_check:
            if n<0:
                continue
            value = poly.eval(n)
            print(f"f({n})={value}")
            if value < 0 and terminates_negative:
                first_n = n
                break
            if value == 0 and terminates_on_zero:
                first_n = n
                break
        return ExactWitness(condition, zeros, first_n)
        
    
    def _normalize_atom(self, atom: Atom) -> Tuple[Poly, bool, bool]:
        # returns a normalized polynomial as first return value.
        # second return value specifies, whether the condition is false for zero
        if atom.cop == ">":
            return atom.poly1 - atom.poly2, True, True
        if atom.cop == "<":
            return atom.poly2 - atom.poly1, True, True
        if atom.cop == ">=":
            return atom.poly1 - atom.poly2, False, True
        if atom.cop == "<=":
            return atom.poly2 - atom.poly1, False, True
        if atom.cop == "==":
            return atom.poly2 - atom.poly1, True, False
        else:
            raise NotImplementedError()