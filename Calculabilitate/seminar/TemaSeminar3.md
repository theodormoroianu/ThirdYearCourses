# Tema seminar 3 -> 4

## Sa se vada daca `P` este prim cu o banda

### Idee

Presupunem ca banda contine initial `P` cifre de `1`, urmate de `Blank`. Daca dorim sa encodam numarul `p` ca `p+1` cifre de `1`, atunci trebuie sa extragem manual ultimul `1`.

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
    * Daca nu exista niciun `1` in dreapta `0`-lui dintre `p` si `x`, atunci am determinat ca **`X < P`**, si ne oprim.
    * Schimbam cel mai din dreapta `1` in `2` (scadem `1` din `X`).
    * Schimbam cel mai din stanga `1` in `2` (scadem `1` din `P`).
    * Verificam daca mai exista un `1` inaintea lui `0` (daca `P` a devenit `0`).
        * Daca DA, atunci executam din nou pasul 2.
        * Daca NU, atunci am determinat ca **`X = P`**, si ne oprim.
    * Resetam banda in starea initiala, inlocuind `2` cu `1`.
3. Dorim sa vedem daca `X | P`.
    * Daca `P` contine numai `2`, atunci:
        * Daca si `X` contine numai `2`, atunci **`X | P`**, si deci `p` NU este prim.
        * Daca `X` contine cel putin un `1`, atunci **`X !| P`**.
    * Marcam un element din `P` din `1` in `2`.
    * Daca `X` contine numai `2`, atunci schimbam toti `2` din `X` in `1`.
    * Marcam un element din `X` din `1` in `2`.
    * Repeteam pasul 3.
4. Crestem pe `X` cu `1`. Ne ducem la capatul benzii, si inlocuim primul `Blank` cu `1`.
5. Ne intoarcem la pasul 2.

### Complexitate

Complexitatea este:

 * `O(p)` pentru pasul 1.
 * `O(p^2)` pentru pasul 2.
 * `O(p^2)` pentru pasul 3.

Executam pasul 1 o data, si pasul 2 si 3 de `p` ori, deci complexitatea algoritmului este `O(p^3)`.

## Sa se vada daca `P` este prim cu doua benzi

### Idee

Vom folosi un automat cu doua benzi.

Pe prima banda il vom pastra pe `p`, si pe a doua banda il vom pune pe `x`, care va lua valori in multimea `[2, 3, ... p-1]`.

Analog ca la automatul pe o singura banda, vom verifica la fiecare pas daca `x | p`.

### Pasii

Avem initial pe banda `1` `p` cifre de `1`, si banda `2` este goala.

1. Setam `x=2`. Pe banda `2` ne mutam de doua ori la dreapta punand un `1` pe banda.
2. Verificam daca `x < p`:
    * Ne ducem cu acul de citire cat mai la stanga pe ambele benzi.
    * Ne ducem in dreapta cu ambele acuri pana cand pe una dintre benzi dam de `Blank`.
        * Daca dam de `Blank` in acelasi timp pe ambele benzi, atunci `x = p`. Ne oprim, si declaram ca `p` ESTE PRIM.
        * Daca dam de `Blank` numai pe banda `2`, atunci `x < p`.
        * Nu avem cum sa dam de `Blank` mai intai pe banda `1`, pentru ca `x <= p`.
3. Verificam daca `x | p`:
    * Ne ducem cu acul de citire la inceputul ambelor benzi.
    * Ne ducem o pozitie mai in dreapta pe ambele benzi.
        * Daca dam pe ambele benzi de `Blank`, atunci `x | p`. ne oprim si declaram ca `p` NU ESTE PRIM.
        * Daca dam de `Blank` numai pe banda `1`, atunci `x !| p`.
        * Daca dam de `Blank` numai pe banda `2`, atunci mutam acul de pe banda `2` inapoi la inceputul benzii.
4. Adaugam un `1` la sfarsitul benzii `2` (il crestem pe `x` cu 1).
5. Ne ducem inapoi la pasul 2.

### Complexitate

Complexitatea fiecarui pas este:
 * `O(1)` pentru pasul 1.
 * `O(p)` pentru pasul 2.
 * `O(p)` pentru pasul 3.
 * `O(1)` pentru pasul 4.

Pasii 2, 3, 4 sunt executati de maxim `p` ori, deci complexitatea finala este `O(p^2)`.

## Sa se verifice daca `p` este prim cu >2 benzi

### Idee

Ideea este similara cu masina turing cu doua benzi, cu o diferenta:

Verificam `x` doar pana la $\sqrt{p}$. Pe banda `3` ne punem asadar `Y=1`, si cat timp `Y*Y < p`, il crestem pe `Y` cu `1`.

Dupa ce il avem pe `Y`, putem sa facem acelasi algoritm ca mai sus, oprindu-ne cand `x` este mai mare de `y` in loc de `p`.

### Complexitate

Calcularea lui `y` necesita `y^3 = p^1.5` pasi, si `x` va lua valori de la `1` la `y`, asadar complexitatea finala este `O(p^1.5)`.