# Lab 11 - Moroianu Theodor - 334

## 1

a. Adevarat
b. Fals
c. Adevarat
d. Adevarat
e. Fals
f. Fals
g. Fals
h. Adevarat
i. Fals

## 2

Trei aspecte ar fi:
 * Validam datele
    * validare atat pe front-end cat si pe back-end
    * Mail-ul sa aiba format de mail
    * Username sa aiba un format standard
    * Parola sa aiba o anumita complexitate
 * Sa limitam numarul de requesturi de pe un dispozitiv
 * Sa verificam daca emailul apartine utilizatorului trimitand un email la acel link.
* Sa hashuim parolele cu un salt
 

## 3

 * Sa efectuam un 2FA bazandu-ne pe email
 * Sa setam o durata de exiprare pentru cookie-ul de autentificare
 * Sa limitam numarul de incercari inainte de-a introduce un CAPTSA.
 * Sa nu dam mesaje prea informative daca autentificarea nu reuseste.
 * Sa validam datele, pentru a evita atacuri de tip SQL Injection.


## 4

### Exemplu 1

Cookie-urile, in loc sa salveze un token de autentificare, salveaza direct userul cu care este conectata o persoana.
Un hacker poate sa schimbe manual cookie-ul sau cu un alt user, si sa se conecteze pe aplicatie cu userul altcuiva.

### Exemplu 2

Validarile pentru a evita SQL Injection / username ne-conform sunt facute doar pe fron-end.
Un hacker poate trimite un request cu date nevalidate, si sa faca un atac de tip SQL Injection.

### Exemplu 3

Site-ul, cand se aceseaza o pagina care nu exista, ne afiseaza mesajul "Pagina XXXX nu a fost gasita", fara sa faca validari peste numele paginii. Un hacker poate folosi aceasta functionalitate pentru a efectua un atac de tip cross-site scripting.

### Exemplu 4

Aplicatia salveaza in memorie un field de lungime 100 pentru parola, pentru ca nimeni nu are parole asa lungi.
Un hacker poate trimite intentionat o parola mai lunga, pentru a efectua un atac de tip stack buffer overflow.

### Exemplu 5

Aplicatia retine parolele in clar, si comparara parola salvata cu cea noua cu o comparare de stringuri.

Un hacker poate efectua un atac de tip timing attack, pentru a compromite parola.


## Ex 5

Am folosit tool-ul "OWASP" pentru a scana site-ul http://testphp.vulnweb.com/.

Am gasit mai multe vulnerabilitati, cum ar fi:
 * X-Frame-Options Header Not Set
 * Absence of Anti-CSRF Tokens
 * Server Leaks Information via "X-Powered-By" HTTP Response Header Field(s)
 * X-Content-Type-Options Header Missing
 * Cross Site Scripting (Reflected)

