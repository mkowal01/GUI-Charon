import socket
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import urandom
import json
from charon_library.Debuger import debug_print

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

def xor_iv_with_index(iv: bytes, index2: bytes) -> bytes:
    """
    Wykonuje operację XOR na wektorze IV i indeksie2.

    Args:
        iv (bytes): Wektor inicjalizujący (IV).
        index2 (int): Indeks drugiej połowy klucza.

    Returns:
        bytes: Zmodyfikowany wektor IV po operacji XOR.
    """
    index_bytes = index2[:len(iv)]  # Konwersja index2 do bajtów o długości IV
    return bytes(a ^ b for a, b in zip(iv, index_bytes))

def decrypt_data(message: bytes, json_file: str) -> str:
    """
    Odszyfrowuje dane zaszyfrowane za pomocą AES-GCM.
    Klucz i wektor IV są wyodrębniane z wiadomości, a połowy klucza są ładowane z pliku JSON.

    Args:
        message (bytes): Zaszyfrowana wiadomość w formacie bajtowym.
        json_file (str): Ścieżka do pliku JSON zawierającego połowy kluczy.

    Returns:
        str: Odszyfrowane dane w formacie tekstowym.
    """
    # Rozdzielenie wiadomości na składniki
    debug_print("odszyfr",f"Odebrana wiadomość (raw): {message}")
    index1 = message[0]  # Indeks pierwszej połowy klucza
    index2 = message[1]  # Indeks drugiej połowy klucza
    iv = message[2:14]   # IV (12 bajtów dla AES-GCM)
    tag = message[30:] # Tag (16 bajtów dla AES-GCM)
    ciphertext = message[14:30]  # Zaszyfrowane dane

    debug_print("odszyfr",f"Indeks 1: {index1}")
    debug_print("odszyfr",f"Indeks 2: {index2}")
    debug_print("odszyfr",f"IV przed XOR: {iv.hex()}")

    # XOR na IV z index2
    iv = xor_iv_with_index(iv, load_key_from_json(index2, "../charon_library/half_keys_indexed.json"))
    debug_print("odszyfr",f"IV po XOR: {iv.hex()}")

    debug_print("odszyfr",f"Tag: {tag.hex()}")
    debug_print("odszyfr",f"Zaszyfrowane dane: {ciphertext.hex()}")

    # Ładowanie połówek klucza z pliku JSON
    key1 = load_key_from_json(index1, json_file)
    key2 = load_key_from_json(index2, json_file)

    # Połączenie klucza
    full_key = key1 + key2

    # Tworzenie instancji AES-GCM
    aesgcm = AESGCM(full_key)

    # Deszyfrowanie danych
    try:
        plaintext = aesgcm.decrypt(iv, ciphertext + tag, None)
    except Exception as e:
        raise ValueError(f"Błąd deszyfrowania: {e}")

    return plaintext.decode("utf-8")

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
    debug_print("odszyfr",f"Serwer nasłuchuje na {host}:{port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            debug_print("odszyfr",f"Połączono z {addr}")

            encrypted_message = conn.recv(4096)
            print("Otrzymano zaszyfrowaną wiadomość.")

            try:
                decrypted_data = decrypt_data(encrypted_message, json_file)
                print("Odszyfrowane dane (tekst):", decrypted_data)
                conn.sendall(b'ACK')
            except Exception as e:
                debug_print("odszyfr",f"Błąd podczas odszyfrowywania: {e}")
                conn.sendall(f"Błąd: {e}".encode('utf-8'))

            conn.close()
    except KeyboardInterrupt:
        debug_print("odszyfr",f"Serwer został zatrzymany.")
        server_socket.close()

if __name__ == "__main__":
    json_file_path = "../charon_library/half_keys_indexed.json"
    server_program("192.168.1.3", 2137, json_file_path)
