# Laborator 2 - Theodor Moroianu (grupa 334)

## Exercitiu 1

Criptologie (A)        - 4
Criptografie (B)       - 2
Criptanaliza (C)       - 5
Confidentialitate (D)  - 1
Integritate (E)        - 6
Disponibilitate (F)    - 3

## Exercitiul 2

1. Salariile angajatilor nu se fac publice: Confidentialitate
2. Biroul caseriei are acces la salarii: Disponibilitate
3. Un angajat nu isi poate schimba salariul: Integritate
4. Un angajat nu afla ce face colegu: Confidentialitate
5. Caseria are certitudinea ca suma e corecta: Integritate

Exemple de primitive criptografice:
 * Confidentialitatea: Criptarea asimetrica - ceva criptat cu cheia publica poate fi decriptat numai cu cheia privata.
 * Integritatea: Criptare asimetrica - ceva criptat cu cheia privata este integru.

## Exercitiul 3

1. Adversarul fiind polinomial in timp, NU are timp infinit la dospozitite, deci orice adversar care are la dispozitie un timp infinit pentru criptanaliza sistemului NU este PPT.

2. Un adversar are voie sa "ghiceasca" cheia de criptare. Un algoritm gresit de-a ghici cheile reduce probabilitatea de succes al atacului, dar nimic nu il impiedica sa o faca. Asadar, DA, are voie sa ghiceasca cheia.

3. Functiile exponentiale crescand mai repede decat orice polinomiale, PPT NU are la dispozitie algoritmi exponentiali.

## Exercitiul 4

1. f(x) = 2 nu are limita in 0, (este constanta), deci NU este neglijabila.
    Putem alege P(x) = x, si rangul 1.

2. f(x) = 1 / 2000 nu are nici ea limita in 0 (este si ea constanta), deci NU este neglijabila.
    Putem alege P(x) = x, si rangul 2001.

3. f(x) = 1 / n^2000 este inversa unei functii polinomiale. NU este neglijabila.
    Putem alege P(x) = 2 * n^2000, rang 1.

4. f(x) = 1/2^n este inversa unei exponentiale, asadar ESTE neglijabila.

5. f(x) = f1(x) + f2(x), f1, f2 neglijabile ESTE si ea neglijabila.

6. f(x) = f1(x) + f2(x), f2 ne-neglijabila asadar nici f NU este neglijabila.

## Exercitiul 5

Securitatea perfecta, desi pare mai buna, nu reprezinta un algoritm concret care sa poata fi aplicat in practica.
Algoritmi precum RSA ofera o securitate computationala inalta, rezistenta la orice fel de atac PPT, si deci pot fi astfel folositi in practic fara vreun risc real legat de ne-optimalitatea acestora din punct de vedere criptografic.
Indiferent de resursele atacantului, acesta se supune totusi unor restrictii si limitari fizice.

## Exercitiul 6

1. Pot exista 2^512 = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084096.
2. Daca testeaza 2^30 chei pe secunda, ii vor trebui 2^(512-30) = 2^(482) secunde = 12486994201263968925526388919172665222994392570659884603436627838501486955279062480481224412253967884639307724485626491581791902717153141225160704 secunde = 3.959599886245551e+137 ani.
3. Consider ca este un atac putin cam lent :(, deci NU.

