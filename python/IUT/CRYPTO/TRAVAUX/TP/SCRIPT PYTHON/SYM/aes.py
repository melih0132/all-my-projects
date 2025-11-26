from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# Clé secrète (doit avoir une taille de 16, 24, ou 32 octets pour AES-128, AES-192 ou AES-256)
key = get_random_bytes(16)  # Clé pour AES-128

# Génération d'un vecteur d'initialisation (IV) aléatoire
iv = get_random_bytes(16)

# Chiffrement
def encrypt(message, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_message = cipher.encrypt(message.encode('utf-8'))
    return base64.b64encode(iv + encrypted_message).decode('utf-8')

# Déchiffrement
def decrypt(encrypted_message, key):
    raw_data = base64.b64decode(encrypted_message)
    iv = raw_data[:16]
    encrypted_message = raw_data[16:]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted_message = cipher.decrypt(encrypted_message)
    return decrypted_message.decode('utf-8')

# Test
message = "Ceci est un message secret."
encrypted = encrypt(message, key, iv)
decrypted = decrypt(encrypted, key)

print(f"Message original : {message}")
print(f"Message chiffré : {encrypted}")
print(f"Message déchiffré : {decrypted}")