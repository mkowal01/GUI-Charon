import json
import random
from typing import Tuple

def generate_random_full_key(filename: str) -> Tuple[bytes, int, int]:
    """
    Wczytuje połowy kluczy z pliku JSON, losowo wybiera dwie różne połowy
    i tworzy pełny klucz poprzez ich połączenie.

    Args:
        filename (str): Nazwa pliku JSON z połowami kluczy.

    Returns:
        Tuple[bytes, int, int]: Losowo wygenerowany pełny klucz w bajtach i indeksy połówek.
    """
    # Wczytaj słownik połówek kluczy z pliku JSON
    with open(filename, "r") as file:
        half_keys = json.load(file)

    # Upewnij się, że mamy co najmniej dwie połówki do wyboru
    if len(half_keys) < 2:
        raise ValueError("Plik JSON musi zawierać co najmniej dwie połówki kluczy.")

    # Losowo wybierz dwa różne indeksy
    index1, index2 = random.sample(list(half_keys.keys()), 2)

    # Pobierz wartości odpowiadające tym indeksom
    half1 = bytes.fromhex(half_keys[index1])
    half2 = bytes.fromhex(half_keys[index2])

    # Połącz dwie połówki, tworząc pełny klucz
    full_key = half1 + half2

    print(f"Index 1: {index1}")
    print(f"Index 2: {index2}")
    print(f"Połówka 1: {half1.hex()}")
    print(f"Połówka 2: {half2.hex()}")
    print(f"Pełny klucz: {full_key.hex()}")

    return full_key, int(index1), int(index2)
