#%%
from typing import List, Tuple

#%%

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

def lcm(a: int, b: int, verbose=True, offset=''):
    if verbose:
        print(f"{offset}lcm({a}, {b}) = {a}*{b}/gcd({a}, {b}) = {a}*{b} / {gcd(a, b, False)} = {a * b // gcd(a, b, False)}")
    return a * b // gcd(a, b, False)

assert gcd(12, 8, False) == gcd(8, 12, False) == 4
# gcd(12, 8)

#%%
def extended_gcd(a: int, b: int, verbose=True, offset=''):
    """
        return (d, coef_a, coef_b)
        CMMDC extins Euclid extins
    """
    d = gcd(a, b, False)
    a //= d
    b //= d

    def solve(x: int, y: int) -> Tuple[int, int]:
        """
        intoarce (d, a, b) a.i.
        d = a * x + b * y
        """
        coef_y = x // y
        rest = x % y
        if verbose:
            print(f"{offset}{x * d} = {y * d} * {coef_y} + {rest * d}")
        if rest == 1:
            if verbose:
                print(f"{offset}Calculam inapoi valorile:")
                print(f"{offset}{d} = {x * d} * 1 + {y * d} * -{coef_y}")
            return (1, -coef_y)

        c_y, c_r = solve(y, rest)
        c_x = c_r
        c_y -= coef_y * c_r
        if verbose:
            print(f"{offset}{d} = {x * d} * {c_x} + {y * d} * {c_y}")
        return (c_x, c_y)

    c_a, c_b = solve(a, b)
    assert c_a * a + c_b * b == 1
    return d, c_a, c_b

d, c_a, c_b = extended_gcd(12, 8, False)
assert d == c_a * 12 + c_b * 8 and d == 4

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
        print(f"{offset}{x}*{element} + {y}*{modul} = 1, deci {x} este inversul lui {element} fata de {modul}.")

    return x

assert invers_modular(5, 7, False) == 3
# invers_modular(5, 7)

#%%
def fast_pow(n, power, modulus=-1, verbose=True, offset=''):
    """
    Fast exponentiation algorithm
    pow put lgput exp
    modulus=-1 if no modulus
    """

    ans = n**power
    if modulus != -1:
        ans %= modulus
    
    if ans < 0 and modulus != -1:
        ans += modulus

    if verbose:
        print(f"{offset}Calculam {n}^{modulus}{'' if modulus == -1 else ' (mod' + str(modulus) + ')'}")
        p_act = 1
        while p_act <= power:
            r = n ** p_act
            if modulus != -1:
                r %= modulus
            print(f"{offset} - {n}^{p_act} = {r}")
            p_act *= 2
        
        print(
            f"{offset}{power} = " +
            " + ".join([str(2**i) for i in range(1000) if ((power >> i) & 1) != 0])
        )
        print(
            f"{offset} => {n}^{power} = " +
            " * ".join([f"{n}^{2**i}" for i in range(1000) if ((power >> i) & 1) != 0])
        )
        print(
            f"{offset} => {n}^{power} = " +
            " * ".join([str(n**(2**i) if modulus == -1 else n**(2**i) % modulus) for i in range(1000) if ((power >> i) & 1) != 0])
        )

        print(f"{offset} => {n}^{power} = {ans}")
    
    return ans

put = fast_pow

assert fast_pow(123, 234, -1, False) == 123 ** 234
assert fast_pow(12, 44, 37, False) == 12**44 % 37

# fast_pow(3, 45, 10)

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
def lfsr(s_init, coefs, l, verbose=True, offset=''):
    """
        lfsr shift registers linear
        s[i] = coef[0]*s[i-1] + coef[1]*s[i-2] + ... + coef[n-1]*s[i-n]
    """
    rez = s_init
    while len(rez) < l:
        c = 0
        for i in range(len(coefs)):
            c ^= rez[-i] * coefs[i]
        rez.append(c)
    return rez
# TODO: Test


#%%
def cipolla(n: int, p: int, verbose=True, offset=''):
    """
        Cipolla algorithm
        square root sqrt radacina patrata in Fp
        P ESTE PRIM
    """

    # cautam a a.i. a^2-n nu e rest patratic
    squares = [i * i % p for i in range(p)]
    a = 0
    while (a * a - n + p) % p in squares:
        a += 1
    
    if verbose:
        print(f"{offset}Folosim a={a}, care respecta {a}^2 - {n} nu e rest patratic modulo {p}")

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
    put = (p + 1) // 2

    for i in range(1, put + 1):
        act = multiply(act, (a, 1))

        if verbose and (i & -i) == i:
            print(f"{offset}    (w + a)^{i} = {act[0]} + {act[1]}*w")

    assert(act[1] == 0)
    if verbose:
        print(
            f"{offset}(w + a)^{put} = " +
            " * ".join([f"(w+a)^{i}" for i in range(1, put + 1) if (i & -i) == i and (i & put) != 0]) +
            f" = {act[0]}"
        )

    if verbose:
        print(f"{offset}sqrt({n}) = {act[0]} (mod {p})")

    assert act[0] ** 2 % p == n % p
    return act[0]

inv = cipolla(1236, 666013, False)
assert inv * inv % 666013 == 1236

# cipolla(15, 17)

#%%

"""
Elgamal
Grup `G`, generator `g`.

Cheie secreta: `X`
Cheie publica: `h = g^x`

Encriptare:
 * Alegem `y` random.
 * `c1 = g^y`
 * `c2 = h^y * m` 
 * Mesaj criptat: `(c1, c2) = (g^y, h^y * m)`

Decriptare:
 * Primim `(c1, c2) = (g^y, h^y * m) = (g^y, g^xy * m)`
 * `m = c2 * (c1^x)^-1`


Caz aditiv:
Daca consideram grupul `G` ca fiind `(Zp, +)`, atunci problema logaritmului
discret se poate rezolva cu euclid extins:
    Cautam `x` a.i. `g*x = h`
            `<=> x = h * g^-1`
Daca il stim pe `x` putem decripta mesajul. 
"""


#%%
"""
## Deffie-Hellman

keyword: logaritm discret schimb de chei DLP

Grup `G`, generator `g`.

Alice:
 * Alege `a` random.
 * Transmite lui bob `ca = g^a`.

Bob:
 * Alege `b` random.
 * transmite lui Alice `cb = g^b`.

Alice:
 * Alege secretul `c = cb^a`.

Bob:
 * Alege acelasi secret `c = ca^b`.
"""

#%%
def legendre_is_residue(rest, modul, verbose=True, offset='') -> bool:
    """
    Rest patratic, quadratic residue modul HAS TO BE PRIME!!!!
    """
    if modul == 2:
        if verbose:
            print(f"{offset}modulul este 2, deci {rest} este un rest patratic.")
        return True
    if verbose:
        print(f"{offset}Calculam {rest}^(({modul}-1)/2) = {rest}^{(modul - 1) // 2}:")
        fast_pow(rest, (modul - 1) // 2, modul, True, "    ")
    
    p = rest ** ((modul - 1) // 2) % modul

    if verbose:
        if p == 1:
            print(f"{offset}Valoarea este 1, deci numarul ESTE un rest patratic")
        else:
            print(f"{offset}Valoarea nu este 1, deci numarul NU ESTE un rest patratic")
    return p == 1

assert legendre_is_residue(2, 7, False)
assert not legendre_is_residue(3, 7, False)

# legendre_is_residue(6, 31)

#%%

"""
RSA decriptat cu phi(n) si dupa lambda(n)


Examen:

 * RSA cu phi si lambda
"""