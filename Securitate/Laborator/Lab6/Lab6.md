# Lab 6 - Theodor Moroianu - 334

## Ex 1

### Candidate 1

Nu este un PRNG pentru ca a^a=0, deci secventa de numere afisata va fi mereu `seed, 0, 0, 0, ...,`, care in mod evident nu este PRNG.


### Candidate 2

Secventa are mai multe probleme:
 * Numerele tind spre infinit, ceea ce nu este fezabil din punct de vedere computational (au o crestere exponentiala, deci necesita o putere de calcul mult prea mare).
 * Sirul poate fi ghicit foarte simplu (reprezinta inmultirea termenilor cu 3/2).

### Candicate 3

 * Worst PRN in history.
 * Este constant, sirul o sa fie de forma `seed, seed, ...`, care in mod evident nu este pseudo-random.


## Ex 2

Solutiile exercitiului 2 sunt in fisierul `ex2.py`.

## Ex 3

### Problemele in secventele de cod

1. Cod 1
    Seed este `static final`, adica constant. Asta contrazice faptul ca seed-ul este un secret criptografic, care nu trebuie sa fie hardodat in cod sau mereu acelasi.
2. Cod 2
    Seed-ul este chiar id-ul user-ului. Asta inseamna ca oricine care stie id-ul unui user poate sa isi genereze local care este sessionID-ul userului, si sa il impersoneze.

### CWE ID

ID-ul in lista "CWE" este 336 (https://cwe.mitre.org/data/definitions/336.html).
Problema pe care o ridica este situatia in care un PRNG foloseste mereu acelasi seed la initializare.

### Ce se intampla cand spatiul seed-urilor este mic?

Daca spatiul seedurilor este mic, atunci ajungem la o alta vulnerabilitate - CWE339 (https://cwe.mitre.org/data/definitions/339.html). Seed-urilor pot fi brut-force-uite, si PRNG-ul spart.


### Gasirea atacului de spatiu mic

Atacul si vulnerabilitatea sunt descrise [aici](https://capec.mitre.org/data/definitions/112.html). 
Spatiul seed-ului este un element central al atacului - `Reduce search space: Find ways to reduce the secret space. The smaller the attacker can make the space they need to search for the secret value, the greater their chances for success. There are a great many ways in which the search space may be reduced.`. Daca spatiul este suficient de mic, putem sa il brute-force-uim.

### Alte defecte ale PRNG

Avem o lista de vulnerabilitati ale PRNG-urilor [aici](https://cwe.mitre.org/data/definitions/1213.html).
De exemplu, avem folositea de PRNG-uri care sa nu fie rezistente la atacuri criptografice, cum ar fi [CWE338](https://cwe.mitre.org/data/definitions/338.html).

### Inregistrari CVE pentru PRNG-uri

Putem cauta [aici](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=PRNG) dupa keyword-ul `prng` si gasim o groaza de vulnerabilitati. Din acest an sunt `4`.