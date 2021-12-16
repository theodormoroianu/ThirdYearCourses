from Crypto import Cipher
from Crypto.Cipher import DES

def get_key(x: int):
    return (16 * x).to_bytes(1, byteorder="little") + b'\x00\x00\x00\x00\x00\x00\x00'

crypted = dict()
plain_text = "Provocare MitM!!"

for nr in range(16):
    key = get_key(nr)
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = cipher.encrypt(plain_text)
    crypted[ciphertext] = key

encrypted_text = b"G\xfd\xdfpd\xa5\xc9'C\xe2\xf0\x84)\xef\xeb\xf9"

for nr in range(16):
    key = get_key(nr)
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = cipher.decrypt(encrypted_text)
    if ciphertext in crypted:
        print(f"Found key!!\nKey1 = {crypted[ciphertext]}, key2 = {key}")


"""
Found key!!
Key1 = b'\x80\x00\x00\x00\x00\x00\x00\x00', key2 = b'\xe0\x00\x00\x00\x00\x00\x00\x00'

"""