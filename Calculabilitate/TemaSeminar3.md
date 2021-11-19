# Tema seminar 3 -> 4

## Sa se vada daca `P` este prim cu o banda

### Idee

Presupunem ca banda contine initial `P` cifre de `1`, urmate de `Blank`. Daca dorim sa encodam numarul `X` ca `X+1` cifre de `1`, atunci trebuie sa extragem manual ultimul `1`.

Vom incerca sa il impartim pe `P` succesiv la `2`, `3`, ..., `P-1`. Daca vreo impartire se efectueaza cu succes, atunci putem spune ca `P` NU este prim.

Pentru a verifica daca `P` se imparte la `X`, vom transforma banda in urmatoarea configuratie:

`1 | 1 | ... | 1 | 0 | 1 | ... | 1 | Blank ...`

Configuratia este practic `P` urmat de `X`, ambele encodate in baza `1`, cu un `0` intre ele.

Putem acum sa apelam o subrutina care sa verifice daca `P` se imparte la `X`, dupa care mai adaugam un `1` la `X`, si daca `X < P` repetam algoritmul.

Subrutina care verifica daca `P` se imparte la `X` are urmatorii pasi:

 * Marcheaza succesiv cate un `1` din `X` si din `P`.
 * Daca a marcat toti `1` din `X`, atunci reseteaza `X`-ul si continua algoritmul.
 * Daca a marcat toti `1` din `P`, atunci:
    * Daca a marcat toti `1` din `X`, atunci `X | P`.
    * Daca NU a marcat toti `1` din `X`, atunci `X !| P`.

### Pasii

Avem initial banda cu `P` cifre de `1`, si acul de citire pe prima pozitie.

Pasii automatului:

1. Ne ducem cu acul de citire la sfarsitul lui `P`, adaugam un `0` si doi de `1`, ca banda noastra sa devina:\
`1 | 1 | ... | 1 | 0 | 1 | 1 | Blank ...`.\
Mai departe vom considera numarul de `1` din prima bucata ca `P`, si din a doua bucata ca `X`.\
Acul de citire este acum pe ultima pozitie din `X`.
2. Verificam daca `X < P`. Daca `X = P`, atunci putem returna ca **P este prim**. Pentru a executa compararea dintre `X` si `P` facem:
    * Daca nu exista niciun `1` in dreapta lui `0`, atunci am determinat ca **`X < P`**, si ne oprim.
    * Schimbam cel mai din dreapta `1` in `2` (scadem `1` din `X`).
    * Schimbam cel mai din stanga `1` in `2` (scadem `1` din `P`).
    * Verificam daca mai exista un `1` inaintea lui `0` (daca `P` a devenit `0`).
        * Daca DA, atunci executam din nou pasul 2.
        * Daca NU, atunci am determinat ca **`X + P`**, si ne oprim.
    * Resetam banda in starea initiala, inlocuind `2` cu `1`.
3. Dorim sa vedem daca `X | P`.
    * Daca `P` contine numai `2`, atunci:
        * Daca si `X` contine numai `2`, atunci **`X | P`**.
        * Daca `X` contine cel putin un `1`, atunci **`X !| P`**.
    * Marcam un element din `P` din `1` in `2`.
    * Daca `X` contine numai `2`, atunci schimbam toti `2` din `X` in `1`.
    * Marcam un element din `X` din `1` in `2`.
    * Repeteam pasul 3.
4. Crestem pe `X` cu `1`. Ne ducem la capatul benzii, si inlocuim primul `Blank` cu `1`.
5. Ne intoarcem la pasul 2.

## Sa se vada daca `P` este prim cu mai multe benzi
