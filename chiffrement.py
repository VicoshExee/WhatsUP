import Crypto.Random as  get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import rsa

#clé RSA
def generate_keys():
    public_key, private_key = rsa.newkeys(512)
    return public_key, private_key

#chiffrement RSA
def encrypt_message(message, public_key):
    return rsa.encrypt(message.encode(), public_key)

#déchiffrement RSA
def decrypt_message(encrypted_message, private_key):
    return rsa.decrypt(encrypted_message, private_key).decode()



#AES
#clé 256 bits AES
def generate_key():
    return get_random_bytes(32)

# Chiffrement AES
def AES_encrypt(text, key):
    iv = get_random_bytes(16)  # genere vi
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted_bytes).decode()

# Déchiffrement AES
def AES_decrypt(text, key):
    encrypted_bytes = base64.b64decode(text)
    iv = encrypted_bytes[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes[16:]), AES.block_size)
    return decrypted_bytes.decode()



# Chiffrement César
def cesar_encrypt(text, cle):
    result = ""
    for caractere in text.upper():
        if caractere.isalpha():
            ascci = ord(caractere) + cle
            result += chr((ascci - 65) % 26 + 65)
        else:
            result += caractere
    return result

# Déchiffrement César
def cesar_decrypt(text, cle):
    return cesar_encrypt(text, -cle).lower()

# Chiffrement Vigenère
def vigenere_encrypt(text, cle):
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(cle[key_index % len(cle)].lower()) - 97
            if char.isupper():
                result += chr(((ord(char) - 65 + shift) % 26) + 65)
            else:
                result += chr(((ord(char) - 97 + shift) % 26) + 97)
            key_index += 1
        else:
            result += char
    return result


# Déchiffrement Vigenère
def vigenere_decrypt(text, cle):
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(cle[key_index % len(cle)].lower()) - 97
            if char.isupper():
                result += chr(((ord(char) - 65 - shift) % 26) + 65)
            else:
                result += chr(((ord(char) - 97 - shift) % 26) + 97)
            key_index += 1
        else:
            result += char
    return result.lower()
