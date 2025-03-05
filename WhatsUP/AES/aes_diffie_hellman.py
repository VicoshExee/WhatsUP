import random
import hashlib
import Crypto.Util.number as cun
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

rand = random.SystemRandom()

def generate_keys():
    p = cun.getPrime(512)
    g = 5
    private_key = rand.randrange(2, p - 1)
    public_key = pow(g, private_key, p)
    return p, g, private_key, public_key

def shared_key(public_key, private_key, p):
    return pow(public_key, private_key, p)

def encrypt_message(message: str, shared_key: int):
    key = hashlib.sha256(cun.long_to_bytes(shared_key)).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=b'\x00' * 16)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return ciphertext.hex()

def decrypt_message(ciphertext: str, shared_key: int):
    key = hashlib.sha256(cun.long_to_bytes(shared_key)).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=b'\x00' * 16)
    decrypted = unpad(cipher.decrypt(bytes.fromhex(ciphertext)), AES.block_size)
    return decrypted.decode()

