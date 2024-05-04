from typing import Optional, Tuple
from sympy import Poly, sympify
from termcolor import colored
from program.condition.atom_cond import Atom
from program.condition.condition import Condition
from program.program import Program
from recurrences.rec_builder import RecBuilder
from recurrences.solver.recurrence_solver import RecurrenceSolver
from termination.polynomial_termination_condition import PolynomialTerminationCondition
from termination.termination_witness import TerminationWitness
from utils.expressions import get_monoms, unpack_piecewise


class TerminationAnalyzer:
    @classmethod
    def analyze(cls, normalized_program: Program, loop_guard: Condition):
        print()
        print(colored("-------------------", "cyan"))
        print(colored("-   Termination   -", "cyan"))
        print(colored("-------------------", "cyan"))
        print()

        if type(loop_guard) != Atom:
            print("At the moment only loop guard consisting of a single condition are supported")
            return
        
        poly, terminates_zero, terminates_negative = cls._normalize_atom(loop_guard)
        
        closed_form_poly = cls._compute_closed_form_of_polynomial(poly, normalized_program)

        witness = cls._analyze_poly(closed_form_poly, terminates_zero, terminates_negative)
        if witness is None:
            print("Program termination could not be determined")
            return
        if witness.is_termination_witness():
            print(colored("Program terminates. Witness found:", "green"))
        else:
            print(colored("Program does not terminate. Witness found:", "green"))
        print(witness)


    @classmethod
    def _compute_closed_form_of_polynomial(cls, poly: Poly, program: Program):
        recurrence_builder = RecBuilder(program)
        expanded_poly = poly.expand()
        symbols = expanded_poly.free_symbols
        solvers = {}
        closed_forms = {}

        for symbol in symbols:
            symbol = sympify(str(symbol))
            if symbol not in solvers:
                recurrences = recurrence_builder.get_recurrences(symbol)
                s = RecurrenceSolver(recurrences)
                solvers.update({sympify(m): s for m in recurrences.monomials})
            closed_forms[symbol], is_exact = recurrence_builder.get_solution(symbol, solvers)
            if not is_exact:
                print("Only exact closed forms are supported")

        closed_forms = {k: unpack_piecewise(closed_forms[k]) for k in closed_forms}
        return expanded_poly.subs(closed_forms)

    @classmethod
    def _analyze_poly(cls, poly: Poly, terminates_zero: bool, terminates_negative: bool) -> Optional[TerminationWitness]:


        # normalze the termination condition
        termination_condition = PolynomialTerminationCondition(poly, terminates_zero, terminates_negative)

        return termination_condition.get_witness()



    @classmethod
    def _normalize_atom(cls, atom: Atom) -> Tuple[Poly, bool, bool]:
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