### Mate

#%%


from typing import List, Tuple

def gcd(a: int, b: int, verbose=True, offset=''):
    """
        Euclid GCD CMMDC
    """
    if a == 0:
        if verbose:
            print(f"{offset}gcd({a}, {b}) = {b}")
        return b
    if verbose:
        print(f"{offset}gcd({a}, {b}) = ", end='')
    d = gcd(b % a, a, verbose, offset)
    return d

assert gcd(12, 8, False) == gcd(8, 12, False) == 4
# gcd(12, 8)

#%%
def extended_gcd(a: int, b: int, verbose=True, offset=''):
    """
        return (d, coef_a, coef_b)
        CMMDC extins Euclid extins
    """
    if a == 0:
        if verbose:
            print(f"{offset}0*0 + 1*{b} = {b}")
        return (b, 0, 1)
    
    d, form_cb, form_ca = extended_gcd(b % a, a, verbose, offset)
    # d = form_cb * (b % a) + form_ca * a
    # d = form_cb * (b - a * (b//a)) + form_ca * a
    #   = form_cb * b + (form_ca - (b//a) * form_cb) * a

    cb = form_cb
    ca = form_ca - (b // a) * form_cb

    if verbose:
        print(f"{offset}{d} = {form_cb} * ({b}%{a}) + {form_ca} * {a} =>")
        print(f"{offset}{d} = {ca} * {a} + {cb} * {b}")

    return d, ca, cb

d, c_a, c_b = extended_gcd(12, 8, False)
assert d == c_a * 12 + c_b * 8 and d == 4

# extended_gcd(67, 1000)

#%%
def invers_modular(element: int, modul: int, verbose=True, offset = ''):
    """
        modular inverse
    """
    if verbose:
        print(f"{offset}Calculam inversul lui {element} fata de {modul}.")
        print(f"{offset}Calculam coeficientii x si y a.i. x * {element} + y * {modul} = 1 cu euclid:")

    d, x, y = extended_gcd(element, modul, verbose, '    ' + offset)

    if d != 1:
        print(f"{element} nu este prim cu {modul}!")
        raise Exception()

    if verbose:
        print(f"{offset}{x}*{element} + {y}*{modul} = 1, deci {x} este inversul lui {element}.")

    return x

assert invers_modular(5, 7, False) == 3
# invers_modular(5, 7)

#%%
def crt(reminders: List[int], modulus: List[int], verbose=True, offset=''):
    """
    Chinese reminder theorem
    Lema chineza a resturilor
    """
    if verbose:
        print(f"{offset}Calculam CRT un X, a.i.:")
        for i in range(len(reminders)):
            print(f"{offset}X % {modulus[i]} = {reminders[i]}")
    
    prod = 1
    for i in modulus:
        prod *= i
    
    if verbose:
        print(f"{offset}Produlus modulelor este {prod}")

    inverses = []
    for i in modulus:
        if verbose:
            print(f"{offset}Calculam inversul lui {prod} / {i} = {prod // i} modulo {i}:")
        invs = invers_modular(prod // i, i, verbose, '    ' + offset)
        inverses.append(invs)

    result = 0
    if verbose:
        print(f"{offset}X = ")
        for i in range(len(modulus)):
            print(f"{offset}   ({prod}/{modulus[i]}) * ({prod}/{modulus[i]})^-1 (mod {modulus[i]}) * {reminders[i]}" + (" +" if i + 1 != len(reminders) else ''))
    
    for i in range(len(modulus)):
        result += (prod // modulus[i]) * inverses[i] * reminders[i]

    result %= prod

    if verbose:
        print(f"{offset}X = {result}")
    
    return result

x = crt([1, 2, 3, 4, 0], [2, 5, 7, 11*13, 666013], False)
assert x % 2 == 1
assert x % 5 == 2
assert x % 7 == 3
assert x % (11*13) == 4
assert x % 666013 == 0

#%%

def cipolla(n: int, p: int, verbose=True, offset=''):
    """
        Cipolla algorithm
        square root sqrt radacina patrata in Fp
    """

    # cautam a a.i. a^2-n nu e rest patratic
    squares = [i * i % p for i in range(p)]
    a = 0
    while (a * a - n + p) % p in squares:
        a += 1
    
    if verbose:
        print(f"{offset}Folosim a={a}, care respecta {a}^2 - {n} ne rest patratic modulo {p}")

        print(f"{offset}Notam cu w = sqrt({a}^2 - {n})")

    # salvam elementele in grupul F[w]:
    # (s, t) -> s + t*w
    # valoarea lui w^2
    w_sq = (a*a - n + p) % p

    if verbose:
        print(f"{offset}Stim ca w^2 = {w_sq}")
    def multiply(s: Tuple[int, int], t: Tuple[int, int]):
        rez = (s[0]*t[0] + s[1]*t[1]*w_sq, s[0]*t[1] + s[1]*t[0])
        rez = (rez[0]%p, rez[1]%p)
        return rez
    
    if verbose:
        print(f"{offset}Calculam (w + a)^(p + 1)/2 = (w + {a})^{(p + 1)//2}")

    act = (1, 0)

    for i in range(1, (p + 1) // 2 + 1):
        act = multiply(act, (a, 1))

        if verbose:
            print(f"{offset}    (w + a)^{i} = {act[0]} + {act[1]}*w")

    assert(act[1] == 0)

    if verbose:
        print(f"{offset}sqrt({n}) = {act[0]} (mod {p})")
    return act[0]

inv = cipolla(1236, 666013, False)
assert inv * inv % 666013 == 1236
# cipolla(15, 17)

#%%

"""
Elgamal

Grup G, generator g.

Cheie secreta: X
Cheie publica: h = g^x

Encriptare:
 * Alegem y random.
 * c1 = g^y
 * c2 = h^y * m 
 * Mesaj criptat: (c1, c2) = (g^y, h^y * m)

Decriptare:
 * Primim (c1, c2) = (g^y, h^y * m) = (g^y, g^xy * m)
 * m = c2 * (c1^x)^-1


Caz aditiv:
Daca consideram grupul G ca fiind (Zp, +), atunci problema logaritmului
discret se poate rezolva cu euclid extins:
    Cautam x a.i. g*x = h
            <=> x = h * g^-1
Daca il stim pe x putem decripta mesajul. 
"""


#%%

"""
RSA decriptat cu phi(n) si dupa lambda(n)


Examen:

 * RSA cu phi si lambda
"""