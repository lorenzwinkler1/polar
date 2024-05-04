# Validated with example 5.2 form paper https://doi.org/10.1007/s10703-023-00440-z

from sympy import Eq, Mul, Poly, Pow, expand, sympify, Symbol, smtlib_code


NUM_VARS = 2
MAX_DEGREE = 2
DO_LABEL = True


def get_monom_tuples(num_vars, max_degree):
    if num_vars == 0:
        return [tuple()]
    
    options = []
    for i in range(max_degree+1):
        rem = get_monom_tuples(num_vars-1, max_degree-i)
        for r in rem:
            options.append((i,)+r)
    
    return options
        
monomial_tuples = get_monom_tuples(NUM_VARS, MAX_DEGREE)
vars = [Symbol(f'x_{i}', real=True) for i in range(NUM_VARS)]
def get_monomial(vars, coeffs):
    monom = sympify(1)
    for i in range(len(coeffs)):
        monom= monom*vars[i]**coeffs[i]
    return monom

monomials = [get_monomial(vars, coeff) for coeff in monomial_tuples]


def n(monom):
    if not monom.is_symbol:
        monom = expand(monom)
        symbols = monom.free_symbols

        substitutes = {Symbol(str(var)+"_TMP", real=True): expand(n(sym)) for sym in symbols}

        monom = monom.subs({var: Symbol(str(var)+"_TMP", real=True) for var in vars})
        return expand(monom.subs(substitutes))
    
    # refers tu x_i
    if not str(monom).startswith("x_"):
        return monom
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
        exprs.append(Eq(coeffs[k], Symbol(f"p_r_{i}_{'_'.join(map(str, monoms[k]))}", real = True)))
        exprs.append(Eq(Symbol(f"p_r_{i}_{'_'.join(map(str, monoms[k]))}", real = True), int(should_be_one)))


# p_{l,i}
inverse_dict = {}
for i,var in enumerate(vars):
    eq = sympify(0)
    for j, monom in enumerate(monomials):
        monomial_tuple = monomial_tuples[j]
        eq += monom*Symbol(f"a_{i}__{'_'.join(map(str, monomial_tuple))}")

    tmp_symbol = Symbol(str(var)+"_TMP", real=True)
    inverse_dict[tmp_symbol] = eq


for i, var in enumerate(vars):
    eq = n(var)
    # substitute in inverse dict
    eq = eq.subs({var: Symbol(str(var)+"_TMP", real=True) for var in vars})

    eq = eq.subs(inverse_dict)
    poly = Poly(eq, *vars)
    coeffs = poly.coeffs()
    monoms = poly.monoms()

    for k in range(len(coeffs)):
        should_be_one = monoms[k][i] == 1 and sum(monoms[k])==1
        exprs.append(Eq(coeffs[k], Symbol(f"p_l_{i}_{'_'.join(map(str, monoms[k]))}", real = True)))
        exprs.append(Eq(Symbol(f"p_l_{i}_{'_'.join(map(str, monoms[k]))}", real = True), int(should_be_one)))

# Now the u' requirement

# Later u is the input!

us = [expand(((-vars[1]**2+vars[0])**2 + vars[1])**2 - 2*vars[1]**2+2*vars[0]),\
      expand((-vars[1]**2+vars[0])**2 + vars[1])]

assert len(us) == NUM_VARS

n_s = [n(var).subs({var: Symbol(str(var)+"_TMP", real=True) for var in vars})
        for var in vars]

# u ( n^{-1} (x))

u_dashs = {
   Symbol(str(var)+"_TMP", real=True): expand(u) for i, u in enumerate(us)
}

ns = [expand(n.subs(u_dashs)).subs({var: Symbol(str(var)+"_TMP", real=True) for var in vars}) for n in n_s]

pass


n_prime_s = {}

for i,var in enumerate(vars):
    # p_{r,i}, where x_i is the var
    eq = sympify(0)
    for j in range(len(monomials)):
        mono = monomials[j]
        monomial_tuple = monomial_tuples[j]
        eq += Symbol(f"a_{i}__{'_'.join(map(str, monomial_tuple))}")*mono
    n_prime_s[Symbol(str(var)+"_TMP", real=True)] = eq

n_s = [n.subs(n_prime_s) for n in n_s]

n_s = [expand(n) for n in n_s]

# now substitute inverse

coeffs_to_assert_zero = []
# Now do comparison of coefficients again
for i, var in enumerate(vars):
    u_dash = n_s[i]

    poly = Poly(u_dash, *vars)
    coeffs = poly.coeffs()
    monoms = poly.monoms()

    for k in range(len(coeffs)):
        sym = Symbol(f"c_{i}_{'_'.join(map(str, monoms[k]))}", real = True)
        exprs.append(Eq(coeffs[k], sym))

        if monoms[k][i] > 0 or (monoms[k][i]==1 and sum(monoms[k])>1):
            exprs.append(Eq(sym, 0))


smt_str = smtlib_code(exprs)
smt_str = str(smt_str)

i=0
if DO_LABEL:
    smt_str = smt_str.replace("(=", "(! (=")

    while smt_str.find("))\n")>0:
        smt_str = smt_str.replace(f"))\n", f") :named a{i}) )\n" ,1)
        i+=1

print(smt_str)