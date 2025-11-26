import rsa

message = "on test"

def rsa_encrypt(message):
    (pubkey, privkey) = rsa.newkeys(2048)
    encrypted_message = rsa.encrypt(message.encode(), pubkey)
    return encrypted_message, privkey

def rsa_decrypt(encrypted_message, privkey):
    decrypted_message = rsa.decrypt(encrypted_message, privkey).decode()
    return decrypted_message

encrypted_message, privkey = rsa_encrypt(message)
print(f"Message chiffré: {encrypted_message}")

decrypted_message = rsa_decrypt(encrypted_message, privkey)
print(f"Message déchiffré: {decrypted_message}")