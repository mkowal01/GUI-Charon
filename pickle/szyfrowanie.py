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
        tuple: Zaszyfrowane dane w bitach, indeksy połówek klucza, wektor IV w bitach.
    """
    # Generowanie klucza z losowych połówek
    full_key, index1, index2 = wspolnyklucz.generate_random_full_key("half_keys_indexed.json")

    # Upewnij się, że klucz ma poprawną długość (256 bitów = 32 bajty)
    if len(full_key) != 32:
        raise ValueError("Klucz AES musi mieć 256 bitów (32 bajty).")

    # Generowanie losowego wektora IV
    iv = urandom(16)  # 128-bitowy wektor inicjalizujący (IV)

    # Tworzenie szyfratora
    cipher = Cipher(algorithms.AES(full_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    # Padding do wielokrotności bloku (16 bajtów)
    padding_length = 16 - (len(data) % 16)
    padded_data = data + bytes([padding_length]) * padding_length

    # Szyfrowanie danych
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Konwersja zaszyfrowanych danych na bity
    ciphertext_bits = ''.join(format(byte, '08b') for byte in ciphertext)

    # Konwersja IV na bity
    iv_bits = ''.join(format(byte, '08b') for byte in iv)

    # Dodanie indeksów i odpowiednich separatorów
    index1_bits = f"{index1:08b}"
    index2_bits = f"{index2:08b}"
    final_ciphertext = (
        index1_bits + "10101010" + index2_bits + ciphertext_bits + "01010101" + iv_bits
    )

    return final_ciphertext, index1, index2, iv_bits

def client_program(host: str, port: int, data: bytes):
    """
    Klient wysyła indeksy połówek klucza, zaszyfrowane dane i IV do serwera.

    Args:
        host (str): Adres IP serwera.
        port (int): Port serwera.
        data (bytes): Dane do zaszyfrowania i wysłania.
    """
    try:
        # Szyfrowanie danych
        encrypted_data_bits, index1, index2, iv_bits = encrypt_data(data)

        # Przygotowanie wiadomości
        message = encrypted_data_bits
        print(len(encrypted_data_bits))
        # Połączenie z serwerem
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Połączono z serwerem {host}:{port}")

        # Wysyłanie zaszyfrowanych danych, indeksów klucza i IV
        client_socket.sendall(message.encode('utf-8'))
        print(len(message))
        print("Dane zostały wysłane.")

        # Odbieranie odpowiedzi
        response = client_socket.recv(4096).decode('utf-8')
        print("Odpowiedź serwera:", response)

        client_socket.close()
    except Exception as e:
        print(f"Błąd klienta: {e}")

if __name__ == "__main__":
    data = input("Podaj dane do zaszyfrowania: ").encode('utf-8')

    client_program("192.168.82.183", 2137, data)