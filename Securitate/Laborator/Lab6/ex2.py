#%%

import secrets
import hashlib
import time

#%%

"""
    Genereaza un password "safe" din punct de vedere al securitatii.
    Poate fi util pentru:
        * Crearea unei parole by-default pentru un user (daca trebuie creat contul acestuia inainte ca el sa isi poata seta parola, urmand ca el sa o schimbe in viitor).
        * Sugestia automata de parole (cum ar fi in Google Chrome sau Firefox).
"""

def generate_strong_password(length=-1, big_letter=True, small_letter=True, digit=True, special_chr=True):
    big_letters = [chr(i) for i in range(ord('A'), ord('A') + 26)]
    small_letters = [chr(i) for i in range(ord('a'), ord('a') + 26)]
    digits = [chr(i) for i in range(ord('0'), ord('0') + 10)]
    specials = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_']
    all = big_letters + small_letters + digits + specials

    if length == -1:
        length = secrets.choice([i for i in range(10, 20)])

    while True:
        generated = ''.join([secrets.choice(all) for _ in range(length)])
        has_big, has_small, has_digit, has_special = False, False, False, False

        for c in generated:
            has_big |= (c in big_letters)
            has_small |= (c in small_letters)
            has_digit |= (c in digits)
            has_special |= (c in specials)

        if has_big and has_small and has_digit and has_special:
            return generated


# %%

"""
    Genereaza un url safe.
    Poate fi folosit:
     * Pentru o aplicatie cum ar fi Google Drive, unde dorim sa avem un folder partajat oamenilor care detin URL-ul, dar care nu poate fi ghicit.
     * Pentru a crea pagini care sa nu fie inchise in spatele unui sistem de autentificare, dar care totusi nu sunt disponibile decat celor care detin URL-ul la acea pagina.
"""

def generate_safe_URL(website='', length=-1):
    if length == -1:
        length = 32
    url = ''
    while len(url) < length:
        url += secrets.token_urlsafe()
    
    return website + url[:length]

# %%


"""
    Genereaza un token hexazecimal.
    Poate fi folosit:
     * 
"""

def generate_hexa_str(length=-1):
    if length == -1:
        length = 32

    token = ''
    while len(token) < length:
        token += secrets.token_hex()
    
    return token[:length]
# %%

"""
    Vrem sa verificam doua secvente, evidand timing attack.
    La ce trebuie sa fim atenti:
     * Sa nu ne oprim la primul mismatch.
     * Sa nu ne oprim la sfarsitul secventei bune (ca sa nu se poata afla lungimea).
"""

def safe_compare(good_str, check_str):
    """
        Want to check if good_str (the secret) is equal to check_str
    """
    
    # nr of positions we have to match
    left_to_match = len(good_str) if len(good_str) == len(check_str) else 10**9

    for i in range(len(check_str)):
        if i < len(good_str):
            left_to_match -= 1 if good_str[i] == check_str[i] else 0
        else:
            pass

    # Wait a few nano secs to be sure
    wait_time = secrets.choice([i for i in range(10)])
    time.sleep(wait_time * 1e-9)

    return left_to_match == 0

#%%

"""
    Genereaza o cheie fluida binara.
"""

def generate_binary_key(length=-1):
    if length == -1:
        length = 100

    return secrets.token_bytes(length)


# %%

"""
    Salveza parole in mod securizat.
    Salvam parola hashuita, cu un salt. Facem asta pentru:
     1. Chiar daca se leakuieste baza de date, nu se vor afla parolele.
     2. Chiar daca cineva afla hashul parolei altcuiva, nu se poate autentifica nici macar pe platforma noastra ca acel user.
     3. Daca s-a leakuit baza de date, putem schimba salt-ul si cere userilor sa isi reseteze parola.
     4. Salt-ul schimba radical hashurile, acestea nemaiputand fi checkuite cu rainbow tables.
"""

# chosen at random
salt = 'fsociety'
# should be in a db somewhere
users = dict()

def hash(password: str):
    return hashlib.sha256((password + salt).encode('utf-8')).digest()

def add_user(user: str, password: str):
    password = hash(password)

    if user in users:
        raise Exception("User already exists")
    
    users[user] = password

def change_password(user: str, old_password: str, new_password: str):
    old_password = hash(old_password)
    new_password = hash(new_password)

    if user not in users:
        raise Exception("User doesn't exist!")
    
    # maybe use a safe check, to avoid timing attack?
    if old_password != users[user]:
        raise Exception("Old password doesn't match!")
    
    users[user] = new_password

def authenticate(user: str, password: str) -> bool:
    password = hash(password)
    
    # maybe use safe check
    if user not in users or users[user] != password:
        return False
    return True


# %%
