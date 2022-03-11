### Mate

#%%


from typing import List


def gcd(a: int, b: int, verbose=True):
    """
        Euclid GCD CMMDC
    """
    if a == 0:
        if verbose:
            print(f"gcd({a}, {b}) = {b}")
        return b
    if verbose:
        print(f"gcd({a}, {b}) = ", end='')
    d = gcd(b % a, a, verbose)
    return d

assert gcd(12, 8, False) == gcd(8, 12, False) == 4
gcd(12, 8)

#%%
def extended_gcd(a: int, b: int, verbose=True):
    """
        return (d, coef_a, coef_b)
        CMMDC extins Euclid extins
    """
    if a == 0:
        if verbose:
            print(f"0*0 + 1*{b} = {b}")
        return (b, 0, 1)
    
    d, form_cb, form_ca = extended_gcd(b % a, a, verbose)
    # d = form_cb * (b % a) + form_ca * a
    # d = form_cb * (b - a * (b//a)) + form_ca * a
    #   = form_cb * b + (form_ca - (b//a) * form_cb) * a

    cb = form_cb
    ca = form_ca - (b // a) * form_cb

    if verbose:
        print(f"{d} = {form_cb} * ({b}%{a}) + {form_ca} * {a} =>")
        print(f"{d} = {ca} * {a} + {cb} * {b}")

    return d, ca, cb

d, c_a, c_b = extended_gcd(12, 8, False)
assert d == c_a * 12 + c_b * 8 and d == 4

extended_gcd(16, 18)

#%%
def invers_modular(element: int, modul: int, verbose=True):
    """
        modular inverse
    """
    if verbose:
        print(f"Calculam inversul lui {element} fata de {modul}.")
        print(f"Calculam coeficientii x si y a.i. x * {element} + y * {modul} = 1 cu euclid:")

    d, x, y = extended_gcd(element, modul, verbose)

    if d != 1:
        print(f"{element} nu este prim cu {modul}!")
        raise Exception()

    if verbose:
        print(f"{x}*{element} + {y}*{modul} = 1, deci {x} este inversul lui {element}.")

    return x

assert invers_modular(5, 7, False) == 3
invers_modular(5, 7)

#%%
def crt(reminders: List[int], modulus: List[int]):
    