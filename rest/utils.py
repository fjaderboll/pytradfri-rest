
import base64
import os

CRYPT_KEY = None
def get_crypt_key():
    global CRYPT_KEY

    if CRYPT_KEY is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        crypt_key_file = f'{base_dir}/crypt.key'
        if os.path.exists(crypt_key_file):
            with open(crypt_key_file, 'r') as f:
                CRYPT_KEY = f.read().strip()
        else:
            CRYPT_KEY = '49dK7YOW6QgIPb9w' # kept for backward compatibility when this was hardcoded
    
    return CRYPT_KEY

# Vigenère cipher + base64
def encrypt(string):
    crypt_key = get_crypt_key()
    encoded_chars = []
    for i in range(len(string)):
        key_c = crypt_key[i % len(crypt_key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    encoded_string = encoded_string.encode('latin')
    return base64.urlsafe_b64encode(encoded_string).decode("utf-8").rstrip('=')

def decrypt(string):
    crypt_key = get_crypt_key()
    string = base64.urlsafe_b64decode(string + '===')
    string = string.decode('latin')
    encoded_chars = []
    for i in range(len(string)):
        key_c = crypt_key[i % len(crypt_key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string
