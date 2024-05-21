from typing import List
from sympy import Dict, Expr, Monomial, Poly, Symbol, Tuple, simplify

from program.assignment.dist_assignment import DistAssignment


def compute_bounds_of_poly(poly: Poly,
                           branches: Dict[Symbol, Tuple[float, List[Poly]]],
                           dist_assignments: Dict[Symbol, DistAssignment],
                           closed_forms: Dict[Symbol, Expr]):
    """
    Compute the bounds of a poly given its possible update-branches
    """
    pass

def _monom_is_deterministic(monom: Monomial,
                            branches: Dict[Symbol, Tuple[float, List[Poly]]],
                            dist_assignments: Dict[Symbol, DistAssignment],):
    for sym in monom.free_symbols:
        if sym in branches and len(branches[sym][1])>1:
            return False
        if sym in dist_assignments:
            return False
    return True

def compute_bounds_of_monom(monom: Monomial,
                            branches: Dict[Symbol, Tuple[float, List[Poly]]],
                            dist_assignments: Dict[Symbol, DistAssignment],
                            closed_forms: Dict[Symbol, Expr]):
    if _monom_is_deterministic(monom, branches):
        # Substitute with closed form
        substitution = {closed_forms[sym] for sym in monom.free_symbols}
        return simplify(monom.subs(substitution))

    # TODO: Shortcut with negative power

    # Solve recurrence