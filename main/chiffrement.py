# Chiffrement César
def cesar_chiffrement(text, cesar_cle=3):
    result = ""
    for caractere in text.upper():
        if caractere.isalpha():
            ascci = ord(caractere) + cesar_cle
            result += chr((ascci - 65) % 26 + 65)
        else:
            result += caractere
    return result

# Déchiffrement César
def cesar_dechiffrement(text, cle=3):
    return cesar_chiffrement(text, -cle).lower()

# Chiffrement Vigenère
def vigenere_cipher(text, key):
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].lower()) - 97
            if char.isupper():
                result += chr(((ord(char) - 65 + shift) % 26) + 65)
            else:
                result += chr(((ord(char) - 97 + shift) % 26) + 97)
            key_index += 1
        else:
            result += char
    return result

# Déchiffrement Vigenère
def vigenere_decipher(text, key):
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].lower()) - 97
            if char.isupper():
                result += chr(((ord(char) - 65 - shift) % 26) + 65)
            else:
                result += chr(((ord(char) - 97 - shift) % 26) + 97)
            key_index += 1
        else:
            result += char
    return result.lower()


# Chiffrement global
def encrypt(text, cesar_cle=3, vigenere_cle="KEY"):
    text_cesar = cesar_chiffrement(text, cesar_cle)
    text_vigenere = vigenere_cipher(text_cesar, vigenere_cle)
    return text_vigenere

# Déchiffrement global
def decrypt(text, cesar_cle=3, vigenere_cle="KEY"):
    text_vigenere = vigenere_decipher(text, vigenere_cle)
    text_cesar = cesar_dechiffrement(text_vigenere, cesar_cle)
    return text_cesar
