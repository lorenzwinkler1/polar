# Validated with example 5.2 form paper https://doi.org/10.1007/s10703-023-00440-z
# file just temporary to have it in source control

from sympy import Eq, Mul, Poly, Pow, sympify, Symbol, smtlib_code


NUM_VARS = 2
MAX_DEGREE = 2


def get_monom_tuples(num_vars, max_degree):
    if num_vars == 0:
        return [tuple()]
    
    options = []
    for i in range(max_degree+1):
        rem = get_monom_tuples(num_vars-1, max_degree-i)
        for r in rem:
            options.append((i,)+r)
    
    return options
        
def pow_to_mul(expr):
    """
    Convert integer powers in an expression to Muls, like a**2 => a*a.
    """
    pows = list(expr.atoms(Pow))
    if any(not e.is_Integer for b, e in (i.as_base_exp() for i in pows)):

        raise ValueError("A power contains a non-integer exponent")
    repl = zip(pows, (Mul(*[b]*e,evaluate=False) for b,e in (i.as_base_exp() for i in pows)))
    return expr.subs(repl)

monomial_tuples = get_monom_tuples(NUM_VARS, MAX_DEGREE)
vars = [Symbol(f'x_{i}', real=True) for i in range(NUM_VARS)]
def get_monomial(vars, coeffs):
    monom = sympify(1)
    for i in range(len(coeffs)):
        monom= monom*pow_to_mul(vars[i]**coeffs[i])
    print(pow_to_mul(monom))
    return pow_to_mul(monom)

monomials = [get_monomial(vars, coeff) for coeff in monomial_tuples]


def n(monom):
    if not monom.is_symbol:
        symbols = monom.free_symbols

        substitutes = {sym: n(sym) for sym in symbols}
        return monom.subs(substitutes)
    
    # refers tu x_i
    i = str(monom).split("_")[1]

    term = sympify(0)
    for monomial_tuple in monomial_tuples:
        term += get_monomial(vars, monomial_tuple)*Symbol(f"b_{i}__{'_'.join(map(str, monomial_tuple))}" , real=True)
    return term

exprs = []
for i,var in enumerate(vars):
    # p_{r,i}, where x_i is the var
    eq = sympify(0)
    for j in range(len(monomials)):
        mono = monomials[j]
        monomial_tuple = monomial_tuples[j]
        eq += Symbol(f"a_{i}__{'_'.join(map(str, monomial_tuple))}")*n(mono)

    poly = Poly(eq, *vars)
    coeffs = poly.coeffs()
    monoms = poly.monoms()

    for k in range(len(coeffs)):
        should_be_one = monoms[k][i] == 1 and sum(monoms[k])==1
        exprs.append(pow_to_mul(Eq(coeffs[k], Symbol(f"p_r_{i}_{'_'.join(map(str, monoms[k]))}", real = True))))
        exprs.append(Eq(Symbol(f"p_r_{i}_{'_'.join(map(str, monoms[k]))}", real = True), int(should_be_one)))

    

print(smtlib_code(exprs))

def generate_p_r_i(monomials, ):
    pass