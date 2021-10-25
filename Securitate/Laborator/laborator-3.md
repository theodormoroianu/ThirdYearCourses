# Laborator 3 - Theodor Moroianu - 334

## On Time Pad

### Exercitiul 1

Folosing functia `base64`, am decompresat mesajul:

`$ base64 -d < mesaj1 > mesaj2`

Dupa, am executat urmatorul script:

```Python
with open('mesaj2', 'rb') as fin:
    data = fin.read()
cheie = "ecb181a479a6121add5b42264db9b44b4b48d7d93c62c56a3c3e1aba64c7517a90ed44f8919484b6ed8acc4670db62c249b9f5bada4ed474c9e4d111308b614788cd4fbdc1e949c1629e12fa5fdbd9"
ans = []
for i in range(0, len(cheie), 2):
    c = int(cheie[i:i+2], 16)
    ans.append(int(data[i // 2]) ^ c)

print("".join([chr(i) for i in ans]))
```

Outputul este `One Time Pad este un sistem de criptare perfect sigur daca este folosit corect.`

### Exercitiul 2

Putem sa gasim o cheie care sa dea output-ul bun.

Refolosind scriptul de la punctul 1, avem:

```Python
with open('mesaj2', 'rb') as fin:
    data = fin.read()
cheie = []
ans = ans = [ord(c) for c in 'Orice text clar poate obtinut dintr-un text criptat cu OTP dar cu o alta cheie.']

for i in range(len(ans)):
    rez = ans[i]
    init = int(data[i])
    c = rez ^ init
    cheie.append(c)

c = 0
for i in cheie:
    c = 256 * c + i

print(hex(c)[2:])
```

Output-ul este `ecad8de748ef0b1a857f032101bdb51f5e07c3c37931c37b3c3219ef748215708cf046a18588c1e2f897ca0076ca7f924eb1e6efcb1b905afed5d110228d24049b824cf2d3ec4980219208fa55cad9`

### Exercitiul 3

Daca refolosim cheia de la One-Time-Pad de mai multe ori, apar probleme de securitate.
Sa presupunem ca am trimis doua mesaje m1 si m2, ambele encryptate cu cheia k.

Cineva poate intercepta m1^k si m2^k, si deci xorandu-le poate afla m1^m2.

Desi pare oarecum inutil, putem sa aflam informatii despre mesaj. De exemplu, daca mesajul reprezinta intensitatea unor pixeli, atunci aflam practic "diferenta" de intensitate dintre cele doua poze.
Mai multe detalii sunt [aici](https://crypto.stackexchange.com/questions/59/taking-advantage-of-one-time-pad-key-reuse).


## Sisteme de Criptare Istorice

### Substitutie

Cel mai clasic sistem istoric de criptare cu substitutie este Caesar Cipher.
Fiecare litera este inlocuita cu o litera `X` pozitii mai departe in alfabet.
Sistemul nu este foarte securizat, avand in vedere ca exista numai 26 de posibilitati.

De exemplu, putem sa ne uitam la Caesar Cipher cu rotatie de `1`.
`Hello There!` => `Ifmmp Uifsf!`.

Pentru a decripta mesajul, este suficient sa facem transformarea inversa, scazand `1` din fiecare caracter (eventual si adaugand 26 daca trece de `a`).

Pentru a sparge sistemul, este suficient sa verificam cele `26` de posibilitati.

### Transpozitie

Cel mai simplu algoritm de criptare prin transpozitie este transpozitia prin coloane, in care scriem un cuvant pe linii si il citim pe coloane.

De exemplu, daca avem cuvantul `Hello there general`, si encodam pe 5 coloane, vom avea:

| H | e | l | l | o |
|---|---|---|---|---|
|   | t | h | e | r |
|---|---|---|---|---|
| e |   | g | e | n |
|---|---|---|---|---|
| e | r | a | l |   |

Care se traduce in `H eeet rlhgaleelorn`.

Pentru a il decripta, este suficient sa calculam cate linii sunt necesare (parte intreaga superioara de lungime pe numar de coloane), sa il scrim pe coloane si sa il citim din nou pe linii.

Pentru a sparge algoritmul, este suficient sa ne variem cate linii sunt, sa scriem cuvantul pe coloane si sa vedem daca este cel bun.

Securitatea criptarii nu este una inalta.

## Analiza de frecventa

Cu ajutorul site-ului `dcode.fr`, am gasit cheia de substitutie care este `UWSHACTIQEDBOLRMPGJXVYNKFZ`, si mesajul decodat este:

`ALICE AND BOB ARE THE WORLDS MOST FAMOUS CRYPTOGRAPHIC COUPLE. SINCE THEIR INVENTION IN 1978, THEY HAVE AT ONCE BEEN CALLED INSEPARABLE, AND HAVE BEEN THE SUBKECT OF NUMEROUS DIVORCES, TRAVELS, AND TORMENTS. IN THE ENSUING YEARS, OTHER CHARACTERS HAVE KOINED THEIR CRYPTOGRAPHICFAMILY. THERES EVE, THE PASSIVE AND SUBMISSIVE EAVESDROPPER, MALLORY THE MALICIOUS ATTACXER, AND TRENT, TRUSTED BY ALL, KUST TO NAME A FEW. WHILE ALICE, BOB, AND THEIR EJTENDED FAMILY WERE ORIGINALLY USED TO EJPLAIN HOW PUBLIC XEY CRYPTOGRAPHY WORXS, THEYHAVE SINCE BECOME WIDELY USED ACROSS OTHER SCIENCE AND ENGINEERING DOMAINS. THEIR INFLUENCE CONTINUES TO GROW OUTSIDE OF ACADEMIA AS WELL: ALICE AND BOB ARE NOW A PART OF GEEX LORE, AND SUBKECT TO NARRATIVES AND VISUAL DEPICTIONS THAT COMBINE PEDAGOGY WITH IN-KOXES, OFTEN REFLECTING OF THE SEJIST AND HETERONORMATIVE ENVIRONMENTS IN WHICH THEY WERE BORN AND CONTINUE TO BE USED. MORE THAN KUST THE WORLDS MOST FAMOUS CRYPTOGRAPHIC COUPLE, ALICE AND BOB HAVE BECOME AN ARCHETYPE OF DIGITAL EJCHANGE, AND A LENS THROUGH WHICH TO VIEW BROADER DIGITAL CULTURE. Q.DUPONT AND A.CATTAPAN CRYPTOCOUPLE`

## Enigma

1. Am preluat cheia din ziua de 25 de pe https://www.101computing.net/enigma-daily-settings-generator/.
2. Am setat cheia.
3. Numele meu criptat este QAIXQ CHFLX HGFLB.
4. Pentru a decripta texul, este suficient sa resetam masina enigma la starea initiala si sa introducem cypher textul. Obtinem din "QAIXQ CHFLX HGFLB" inapoi "THEOD ORMOR OIANU".
5. Nu se poate da un astfel de exemplu. Prin natura ei, operatiile masinei Enigma sunt reversibile, in sensul ca exista o bijectie intre toate textele criptate si toate textele necriptate de o anumita lungime (prin simplul motiv ca nu exista coliziuni si cele doua multimi au acelasi cardinal).
Asadar, orice text criptat este criptarea unui text normal de aceeasi lungime, care poate fi numele nostru (unii oameni au nume foarte ciudate).