
import base64

CRYPT_KEY = '49dK7YOW6QgIPb9w' # TODO add option for custom key

# Vigenère cipher + base64
def encrypt(string, key=CRYPT_KEY):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    encoded_string = encoded_string.encode('latin')
    return base64.urlsafe_b64encode(encoded_string).decode("utf-8").rstrip('=')

def decrypt(string, key=CRYPT_KEY):
    string = base64.urlsafe_b64decode(string + '===')
    string = string.decode('latin')
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string
