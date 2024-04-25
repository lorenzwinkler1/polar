from typing import List, Tuple, cast
import numpy as np
from sympy import Poly, Symbol, limit, real_roots, simplify, solve
from program.condition.and_cond import And
from program.condition.atom_cond import Atom
from program.condition.condition import Condition
from program.condition.false_cond import FalseCond
from program.condition.true_cond import TrueCond
from termination.asymptotic_termination_witness import AsymptoticTerminationWitness
from termination.exact_termination_witness import ExactWitness
from termination.termination_witness import TerminationWitness
from utils.expressions import unpack_piecewise
import numpy.polynomial.polynomial as np_poly


class PolynomialTerminationCondition:
    def __init__(self, poly: Poly, terminates_zero: bool, terminates_negative: bool) -> None:
        self.poly = poly
        self.terminates_zero = terminates_zero
        self.terminates_negative = terminates_negative

    def get_witness(self) -> TerminationWitness:
        n = Symbol('n')
        poly = Poly(self.poly, n)

        if len(poly.free_symbols) == 1:
            return self._get_exact_witness(poly, self.terminates_zero, self.terminates_negative)
        
        return self._get_asymptotic_witness(poly, self.terminates_zero, self.terminates_negative)
    
    def _get_asymptotic_witness(self, poly: Poly, terminates_on_zero: bool, terminates_negative: bool):
        leading_coeff = poly.coeffs()[0]
        print(type(leading_coeff))
        print(f"Leading coefficient: {leading_coeff}")

        if not terminates_negative:
            # exact termination conditions can not be checked asymptotically
            return None

        # TODO: this currently is very naive, and can, at least for coefficients
        # that consist of low-degree polynomials over constants, be improved

        if leading_coeff.is_negative:
            return AsymptoticTerminationWitness(poly)
        
        # if leading_coeff is positive, we still don't know for sure if the 
        # condition is false for some ("smaller") n

        return None
        
        
    def _get_exact_witness(self, poly: Poly, terminates_on_zero: bool, terminates_negative: bool):
        # extract coefficients
        coeffs = [float(coeff) for coeff in poly.all_coeffs()]
        zeros = cast(np.ndarray, np_poly.polyroots(list(reversed(coeffs))))
        print(f"Found zeros: {zeros}")

        ns_to_check = [0]+[int(zero) for zero in zeros] + [int(zero)+1 for zero in zeros]
        ns_to_check.sort()

        first_n = None
        for n in ns_to_check:
            if n<0:
                continue
            value = poly.eval(n)
            if value < 0 and terminates_negative:
                first_n = n
                break
            if value == 0 and terminates_on_zero:
                first_n = n
                break
        return ExactWitness(poly, zeros, first_n, terminates_on_zero, terminates_negative)
