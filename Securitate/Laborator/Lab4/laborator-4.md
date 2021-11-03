# Laborator 4 - Theodor Moroianu - 334

## 1. Notiuni Generale

A - 4
B - 2
C - 1
D - 3
E - 4
F - 5

## 2. Indentificarea vizuala

Elemente care sa indice faptul ca este vorba de un fishing sunt:
 * Clientul de email (Gmail / Outlook / Yahoo mail) a identificat emailul ca fiind "junk", probabil bazandu-se pe feedback-ul altor utilizatori.
 * Email-ul de pe care a fost trimis nu este un email din domeniul ing.ro, ci "externalys.net".
 * Titlul email-ului este de tipul click-bait - "mesaj important (1 ): ING.ro" cu greseli cum ar fi un spatiu in plus.
 * Mesajul este scris intr-un format foarte ne-profesional, fara taburi, fara numele utilizatorului si fara detalii aditionale.
 * Mesajul spune "ne cerem scuze pentru orice neplaceri", mesaj care nu s-ar gasi niciodata intr-un email legitim (probabil pentru a pregati utilizatorul ca va avea de introduce date personale).
 * Butonul "Valida" probabil ca duce la un site fals, care nu se afla pe domeniul ing.ro.

## 3. Analiza emailurilor de Fishing


Folosind site-ul https://emkei.cz/, and trimis un email spoofuit pe adresa mea personala.

Daca un astefel de atac ar reusi, atunci:
 * Am putea pretinde ca suntem alte entitati, precum o banca / un reprezentant legal etc.
 * Putem cere date cu caracter presonal, de exemplu pentru a updata contul bancar.
 * Etc.

Diferentele dintre emailul spoofuit si un email legitim sunt:
 * DMARC:
    Pe mailul legitim, checkul DMARC este validat de serverul GMAIL (DMARC:	'PASS'), pe cand pentru emailul fals, checkul pica (DMARC:	'FAIL').
 * DKIM:
    Pe mailul legitim, exista semnatura DKIM, care valideaza originea emailului ca fiind gmail.com.
    Pe mailul spoofuit, semnatura DKIM este inexistenta.
 * SPF:
    Pe mailul legitim, exista SPF-ul este validat, IP-ul fiind 209.85.220.41. Pe https://www.spf-record.com/spf-lookup/gmail.com putem verifica ca este intradevar un IP care depinde de gmail.com.
    Pe mailul spoofuit, IP-ul este 101-99-94-116, care nu este recunoscut ca IP din domeniul gmail.com.



