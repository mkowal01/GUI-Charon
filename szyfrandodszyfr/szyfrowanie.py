import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom
import functions.współnyklucz as wspolnyklucz

def encrypt_data(data: bytes) -> tuple:
    """
    Szyfruje dane za pomocą AES w trybie CBC.

    Args:
        data (bytes): Dane do zaszyfrowania w formacie bajtów.

    Returns:
        tuple: Dane wejściowe w hex, zaszyfrowane dane w hex, indeksy połówek klucza, IV w hex.
    """
    # Konwersja danych wejściowych do hex
    data_hex = data.hex()

    # Generowanie klucza z losowych połówek
    full_key, index1, index2 = wspolnyklucz.generate_random_full_key("/home/kopis/GUI-Charon/szyfrandodszyfr/half_keys_indexed.json")

    # Upewnij się, że klucz ma poprawną długość (256 bitów = 32 bajty)
    if len(full_key) != 32:
        raise ValueError("Klucz AES musi mieć 256 bitów (32 bajty).")

    # Generowanie losowego wektora IV
    iv = urandom(16)  # 128-bitowy wektor inicjalizujący (IV)

    # Tworzenie szyfratora
    cipher = Cipher(algorithms.AES(full_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Padding do wielokrotności bloku (16 bajtów)
    data_bytes = bytes.fromhex(data_hex)
    padding_length = 16 - (len(data_bytes) % 16)
    padded_data = data_bytes + bytes([padding_length]) * padding_length

    # Szyfrowanie danych
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Konwersja zaszyfrowanych danych oraz IV na format hex
    ciphertext_hex = ciphertext.hex()
    iv_hex = iv.hex()

    return data_hex, ciphertext_hex, index1, index2, iv_hex

def client_program(host: str, port: int, data: bytes):
    """
    Klient wysyła dane wejściowe, indeksy połówek klucza, zaszyfrowane dane i IV do serwera.

    Args:
        host (str): Adres IP serwera.
        port (int): Port serwera.
        data (bytes): Dane do zaszyfrowania i wysłania.
    """
    try:
        # Szyfrowanie danych
        data_hex, encrypted_data_hex, index1, index2, iv_hex = encrypt_data(data)

        # Przygotowanie wiadomości
        message = f"{index1:02x}:{index2:02x}:{data_hex}:{encrypted_data_hex}:{iv_hex}"
        print("Długość wiadomości HEX:", len(message))

        # Połączenie z serwerem
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Połączono z serwerem {host}:{port}")

        # Wysyłanie wiadomości
        client_socket.sendall(message.encode('utf-8'))
        print("Dane zostały wysłane w HEX.")

        # Odbieranie odpowiedzi
        response = client_socket.recv(4096).decode('utf-8')
        print("Odpowiedź serwera:", response)

        client_socket.close()
    except Exception as e:
        print(f"Błąd klienta : {e}")

if __name__ == "__main__":
    data = input("Podaj dane do zaszyfrowania: ").encode('utf-8')
    client_program("192.168.1.2", 2137, data)
