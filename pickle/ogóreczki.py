import hashlib
import pickle

# Dane wejściowe
data = "Pomocy"
key = "haslo"

# Tworzenie hasha z danych
objecthash = hashlib.sha256(data.encode())
print(objecthash)
data_hash_hex = objecthash.hexdigest()

# Konwersja hash na liczbę całkowitą
dataint = int(data_hash_hex, 16)

# Konwersja klucza na liczbę całkowitą
keyint = int.from_bytes(key.encode(), byteorder='big')

# Szyfrowanie XOR
resultat = dataint ^ keyint

# Odszyfrowanie XOR
unxor = resultat ^ keyint

# Sprawdzenie poprawności
if unxor == dataint:
    print("OK: Oryginalne dane zostały poprawnie odzyskane.")
else:
    print("NO: Oryginalne dane nie zostały poprawnie odzyskane.")

# Picklowanie danych (zapis do pliku)
with open("unxor_data.pkl", "wb") as file:
    pickle.dump(unxor, file)
    print("Dane zostały zapisane w pliku 'unxor_data.pkl'.")

# Odczyt z pliku i sprawdzenie
with open("unxor_data.pkl", "rb") as file:
    loaded_data = pickle.load(file)
    print("Dane odczytane z pliku:", loaded_data)

    # Sprawdzenie, czy odczytane dane są poprawne
    if loaded_data == unxor:
        print("OK: Dane odczytane poprawnie.")
    else:
        print("NO: Dane odczytane niepoprawnie.")
