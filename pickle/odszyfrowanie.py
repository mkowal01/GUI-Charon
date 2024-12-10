
key1 = b'tGdYBJ0zcTDnrSgn8VdwtBlr2zDKUoMA3G9uXMHlBO8='  # Klucz Fernet wygenerowany wcześniej
import zlib
from cryptography.fernet import Fernet

cipher_suite = Fernet(key1)

# Odczytanie zaszyfrowanych danych z pliku
with open("compressed_encrypted_data.bin", "rb") as f:
    encrypted_data = f.read()

# Odszyfrowanie danych
compressed_data = cipher_suite.decrypt(encrypted_data)
print(compressed_data)
# Zdekompresowanie danych
buffer = zlib.decompress(compressed_data)
print(buffer)
# Odszyfrowanie XOR (zamiana danych binarnych na int)
xor = int.from_bytes(buffer, byteorder="big")
print(xor)

# Klucz do XOR
key = "wojtek"
keyint = int.from_bytes(key.encode(), byteorder="big")

# Odszyfrowanie danych XOR
original_data = xor ^ keyint

# Zamiana z int na hash i dalej na oryginalne dane
data_hex = hex(original_data)[2:]  # Zamiana na ciąg heksadecymalny
retrieved_data = bytes.fromhex(data_hex)

print("Oryginalne dane:", retrieved_data.decode())
#b'gAAAAABnWM0qliVznSWzZPSNH6xssxuZnEHzmVcQO58FzaoGvmgRyw8cGMBC6B_rBDiJ13OvidZ5eCpkGx_fvSctN6ndfnFp5A=='