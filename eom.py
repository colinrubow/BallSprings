import sympy as sp

t = sp.symbols('t')
r_1 = sp.Function('r_1')(t)
r_2 = sp.Function('r_2')(t)
r_3 = sp.Function('r_3')(t)

r_1dot = r_1.diff(t)
r_1ddot = r_1dot.diff(t)
r_2dot = r_2.diff(t)
r_2ddot = r_2dot.diff(t)
r_3dot = r_3.diff(t)
r_3ddot = r_3dot.diff(t)

eqs = [
    sp.Eq(r_1ddot, (r_3 - r_1)/3),
    sp.Eq(r_2ddot, (r_3 - r_2)/3),
    sp.Eq(r_3ddot, (r_1 + r_2 - 2*r_3)/3)
]
icx = {
    r_1.subs(t, 0): 1,
    r_2.subs(t, 0): -1/2,
    r_3.subs(t, 0): -1/2,
    r_1dot.subs(t, 0): 0,
    r_2dot.subs(t, 0): -sp.sqrt(3)/2,
    r_3dot.subs(t, 0): sp.sqrt(3)/2
}
sol = sp.dsolve(eqs, [r_1, r_2, r_3], ics=icx)
sp.pprint(sol)

icy = {
    r_1.subs(t, 0): 0,
    r_2.subs(t, 0): sp.sqrt(3)/2,
    r_3.subs(t, 0): -sp.sqrt(3)/2,
    r_1dot.subs(t, 0): 1,
    r_2dot.subs(t, 0): -1/2,
    r_3dot.subs(t, 0): -1/2
}
sol = sp.dsolve(eqs, [r_1, r_2, r_3], ics=icy)
print()
print()
sp.pprint(sol)
