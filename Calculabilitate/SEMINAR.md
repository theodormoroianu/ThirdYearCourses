# Seminar Complexitate

## Seminar 1 Dumitran (14 Oct 2021) - Tema

### Masina turing care sa gasesasca `a^n b^n c^n`

Idee:

Luam cate un `a`, `b` si `c` pana am consumat tot inputul.



Starile masinii: `{ q1, q2, q3, q4, q5, q6 }`.

Alfabetul de intrare: `{ a, b, c }`.

Alfabetul masinii: `{ a, b, c, A, B, C, Blank }`.

Starea initiala: `q1`.

Starea finala: `q6`.

Tranzitiile:

 * Luam un a:
	`(q1, a) -> (q2, A, R)`
 * Inaintam pana dam de un b:
	`(q2, a) -> (q2, a, R)`
	`(q2, B) -> (a2, B, R)`
 * Luam un b:
	`(q2, b) -> (q3, B, R)`
 * Inaintam pana dam de un c:
	`(q3, b) -> (q3, b, R)`
	`(q3, C) -> (q3, C, R)`
 * Luam un c:
	`(q3, c) -> (q4, C, L)`
 * Mergem inapoi pana dam de un A:
	`(q4, a) -> (q4, a, L)`
	`(q4, b) -> (q4, b, L)`
	`(q4, c) -> (q4, c, L)`
	`(q4, B) -> (q4, B, L)`
	`(q4, C) -> (q4, C, L)`
 * Dam de un A:
	`(q4, A) -> (q1, A, R)`
 * Am terminat toti a:
	`(q1, B) -> (q5, B, R)`
 * Mergem pana dam de `Blank`:
	`(q5, B) -> (q5, B, R)`
	`(q5, C) -> (q5, C, R)`
 * Am dat de `Blank`:
	`(q5, Blank) -> (q6, Blank, L)`

### Masina turing pentru w wRev w (w + w reversed + w)



De inclus in masinile turing:
Idee + tranzitii + complexitate.


