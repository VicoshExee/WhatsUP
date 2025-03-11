import random

def cle_generate():
    p = 90703 # nb premier
    g = 5  # Base 
    private_key = random.randint(1, p - 1)
    public_key = (g ** private_key) % p
    return p, g, private_key, public_key

def echange_secret(private_key, received_public_key, p):
    return (received_public_key ** private_key) % p