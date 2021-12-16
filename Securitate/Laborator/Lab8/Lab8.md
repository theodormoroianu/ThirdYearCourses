# Lab 8 SSI - Theodor Moroianu - 334

## Ex 1

### a.

Nu apare nicio eroare, poza se deschide normal.

### b.

Daca deschidem poza cu un editor hexadecimal, observam ca apare textul "This program cannot be run in DOS mode." in continutul imaginii. Este o evidentiere ca imaginea ascunde un fisier executabil.

### c.

Daca incarcam poza pe virustotal, nu gaseste niciun virus: https://www.virustotal.com/gui/file/dbd3b32b7327855cd335f14becb7f155e8fa166bf440f856752d87b7a44fdda6

### d. 

Cu ajutorul programului `Ghex`, am extras continutul de dupa primul "MZ", si pus intr-un executabil separat.
Cand il incarc pe virustotal, este detectat de cativa antivirusi ca fiind un trojan: https://www.virustotal.com/gui/file/5ce6bc2c78ec45babb393b2f8f1c30adce6e01a60fc23bfb22abc7e3496f50fa

### e. 

Nu am reusit sa decompresez dll-urile, dar presupun ca sunt necesare pentru a putea executa programul.

### f.

Da, putem considera imaginea un malware, deoarece are ca payload ascuns un executabil cu intentii malitioase.

## Ex 2

Vedem ca atunci cand citim parola nu verificam sa nu apara un buffer overflow. Din cum este pozitionata stiva, putem sa supra-scriem pass.
Asadar, daca executam programul si punem ca input "aaaaaaaaaaaaaa" o sa suprascrie si variabila "pass" si va acepta inputul.

Acest tip de atac se numeste stack buffer overflow attack.


