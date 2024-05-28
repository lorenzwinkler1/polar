from typing import List
from sympy import Dict, Expr, Monomial, Poly, Symbol, Tuple, simplify, sympify

from program.assignment.dist_assignment import DistAssignment
from termination.util.constants import ITER_VAR
from termination.util.poly_utils import get_possible_signs


def compute_bounds_of_expr(poly: Poly,
                           branches: Dict[Symbol, Tuple[float, List[Poly]]],
                           dist_assignments: Dict[Symbol, DistAssignment],
                           closed_forms: Dict[Symbol, Expr],
                           initial_values: Dict[Symbol, Expr]):
    """
    Compute the bounds of a poly given its possible update-branches
    """
    pass


def _monom_is_deterministic(monom: Monomial,
                            branches: Dict[Symbol, Tuple[float, List[Poly]]],
                            dist_assignments: Dict[Symbol, DistAssignment],):
    for sym in monom.free_symbols:
        if sym in branches and len(branches[sym][1]) > 1:
            return False
        if sym in dist_assignments:
            return False
    return True


def compute_bounds_of_monom(monom: Monomial,
                            branches: Dict[Symbol, Tuple[float, List[Poly]]],
                            dist_assignments: Dict[Symbol, DistAssignment],
                            closed_forms: Dict[Symbol, Expr],
                            initial_values: Dict[Symbol, Expr]):
    if _monom_is_deterministic(monom, branches):
        # Substitute with closed form
        bound = simplify(monom.subs(closed_forms))
        return bound, bound

    # TODO: Shortcut with negative power

    # Solve recurrence (this basically resembles __compute_bounds_of_monom_recurrence,
    # which also basically is Algorithm 1 from
    # "Automated TerminationAnalysis of Polynomial Probabilistic Programs, Mossbrugger et. al.")

    assert monom in branches
    # TODO: Ask marcel why "b.lower.xreplace({n: n - 1})" in amber
    inhom_bounds_upper = [compute_bounds_of_expr(b,
                                                 branches,
                                                 dist_assignments,
                                                 closed_forms,
                                                 initial_values)[1] for b in inhom(branches)[monom]]
    inhom_bounds_lower = [compute_bounds_of_expr(b,
                                                 branches,
                                                 dist_assignments,
                                                 closed_forms,
                                                 initial_values)[0] for b in inhom(branches)[monom]]

    max_upper = dominating(inhom_bounds_upper, ITER_VAR)
    min_lower = dominated(inhom_bounds_lower, ITER_VAR)

    min_rec = min(recurrence_constant(b) for b in branches)
    max_rec = max(recurrence_constant(b) for b in branches)

    maybe_pos, maybe_neg = get_possible_signs(*branches, 
                                              *inhom_bounds_lower, 
                                              *inhom_bounds_upper,
                                              monom.subs(initial_value))

    I = set()
    if maybe_pos:
        I.add(unique_positive_symbol())
    if maybe_neg:
        I.add(-unique_positive_symbol())
    if len(I) == 0:
        I.add(sympify(0))

    coeff_upper = {max_rec}
    if maybe_neg:
        coeff_upper.add(min_rec)
    
    coeff_lower = {min_rec}
    if maybe_pos:
        coeff_upper.add(max_rec)

    upper_candidates = compute_bound_candidates(coeff_upper, {max_upper}, I)
    lower_candidates = compute_bound_candidates(coeff_lower, {min_lower}, I)

    max_upper_candidate = dominating(upper_candidates, ITER_VAR)
    min_lower_candidate = dominated(lower_candidates, ITER_VAR)
    
    if not maybe_pos:
        max_upper_candidate = dominated([max_upper_candidate, sympify(0)], ITER_VAR)
        
    if not maybe_neg:
        min_lower_candidate = dominating([min_lower_candidate, sympify(0)], ITER_VAR)

    return max_upper_candidate, min_lower_candidate