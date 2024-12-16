import socket
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import runtext1

def load_key_from_json(index: int, json_file: str) -> bytes:
    """
    Ładuje połowę klucza z pliku JSON na podstawie indeksu.

    Args:
        index (int): Indeks klucza do załadowania.
        json_file (str): Ścieżka do pliku JSON zawierającego połowy kluczy.

    Returns:
        bytes: Połowa klucza w formacie bajtów.
    """
    with open(json_file, "r") as file:
        half_keys = json.load(file)
    return bytes.fromhex(half_keys[str(index)])

def decrypt_data(encrypted_bits: str, json_file: str) -> bytes:
    """
    Odszyfrowuje dane zaszyfrowane za pomocą AES w trybie CBC.
    Klucz i wektor IV są wyodrębniane z wiadomości, a połowy klucza są ładowane z pliku JSON.

    Args:
        encrypted_bits (str): Zaszyfrowane dane w postaci ciągu bitów.
        json_file (str): Ścieżka do pliku JSON zawierającego połowy kluczy.

    Returns:
        bytes: Odszyfrowane dane w formacie bajtów.
    """
    # Rozdzielenie wiadomości na składowe
    index1_bits = encrypted_bits[:8]  # Indeks pierwszej połowy klucza (8 bitów)
    index2_bits = encrypted_bits[16:24]  # Indeks drugiej połowy klucza (8 bitów)
    ciphertext_bits = encrypted_bits[24:-136]  # Zaszyfrowana wiadomość
    iv_bits = encrypted_bits[-128:]  # Wektor IV (128 bitów)

    # Konwersja indeksów z bitów na liczby całkowite
    index1 = int(index1_bits, 2)
    index2 = int(index2_bits, 2)

    # Ładowanie połówek klucza z pliku JSON
    key1 = load_key_from_json(index1, json_file)
    key2 = load_key_from_json(index2, json_file)

    # Połączenie klucza
    full_key = key1 + key2

    # Konwersja IV i zaszyfrowanej wiadomości z bitów na bajty
    iv = bytes(int(iv_bits[i:i+8], 2) for i in range(0, len(iv_bits), 8))
    ciphertext = bytes(int(ciphertext_bits[i:i+8], 2) for i in range(0, len(ciphertext_bits), 8))

    # Tworzenie deszyfratora
    cipher = Cipher(algorithms.AES(full_key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    # Deszyfrowanie danych
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Usunięcie paddingu
    padding_length = padded_data[-1]
    if padding_length > 16 or padding_length == 0:
        raise ValueError("Padding nieprawidłowy.")
    plaintext = padded_data[:-padding_length]

    return plaintext

def server_program(host: str, port: int, json_file: str):
    """
    Funkcja uruchamia serwer nasłuchujący na podanym porcie, który deszyfruje wiadomości.

    Args:
        host (str): Adres IP serwera.
        port (int): Port serwera.
        json_file (str): Ścieżka do pliku JSON zawierającego połowy kluczy.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Serwer nasłuchuje na {host}:{port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Połączono z {addr}")

            encrypted_message = conn.recv(4096).decode('utf-8')
            print("Otrzymano zaszyfrowaną wiadomość.")

            try:
                decrypted_data = decrypt_data(encrypted_message, json_file)
                print("Odszyfrowane dane (tekst):", decrypted_data.decode('utf-8'))
                runtext1.display_text_on_matrix(decrypted_data.decode('utf-8'))
                conn.sendall(b'Dane zostaly odpowiednie.')
            except Exception as e:

                print(f"Błąd podczas odszyfrowywania: {e}")
                conn.sendall(f"Błąd: {e}".encode('utf-8'))

            conn.close()
    except KeyboardInterrupt:
        print("Serwer został zatrzymany.")
        server_socket.close()

if __name__ == "__main__":
    json_file_path = "/home/kopis/GUI-Charon/szyfrandodszyfr/half_keys_indexed.json"
    data = server_program("192.168.1.2", 2137, json_file_path)
    