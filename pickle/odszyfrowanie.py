import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def decrypt_data(encrypted_bits: str) -> bytes:
    """
    Odszyfrowuje dane zaszyfrowane za pomocą AES w trybie CBC.
    Klucz i wektor IV są wyodrębniane z wiadomości.

    Args:
        encrypted_bits (str): Zaszyfrowane dane w postaci ciągu bitów.

    Returns:
        bytes: Odszyfrowane dane w formacie bajtów.
    """
    # Rozdzielenie wiadomości na składowe
    key1_bits = encrypted_bits[:128]  # Pierwsze 16 bajtów klucza (128 bitów)
    key2_bits = encrypted_bits[136:264]  # Kolejne 16 bajtów klucza (128 bitów)
    ciphertext_bits = encrypted_bits[264:-136]  # Zaszyfrowana wiadomość
    iv_bits = encrypted_bits[-128:]  # Wektor IV (128 bitów)

    # Konwersja klucza i IV z bitów na bajty
    key1 = bytes(int(key1_bits[i:i+8], 2) for i in range(0, len(key1_bits), 8))
    key2 = bytes(int(key2_bits[i:i+8], 2) for i in range(0, len(key2_bits), 8))
    iv = bytes(int(iv_bits[i:i+8], 2) for i in range(0, len(iv_bits), 8))

    # Połączenie klucza
    full_key = key1 + key2

    # Konwersja zaszyfrowanej wiadomości z bitów na bajty
    ciphertext = bytes(int(ciphertext_bits[i:i+8], 2) for i in range(0, len(ciphertext_bits), 8))

    # Tworzenie deszyfratora
    cipher = Cipher(algorithms.AES(full_key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    # Deszyfrowanie danych
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Usunięcie paddingu
    padding_length = padded_data[-1]
    plaintext = padded_data[:-padding_length]

    return plaintext

def server_program(host: str, port: int):
    """
    Funkcja uruchamia serwer nasłuchujący na podanym porcie, który deszyfruje wiadomości.
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
            print(encrypted_message)
            print("Otrzymano zaszyfrowaną wiadomość.")

            try:
                decrypted_data = decrypt_data(encrypted_message)
                print("Odszyfrowane dane (tekst):", decrypted_data.decode('utf-8'))
                print(decrypted_data)
            except Exception as e:
                print(f"Błąd podczas odszyfrowywania: {e}")
                conn.sendall(f"Błąd: {e}".encode('utf-8'))

            conn.close()
    except KeyboardInterrupt:
        print("Serwer został zatrzymany.")
        server_socket.close()

if __name__ == "__main__":

    server_program("192.168.82.183", 2137)
