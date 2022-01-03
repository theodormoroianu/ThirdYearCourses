# Cheat Sheet

## Inmultire

### O Banda

 `[ a | b ] => [a | b | a*b]`

Avem `a` `1`-uri urmate de `b` `1`-uri. Vrem sa adaugam `a*b` `1`-uri la sfarsitul benzii.

 * Ciclam:
    * Daca nu mai este niciun `1` in `a`, atunci iesim din ciclu.
    * Marcam primul `1` din `a` in `2`.
    * Ciclam:
        * Daca nu mai este niciun `1` in `b`, atunci iesim din cilu.
        * Marcam primul `1` din `b` in `2`.
        * Adaugam un `1` la sfarsitul benzii.
    * Marcam toti `2` din `b` inapoi in `1`.
* Marcam toti `2` din `a` inapoi in `1`.

Complexitate: O(a * (a + b * (b + a * b))) = O(a^2 * b^2)

### Mai Multe Benzi

`B1[a], B2[b], B3[] => B1[a], B2[b], B3[a*b]`

* Ciclam:
    * Daca pe B1 am dat de Blank, atunci iesim din ciclu.
    * Ne mutam la dreapta pe B1.
    * Ciclam:
        * Daca pe B2 am dat de Blank, atunci iesim din ciclu.
        * Ne ducem in dreapta pe B2.
        * Adaugam un 1 si ne ducem la dreapta pe B3.
    * Punem cursorul de pe B2 inapoi la inceputul benzii.
* Mutam cursorul de pe B1 si B3 inapoi la inceputul benzii.

Complexitatea: O(a * b)

## Impartire

### O Banda

`[a | b] => [a | b | a/b]`

* Ciclam:
    * Ciclam:
        * Daca `b` nu mai contine niciun `1`, atunci iesim din ciclu.
        * Marcam primul `1` din `b` in `2`.
        * Daca `a` nu contine niciun `1`, atunci iesim din AMBELE cicluri.
        * Marcam primul `1` din `a` in `2`.
    * Adaugam `1` la sfarsitul benzii.
    * Marcam toti `2` din `b` in `1`.
* Marcam inapoi toti `2` din `a` si `b` in `1`.

Complexitate: O(a^2) ??

### Mai Multe Benzi

`B1[a], B2[b], B3[] => B1[a], B2[b], B3[a/b]`

* Ciclam:
    * Daca dam de Blank pe banda B2, atunci
        * Adaugam un `1` la sfarsitul benzii B3.
        * Mutam acul de citire la inceputul benzii B2.
    * Daca dam de un Blank pe banda B1, atunci iesim din ciclu.

Complexitate: O(a)

## Radical

### O Banda

`[a] => [a | b=sqrt(a)]`

* Adaugam un `0` dupa `a` pe banda (setam `b=0`).
* Ciclam:
    * Pentru fiecare element din `b`:
        * Daca nu sunt doua elemente nemarcate in `a`, atunci iesim din cicluri.
        * Marcam doua elemente din `a`.
    * Daca nu mai exista niciun element nemarcat in `a`, atunci iesim din ciclu.
    * Marcam un element in `a`.
    * Crestem `b` cu `1`.

Complexitate: O(a^2)

### Mai Multe Benzi

Ne folosim de faptul ca 1+3+5+...+ 2k+1 = k^2

`B1[a], B2[] => B1[a], B2[sqrt(a)]`

* Ciclam:
    * Parcurgem toata banda B2, mergand la dreapta pe banda B1 la fiecare pas.
    * Daca pe banda B1 am dat de Blank, atunci iesim din ciclu.
    * Mergem o pozitie la dreapta pe banda B1.
    * Adaugam un 1 la sfarsitul benzii B2.

Complexitate: O(a).

## Log
