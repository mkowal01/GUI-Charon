import os
import json


def generate_half_keys(num_halves: int, half_length: int) -> dict:
    """
    Generuje słownik z indeksowanymi połowami kluczy.

    Args:
        num_halves (int): Liczba połówek do wygenerowania.
        half_length (int): Długość jednej połowy klucza w bajtach.

    Returns:
        dict: Słownik z indeksami jako kluczami i połowami kluczy w formacie heksadecymalnym jako wartościami.
    """
    return {index: os.urandom(half_length).hex() for index in range(num_halves)}


def save_half_keys_to_json(half_keys: dict, filename: str) -> None:
    """
    Zapisuje słownik połówek kluczy do pliku JSON.

    Args:
        half_keys (dict): Słownik połówek kluczy.
        filename (str): Nazwa pliku JSON.
    """
    with open(filename, "w") as file:
        json.dump(half_keys, file, indent=4)


def load_half_keys_from_json(filename: str) -> dict:
    """
    Wczytuje słownik połówek kluczy z pliku JSON.

    Args:
        filename (str): Nazwa pliku JSON.

    Returns:
        dict: Słownik z indeksami i połowami kluczy.
    """
    with open(filename, "r") as file:
        return json.load(file)


def create_full_key(index1: int, index2: int, half_keys: dict) -> str:
    """
    Tworzy pełny klucz poprzez połączenie dwóch połówek.

    Args:
        index1 (int): Indeks pierwszej połowy klucza.
        index2 (int): Indeks drugiej połowy klucza.
        half_keys (dict): Słownik z połowami kluczy.

    Returns:
        str: Pełny klucz w formacie heksadecymalnym.
    """
    half1 = half_keys.get(str(index1))
    half2 = half_keys.get(str(index2))
    if not half1 or not half2:
        raise ValueError("Nieprawidłowe indeksy kluczy.")
    return half1 + half2


# Przykład użycia
if __name__ == "__main__":
    num_halves = 200  # Liczba połówek
    half_length = 16  # Długość każdej połowy w bajtach (16 bajtów = połowa 256-bitowego klucza)
    filename = "half_keys_indexed.json"  # Nazwa pliku JSON

    # Generowanie i zapisywanie połówek kluczy
    half_keys = generate_half_keys(num_halves, half_length)
    save_half_keys_to_json(half_keys, filename)
    print(f"{num_halves} połówek kluczy zapisano do pliku {filename}.")

    # Wczytywanie kluczy z pliku i tworzenie pełnego klucza
    loaded_keys = load_half_keys_from_json(filename)
    index1, index2 = 0, 1  # Przykładowe indeksy
    full_key = create_full_key(index1, index2, loaded_keys)
    print(f"Pełny klucz stworzony z indeksów {index1} i {index2}: {full_key}")
