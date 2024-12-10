import zlib
from cryptography.fernet import Fernet

# Twój klucz szyfrowania Fernet (musisz go zapisać wcześniej)
key = b'foHlPTBjxu1WrOW3HGIiyll1FctGM8SoaZ_UDplK3Gg='  # Klucz Fernet wygenerowany wcześniej
cipher_suite = Fernet(key)

# Klucz XOR używany podczas szyfrowania
key_bytes = b"haslo"

def decrypt_data(file_path):
    try:
        # 1. Odczyt skompresowanych i zaszyfrowanych danych z pliku
        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        # 2. Deszyfrowanie danych za pomocą Fernet
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        # 3. Rozpakowanie skompresowanych danych za pomocą zlib
        decompressed_data = zlib.decompress(decrypted_data)

        # 4. Odwrócenie operacji XOR z kluczem
        original_data = bytes([decompressed_data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(decompressed_data))])

        return original_data.decode('utf-8')

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return None

# Ścieżka do pliku z danymi skompresowanymi i zaszyfrowanymi
file_path = "compressed_encrypted_data.bin"

# Odszyfrowanie danych
original_data = decrypt_data(file_path)

# Wyświetlenie oryginalnych danych
if original_data:
    print(f"Odszyfrowane dane: {original_data}")
