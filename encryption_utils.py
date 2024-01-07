import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=algorithms.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(key, file_path, output_path):
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(output_path, 'wb') as encrypted_file:
        encrypted_file.write(iv + ciphertext)

def decrypt_file(key, file_path, output_path):
    with open(file_path, 'rb') as encrypted_file:
        data = encrypted_file.read()

    iv = data[:16]
    ciphertext = data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    with open(output_path, 'wb') as decrypted_file:
        decrypted_file.write(plaintext)

def send_file(connection, file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()

    connection.sendall(data)

def receive_file(connection, file_path, key):
    data = connection.recv(1024)
    with open(file_path, 'wb') as file:
        while data:
            file.write(data)
            data = connection.recv(1024)
