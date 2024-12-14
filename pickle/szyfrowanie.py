from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom


def encrypt_data(data: bytes) -> tuple:
    """
    Szyfruje dane za pomocą AES w trybie CBC.

    Args:
        data (bytes): Dane do zaszyfrowania w formacie bajtów.

    Returns:
        tuple: Zaszyfrowane dane, klucz AES, wektor IV.
    """
    key = urandom(32)  # 256-bitowy klucz
    iv = urandom(16)  # 128-bitowy wektor inicjalizujący (IV)

    # Tworzenie szyfratora
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Padding do wielokrotności bloku (16 bajtów)
    padding_length = 16 - (len(data) % 16)
    padded_data = data + bytes([padding_length]) * padding_length

    # Szyfrowanie danych
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext, key, iv


# Przykład użycia
if __name__ == "__main__":
    data = b"Secret data in bytes"
    encrypted_data, aes_key, aes_iv = encrypt_data(data)
    print("Zaszyfrowane dane:", encrypted_data)
    print("Klucz AES:", aes_key)
    print("IV:", aes_iv)
