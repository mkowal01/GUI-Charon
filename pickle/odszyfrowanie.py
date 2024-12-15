from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decrypt_data(ciphertext_bits: str, key: bytes, iv: bytes) -> bytes:
    """
    Deszyfruje dane za pomocą AES w trybie CBC, przyjmując zaszyfrowane dane jako ciąg bitów.

    Args:
        ciphertext_bits (str): Zaszyfrowane dane w bitach.
        key (bytes): Klucz AES w bajtach.
        iv (bytes): Wektor IV w bajtach.

    Returns:
        bytes: Odszyfrowane dane w formacie bajtów.
    """
    # Konwersja z bitów do bajtów
    ciphertext = bytes(int(ciphertext_bits[i:i + 8], 2) for i in range(0, len(ciphertext_bits), 8))

    # Tworzenie deszyfratora
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    # Deszyfrowanie danych
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Usunięcie paddingu
    padding_length = padded_data[-1]
    plaintext = padded_data[:-padding_length]

    return plaintext


# Przykład użycia
if __name__ == "__main__":
    # Dane z programu szyfrującego
    encrypted_data_bits = "..."  # Zaszyfrowane dane w bitach
    aes_key = b"..."  # Klucz AES w bajtach
    aes_iv = b"..."  # IV w bajtach

    decrypted_data = decrypt_data(encrypted_data_bits, aes_key, aes_iv)
    print("Odszyfrowane dane:", decrypted_data)
