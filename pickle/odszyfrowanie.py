from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decrypt_data(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Deszyfruje dane za pomocą AES w trybie CBC.

    Args:
        ciphertext (bytes): Zaszyfrowane dane w formacie bajtów.
        key (bytes): Klucz AES użyty do szyfrowania.
        iv (bytes): Wektor inicjalizujący (IV) użyty do szyfrowania.

    Returns:
        bytes: Odszyfrowane dane w formacie bajtów.
    """
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
    # Użyj zaszyfrowanych danych z programu szyfrującego
    encrypted_data = b"\x90\x93\t\x8ao\x11\xb0^ \x07\xd90\x12\\?\x8e\xec)\x91\x9e\xcd\xfc\xec\xa6E\xa0\x114'(H\x1b"  # Zaszyfrowane dane
    aes_key = b'\xf0\x0e\xca\xaf\xc1~\xd7\x9e\x82\xb0\xa8\x99\x9c\xbe\x02\x13\xdc%\x0b\x1a%f3\xf7\x96E\x93f4\xf8\xaa\xa4'  # Klucz AES
    aes_iv = b'\xba\xda\x94\xe4\xa4\xaf+k\xa1\xcb6\x01\x1b\xc0>g' # IV

    decrypted_data = decrypt_data(encrypted_data, aes_key, aes_iv)
    print("Odszyfrowane dane:", decrypted_data)
