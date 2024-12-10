import hashlib
import pickle
import zlib
from cryptography.fernet import Fernet

# tworzenie klucza zrobione by to było raz
key1 = Fernet.generate_key()
cipher_suite = Fernet(key1)

# Dane wejściowe
data = "Pomocy"
key = "haslo"

# Tworzenie hasha z danych
objecthash = hashlib.sha256(
data.encode())  # Utworzenie sha256 jest dostępne 512 -> <sha256 _hashlib.HASH object @ 0x0000022D3CBFBBD0>
data_hash_hex = objecthash.hexdigest()  # Utworzenie z tego hexa

# Konwersja hash na liczbę całkowitą
dataint = int(data_hash_hex, 16)

# Konwersja klucza na liczbę całkowitą
keyint = int.from_bytes(key.encode(),byteorder='big')  # big oznacza jakieś coś jest jeszcze little (trochę nie zrozumiałem)

# Szyfrowanie XOR
resultat = dataint ^ keyint
#
# # Odszyfrowanie XOR
# unxor = resultat ^ keyint


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

with open("out_of_band_data.pkl", "wb") as file:
    # Zapisujemy dane do pliku z new_buffer
    pickle.dump(data, file, protocol=5, buffer_callback=new_buffer)
with open("out_of_band_data.pkl", "rb") as file:
    data = pickle.load(file)
print(data)
print(key1)