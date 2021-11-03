# Laborator 1 - Theodor Moroianu (grupa 334)

## Notiuni Generale

 * Adversar (A) - (3) O entitate (inclusiv un insider) care acționează rău intenționat pentru a compromite un sistem.
 * Securitate (B) - (1) O condiție care rezultă din stabilirea și menținerea măsurilor de protecție care permit unei organizații/sistem să își îndeplinească misiunea sau funcțiile critice, în ciuda riscurilor reprezentate de amenințări.
 * Crisc (C) - (5) O măsură a gradului în care o entitate este amenințată de o eventuală circumstanță sau eveniment.
 * Vulnerabilitate (D) - (2) Slăbiciune într-un sistem informațional, proceduri de securitate ale sistemului, controale interne sau implementare care ar fi putea fi exploatate sau declanșate de o sursă de amenințare.
 * Securitatea Cibernetica (E) - (4) Capacitatea de a proteja / apăra spațiul cibernetic de atacuri cibernetice.

## "The Security Mindset"

## Sisteme de Numeratie

### Convertiti ziua de nastere +10 in binar si invers

M-am nascut pe 30 Octombrie.
30 + 10 = 40, asa ca il convertim pe 40 in binar.
40 = 32 + 8 = 2^5 + 2^3 = 0b10100.
0b10100 = 2^3 + 2^5 = 8 + 32 = 40.

### Transformati un nr hexazecimal oarecare de 4 cifre in binar si invers

Alegem X = 0x12AB.

0x1 = 0b0001
0x2 = 0b0010
0xA = 0b1010
0xB = 0b1011

Asadar, 0x12AB = 0b0001001010101011 = 0b1001010101011.

Pentru a face transformarea inversa, impartim in grupe de 4, de la dreapta la stanga:
0b1001010101011 = 0b1 0010 1010 1011.

0b1 = 0x1
0b0010 = 0x2
0b1010 = 0xA
0b1011 = 0xB

Asadar, 0b1001010101011 = 0x12AB.

## Codul ASCII

Pentru a imi gasi codificarea numelui meu in ASCII, putem rula comanda:
$ python -c "print([ord(c) for c in 'Theodor Moroianu'])"

Rezultatul este:
[84, 104, 101, 111, 100, 111, 114, 32, 77, 111, 114, 111, 105, 97, 110, 117]

Pentru a imi afla numele in majuscula (THEODOR), putem rula aceeasi comanda.

Pentru a gasi codificarea ASCII putem rula comanda:
$ python -c "print(''.join([chr(int(x)) for x in input().split()]))"
> 66 82 65 86 79
BRAVO

## Base64

Pentru a imi encoda numele in basa 64, putem folosi tabelele specifice encodarii in basa 64, sau putem folosi direct comanda "base64":
$ echo "THEODOR" | base64
VEhFT0RPUgo=

Pentru a decoda, putem din nou folosi tabelele specifice, sau functia "base64":
$ echo "U3VudCBzdHVkZW50IGxhIEZNSS4=" | base64 -d
Sunt student la FMI.

## Introducere in Malware

 * Malware: Software malitios al carui obiect este de-a provoca daune pe sistemul in care ruleaza.
 * Virus: Un program capabil sa se auto-copieze fara autorizatia utilizatorului, de multe ori creat cu intetii malitioase.
 * Dropper: Un dropper este un program care se conecteaza la internet pentru a downloada un payload pe sistemul pe care ruleaza.
 * Downloader: Ca si dropperul, un downloader este un program capabil sa downloadeze un payload de pe internet fara autorizatia utilizatorului.
 * Trojan: Un trojan (referinta la calul troian) este un tip de malware care permite executarea diferitor actiuni la distanta (cum ar fi remote access). Cele mai clasice tipuri de troian sunt dropper / downloader. 
 * Spyware: Un spyware este un program al carui obiectiv este obtinerea unor informatii private ale unui utilizator fara autorizatia acestuia.
 * Riskware: Un riskware este un program scris cu intentii bune (nu un malware), dar care reprezinta un risc de securitate pentru sistemul pe care ruleaza, din cauza unor probleme pe cum incompatibilitati, buguri etc.
 * Ransomware: Un ransomware este un program care encripteaza datele de pe un device si cere o rascumparare pentru a le decripta.
 * Adware: Un adware este un program care afiseaza fara autorizatia utilizatorului publicitati pe dispozitivul acestuia.
 * Worm: Un worm este un virus capabil sa se raspandeasca pe diferite retele private sau publice fara sa necesite interactie umana.
 * Obfuscare: Obfuscarea unui program reprezinta diferite tehnici folosite pentru a face functionarea interna a programului greu de determinat. Este in general folosita de malware pentru a nu fi detectat de antivirusi.

## Masini virtuale

Am instalat Windows 7 pe Gnome Boxes, hipervizorul by default Gnome.
Pentru asta:
 * Am torrentat un iso windows 7
 * Am instalat windows intr-un VM
 * Nu am putut modifica setarile retelei pentru ca gnome boxes nu ofera aceasta functionalitate
 * Gnome Boxes a facut automat un snapshot

Am repetat de asemenea pasii de mai sus cu Virtual Box, care pare mai complet.





