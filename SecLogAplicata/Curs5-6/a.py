
def break_cypher(enc_k_k):
    """
    Input: 
        * encodarea cu cheia K al lui k
        * modulul m, unde m este par
    Output:
        Cheia k - corecta cu o probabilitate de 1/2^n
    """

    # Toate elementele sunt pare, fiind ca enc_k_k este 2*k, in Z2t
    # le impartim asadar ca numere intregi, ceea ce este corect
    # cu o probabilitate de 1/2 pentru fiecare pozitie din sirul
    # de lungime n
    k = [x // 2 for x in enc_k_k]

    return k

# b
A = [1, 2, 5, 6, 7, 9]
B = [1, 3, 4, 5, 8, 9]
C = [2, 3, 4, 6, 7, 8]

a_egal_b = []
b_egal_c = []
c_egal_a = []

for i in A:
    for j in B:
        if i == j:
            a_egal_b.append((i, j))


for i in B:
    for j in C:
        if i == j:
            b_egal_c.append((i, j))


for i in C:
    for j in A:
        if i == j:
            c_egal_a.append((i, j))

print(f"Perechile cu A = B: {a_egal_b}")
print(f"P(A = B) = {len(a_egal_b)}/36 = {len(a_egal_b) / 36}")

print(f"Perechile cu B = C: {b_egal_c}")
print(f"P(B = C) = {len(b_egal_c)}/36 = {len(b_egal_c) / 36}")

print(f"Perechile cu C = A: {c_egal_a}")
print(f"P(C = A) = {len(c_egal_a)}/36 = {len(c_egal_a) / 36}")



# a
# A = [1, 2, 5, 6, 7, 9]
# B = [1, 3, 4, 5, 8, 9]
# C = [2, 3, 4, 6, 7, 8]

# nr_a_mai_mare_b = []
# nr_b_mai_mare_c = []
# nr_c_mai_mare_a = []

# for i in A:
#     for j in B:
#         if i > j:
#             nr_a_mai_mare_b.append((i, j))


# for i in B:
#     for j in C:
#         if i > j:
#             nr_b_mai_mare_c.append((i, j))


# for i in C:
#     for j in A:
#         if i > j:
#             nr_c_mai_mare_a.append((i, j))

# print(f"Perechile cu A > B: {nr_a_mai_mare_b}")
# print(f"P(A > B) = {len(nr_a_mai_mare_b)}/36 = {len(nr_a_mai_mare_b) / 36}")

# print(f"Perechile cu B > C: {nr_b_mai_mare_c}")
# print(f"P(B > C) = {len(nr_b_mai_mare_c)}/36 = {len(nr_b_mai_mare_c) / 36}")

# print(f"Perechile cu C > A: {nr_c_mai_mare_a}")
# print(f"P(C > A) = {len(nr_c_mai_mare_a)}/36 = {len(nr_c_mai_mare_a) / 36}")


