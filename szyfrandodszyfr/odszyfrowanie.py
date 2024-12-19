import socket
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import runtext1

def load_key_from_json(index: int, json_file: str) -> bytes:
    """
    �aduje po�ow� klucza z pliku JSON na podstawie indeksu.

    Args:
        index (int): Indeks klucza do za�adowania.
        json_file (str): �cie�ka do pliku JSON zawieraj�cego po�owy kluczy.

    Returns:
        bytes: Po�owa klucza w formacie bajt�w.
    """
    with open(json_file, "r") as file:
        half_keys = json.load(file)
    return bytes.fromhex(half_keys[str(index)])

def decrypt_data(message: str, json_file: str) -> str:
    """
    Odszyfrowuje dane zaszyfrowane za pomoc� AES w trybie CBC.
    Klucz i wektor IV s� wyodr�bniane z wiadomo�ci, a po�owy klucza s� �adowane z pliku JSON.

    Args:
        message (str): Zaszyfrowana wiadomo�� w formacie hex (index1:index2:data:ciphertext:iv).
        json_file (str): �cie�ka do pliku JSON zawieraj�cego po�owy kluczy.

    Returns:
        str: Odszyfrowane dane w formacie tekstowym.
    """
    # Rozdzielenie wiadomo�ci na sk�adowe
    parts = message.split(":")
    if len(parts) != 5:
        raise ValueError("Niepoprawny format wiadomo�ci.")

    index1 = int(parts[0], 16)  # Indeks pierwszej po�owy klucza
    index2 = int(parts[1], 16)  # Indeks drugiej po�owy klucza
    data_hex = parts[2]         # Oryginalne dane (hex) - nieu�ywane przy deszyfrowaniu
    ciphertext_hex = parts[3]   # Zaszyfrowane dane (hex)
    iv_hex = parts[4]           # IV (hex)

    # �adowanie po��wek klucza z pliku JSON
    key1 = load_key_from_json(index1, json_file)
    key2 = load_key_from_json(index2, json_file)

    # Po��czenie klucza
    full_key = key1 + key2

    # Konwersja IV i zaszyfrowanej wiadomo�ci z hex na bajty
    iv = bytes.fromhex(iv_hex)
    ciphertext = bytes.fromhex(ciphertext_hex)

    # Tworzenie deszyfratora
    cipher = Cipher(algorithms.AES(full_key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    # Deszyfrowanie danych
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Usuni�cie paddingu
    padding_length = padded_data[-1]
    if padding_length > 16 or padding_length == 0:
        raise ValueError("Padding nieprawid�owy.")
    plaintext = padded_data[:-padding_length]

    return plaintext.decode("utf-8")

def server_program(host: str, port: int, json_file: str):
    """
    Funkcja uruchamia serwer nas�uchuj�cy na podanym porcie, kt�ry deszyfruje wiadomo�ci.

    Args:
        host (str): Adres IP serwera.
        port (int): Port serwera.
        json_file (str): �cie�ka do pliku JSON zawieraj�cego po�owy kluczy.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Serwer nas�uchuje na {host}:{port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Po��czono z {addr}")

            encrypted_message = conn.recv(4096).decode('utf-8')
            print("Otrzymano zaszyfrowan� wiadomo��.")

            try:
                decrypted_data = decrypt_data(encrypted_message, json_file)
                print("Odszyfrowane dane (tekst):", decrypted_data)
                runtext1.display_text_on_matrix(decrypted_data)
                conn.sendall(b'Dane zostaly odpowiednio odszyfrowane.')
            except Exception as e:
                print(f"B��d podczas odszyfrowywania: {e}")
                conn.sendall(f"B��d: {e}".encode('utf-8'))

            conn.close()
    except KeyboardInterrupt:
        print("Serwer zosta� zatrzymany.")
        server_socket.close()

if __name__ == "__main__":
    json_file_path = "/home/kopis/GUI-Charon/szyfrandodszyfr/half_keys_indexed.json"
    server_program("192.168.1.2", 2137, json_file_path)
