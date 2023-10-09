import pkcs11
import os

# Initialise our PKCS#11 library
lib = pkcs11.lib("aetpkss1.dll")

token = lib.get_token(token_label='ensaios')
data = b'INPUT DATA'
# Open a session on our token

with token.open(user_pin='1234') as session:
    # Generate an AES key in this session
    key = session.generate_key(pkcs11.KeyType.DES3)
    # Get an initialisation vector
    iv = session.generate_random(64) # AES blocks are fixed at 128 bits
    # Encrypt our data
    crypttext = key.encrypt(data, mechanism_param=iv)


print(crypttext)