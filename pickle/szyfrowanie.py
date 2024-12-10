import hashlib
import pickle
import zlib
from cryptography.fernet import Fernet

# Tworzenie klucza (robi się raz)
key1 = b'tGdYBJ0zcTDnrSgn8VdwtBlr2zDKUoMA3G9uXMHlBO8='
cipher_suite = Fernet(key1)

# Dane wejściowe
data = b"Pomocy"  # Musi być typu bytes
key = "wojtek"

# Tworzenie hasha z danych
objecthash = hashlib.sha256(data)  # Hashowanie danych binarnych
data_hash_hex = objecthash.hexdigest()

# Konwersja hash na liczbę całkowitą
dataint = int(data_hash_hex, 16)

# Konwersja klucza na liczbę całkowitą
keyint = int.from_bytes(key.encode(), byteorder="big")

# Szyfrowanie XOR
resultat = dataint ^ keyint
resultat =resultat.bit_length()
resultat = (resultat + 7) // 8
nowe = resultat.to_bytes(byteorder='big')

# Tworzenie buffera z szyfrowaniem i "zipem"
def new_buffer(buffer):
    print("OOB Data:", buffer)

    # Kompresowanie danych
    compressed_data = zlib.compress(buffer)

    # Szyfrowanie danych
    encrypted_data = cipher_suite.encrypt(compressed_data)

    # Logowanie skompresowanych i zaszyfrowanych danych
    print(f"OOB Data (compressed & encrypted): {encrypted_data}")

    # Zapisywanie zaszyfrowanych danych do pliku
    with open("compressed_encrypted_data.bin", "ab") as f:
        f.write(encrypted_data)

# Serializacja danych z obsługą bufora
with open("out_of_band_data.pkl", "wb") as file:
      pickle.dump(nowe, file, protocol=5, buffer_callback=new_buffer(nowe))

print("Klucz szyfrowania:", key1)
