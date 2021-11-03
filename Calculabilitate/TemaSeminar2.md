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
    * `(Q0, 1) -> (Q1, a, middle)`.
 * Inlocuim pentru fiecare `a` cate un `1`.
    * `(Q1, a) -> (Q2, c, right)`.
    * `(Q2, b) -> (Q2, c, right)`.
    * `(Q2, 1) -> (Q3, b, left)`.
    * `(Q3, b) -> (Q3, b, left)`.
    * `(Q3, a) -> (A3, a, left)`.
    * `(Q3, c) -> (Q1, c, right)`.
 * Inlocuim toti `b` si `c` cu `a`.
    * `(Q1, b) -> (Q4, b, right)`.
    * `(Q4, b) -> (Q4, b, right)`.
    * `(Q4, 1) -> (Q5, 1, left)`.
    * `(Q4, Blank) -> (Q6, Blank, left)`.
    * `(Q5, b) -> (Q5, a, left)`.
    * `(Q5, c) -> (Q5, a, left)`.
 * Verificam incepem din nou algoritmul.
    * `(Q5, Blank) -> (Q1, Blank, right)`.
