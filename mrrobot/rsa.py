import base64

try:
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP

except ImportError:  # Damn you, OS X

    import rsa, sys
    sys.modules['Crypto'] = rsa
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP


def read_key(filename):
    with open(filename, 'rt') as f:
        key = RSA.importKey(f.read())
    return key


def rsa_encrypt_string(public_key, plaintext):
    if not public_key.can_encrypt():
        raise ValueError("The provided key can't be used for encryption.")

    plaintext = plaintext.encode('utf-8')
    cipher = PKCS1_OAEP.new(public_key)
    b = cipher.encrypt(plaintext)
    b = base64.b64encode(b).decode('utf-8')
    return b


def rsa_decrypt_string(private_key, ciphertext):
    b = ciphertext.rstrip('\n')
    b = base64.b64decode(b)
    cipher = PKCS1_OAEP.new(private_key)
    b = cipher.decrypt(b)
    b = b.decode('utf-8')
    return b

