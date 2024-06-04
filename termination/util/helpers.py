from sympy import Symbol, limit, oo
from termination.util.constants import ITER_VAR


def amber_limit(expr):
    if ITER_VAR in expr:
        return limit(expr, ITER_VAR, oo)
    return expr

count = 0
def unique_positive_symbol():
    count += 1
    return Symbol(f"__a__{count}", positive=True, real=True)
