import serial
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import urandom
import json
from functions.współnyklucz import generate_random_full_key
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

def encrypt_data(data: bytes) -> tuple:
    """
    Szyfruje dane za pomocą AES-GCM.

    Args:
        data (bytes): Dane do zaszyfrowania w formacie bajtów.

    Returns:
        tuple: Zaszyfrowane dane w bajtach, indeksy połówek klucza, IV w bajtach, tag w bajtach.
    """
    # Generowanie klucza z losowych połówek
    full_key, index1, index2 = generate_random_full_key("C:/Users/ninja/OneDrive/Pulpit/Praca/GUI-Charon/szyfrandodszyfr/half_keys_indexed.json")

    # Upewnij się, że klucz ma poprawną długość (256 bitów = 32 bajty)
    if len(full_key) != 32:
        raise ValueError("Klucz AES musi mieć 256 bitów (32 bajty).")

    # Generowanie losowego wektora IV
    iv = urandom(12)  # 96-bitowy wektor inicjalizujący (IV) dla AES-GCM
    debug_print("szyfr", f" [encrypt_data] (VI przed {iv.hex()}")

    # Tworzenie instancji AES-GCM
    aesgcm = AESGCM(full_key)

    # Szyfrowanie danych
    ciphertext = aesgcm.encrypt(iv, data, None)

    # Wyodrębnianie tagu autentyczności
    tag = ciphertext[-16:]  # Ostatnie 16 bajtów to tag
    encrypted_data = ciphertext[:-16]  # Reszta to zaszyfrowane dane

    return encrypted_data, index1, index2, iv, tag

def client_program(port: str, baudrate: int, data: bytes):
    """
    Klient wysyła dane wejściowe, indeksy połówek klucza, zaszyfrowane dane, IV i tag do odbiorcy LoRa.

    Args:
        port (str): Port szeregowy, do którego podłączony jest moduł LoRa.
        baudrate (int): Prędkość transmisji w bodach.
        data (bytes): Dane do zaszyfrowania i wysłania.
    """
    try:
        # Szyfrowanie danych
        encrypted_data, index1, index2, iv, tag = encrypt_data(data)
        debug_print("szyfr", f" [client_program] Indeks 1: {index1}")
        debug_print("szyfr", f" [client_program] Indeks 2: {index2}")
        debug_print("szyfr", f" [client_program] IV przed XOR: {iv.hex()}")

        # XOR na IV z index2
        iv = xor_iv_with_index(iv, load_key_from_json(index2, "C:/Users/ninja/OneDrive/Pulpit/Praca/GUI-Charon/szyfrandodszyfr/half_keys_indexed.json"))
        debug_print("szyfr", f" [client_program] IV po XOR: {iv.hex()}")

        debug_print("szyfr", f" [client_program] Tag: {tag.hex()}")

        # Przygotowanie wiadomości
        message = (index1.to_bytes(1, 'little') +
                   index2.to_bytes(1, 'big') +
                   iv +
                   encrypted_data +
                   tag)
        debug_print("szyfr", f" [client_program] Długość wiadomości w bajtach: {len(message)}")

        # Połączenie z modułem LoRa przez port szeregowy
        with serial.Serial(port, baudrate, timeout=1) as ser:
            # debug_print("szyfr", f" [client_program] Połączono z modułem LoRa na porcie {port} z prędkością {baudrate}.")

            # Wysyłanie wiadomości
            ser.write(message)

            # Odbieranie odpowiedzi
            response = ser.read(4096)
            try:
                response_text = response.decode('utf-8')
                debug_print("szyfr", f"Odebrane dane {response_text}")
            except UnicodeDecodeError:
                debug_print("szyfr", f"Odebrane dane nie są tekstem {response}")

    except Exception as e:
        debug_print("szyfr", f"Błąd klienta: {e}")

if __name__ == "__main__":
    while True:
        data = input("Podaj dane do zaszyfrowania: ").encode('utf-8')
        client_program("COM6", 9600, data)
