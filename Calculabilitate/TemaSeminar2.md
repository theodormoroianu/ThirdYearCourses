# Tema Semiar 2 Theodor Moroianu (334)

Avem de verificat daca un numar este sau nu o putere de 2.

## Idee

 1. Inlocuim primul caracter de `1` cu un `a`.
 2. Inlocuim atati de `1` cu `b` cati avem de `a` (si inlocuim pe `a` in `c`).
 3. Inlocuim `b` si `c` cu `a`.
 4. Daca am terminat tot sirul, atunci acceptam cuvantul.
 5. Daca nu, ne intoarcem la pasul 2.

## Definitie Formala

Starea initiala: `Q0`.

Starea finala: `Q6`.

Tranzitii:

 * Punem un `a` pe banda.
    * `(Q0, 1) -> (Q7, a, right)`.
    * `(Q7, Blank) -> (Q6, Blank, left)`.
    * `(Q7, 1) -> (Q1, 1, left)`.
 * Inlocuim pentru fiecare `a` cate un `1`.
    * `(Q1, a) -> (Q2, c, right)`.
    * `(Q2, a) -> (Q2, a, right)`.
    * `(Q2, b) -> (Q2, b, right)`.
    * `(Q2, 1) -> (Q3, b, left)`.
    * `(Q3, b) -> (Q3, b, left)`.
    * `(Q3, a) -> (Q3, a, left)`.
    * `(Q3, c) -> (Q1, c, right)`.
 * Inlocuim toti `b` si `c` cu `a`.
    * `(Q1, b) -> (Q4, b, right)`.
    * `(Q4, b) -> (Q4, b, right)`.
    * `(Q4, 1) -> (Q5, 1, left)`.
    * `(Q4, Blank) -> (Q6, Blank, left)`.
    * `(Q5, b) -> (Q5, a, left)`.
    * `(Q5, c) -> (Q5, a, left)`.
 * Incepem din nou algoritmul (de-a inlocui atati de 1 cati a).
    * `(Q5, Blank) -> (Q1, Blank, right)`.


## Complexitate

Daca sunt `N` de 1 pe banda, programul are o complexitate de:
`C(N) = 2^2 + 4^2 + 8^2 + ... + 2^(log2(N))^2`.
Complexitatea este asadar `O(N^2)`.
