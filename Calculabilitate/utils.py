def make_pair(a: int, b: int):
    return 2**a * (2*b+1) - 1

def left(x: int):
    ans = 0
    x += 1
    while x % 2 == 0:
        ans += 1
        x //= 2
    return ans

def right(x: int):
    val_left = left(x)
    x += 1
    x //= 2**val_left
    x -= 1
    return x // 2


def is_prime(x):
    for i in range(2, x):
        if x % i == 0:
            return False
    return True

def get_x_th_prime(x: int):
    """
        Index from 1
    """
    for i in range(2, 10**10):
        if is_prime(i):
            x -= 1
        if x == 0:
            return i

def get_godel(arr: list):
    nr = 1
    for poz, val in enumerate(arr):
        prime = get_x_th_prime(poz + 1)
        nr *= prime ** val

    return nr

def get_list_from_godel(nr):
    arr = []
    for i in range(1, 10**10):
        if nr == 1:
            return arr
        prime = get_x_th_prime(i)
        put = 0
        while nr % prime == 0:
            put += 1
            nr /= prime
        arr.append(put)
    return arr