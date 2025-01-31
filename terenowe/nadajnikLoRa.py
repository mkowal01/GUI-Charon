import serial
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import urandom
import json
from functions.współnyklucz import generate_random_full_key
from datetime import datetime

def load_key_from_json(index: int, json_file: str) -> bytes:
    with open(json_file, "r") as file:
        half_keys = json.load(file)
    return bytes.fromhex(half_keys[str(index)])

def xor_iv_with_index(iv: bytes, index2: bytes) -> bytes:
    index_bytes = index2[:len(iv)]
    return bytes(a ^ b for a, b in zip(iv, index_bytes))

def encrypt_data(data: bytes) -> tuple:
    full_key, index1, index2 = generate_random_full_key("../charon_library/half_keys_indexed.json")

    if len(full_key) != 32:
        raise ValueError("Klucz AES musi mieć 256 bitów (32 bajty).")

    iv = urandom(12)
    aesgcm = AESGCM(full_key)
    ciphertext = aesgcm.encrypt(iv, data, None)
    tag = ciphertext[-16:]
    encrypted_data = ciphertext[:-16]

    return encrypted_data, index1, index2, iv, tag

def client_program(port: str, baudrate: int):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            while True:
                data = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f").encode('utf-8')
                encrypted_data, index1, index2, iv, tag = encrypt_data(data)

                iv = xor_iv_with_index(iv, load_key_from_json(index2, "../charon_library/half_keys_indexed.json"))

                message = (index1.to_bytes(1, 'little') +
                           index2.to_bytes(1, 'big') +
                           iv +
                           encrypted_data +
                           tag)

                ser.write(message)
                print(f"Wysłano zaszyfrowaną wiadomość: {data.decode('utf-8')} (długość: {len(message)} bajtów)")

                response_text = ""
                while not response_text:
                    if ser.in_waiting > 0:
                        response_text = ser.readline().decode('ascii', errors='ignore').strip()
                        print(f"Wysłano zaszyfrowaną wiadomość: {data.decode('utf-8')} (długość: {len(message)} bajtów)")

    except Exception as e:
        print(f"Błąd klienta: {e}")

if __name__ == "__main__":
    client_program("COM9", 9600)
