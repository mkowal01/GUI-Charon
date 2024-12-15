import json
import random


def generate_random_full_key(filename: str) -> str:
    """
    Wczytuje połowy kluczy z pliku JSON, losowo wybiera dwie różne połowy
    i tworzy pełny klucz poprzez ich połączenie.

    Args:
        filename (str): Nazwa pliku JSON z połowami kluczy.

    Returns:
        str: Losowo wygenerowany pełny klucz w formacie heksadecymalnym.
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
    half1 = half_keys[index1]
    half2 = half_keys[index2]

    # Połącz dwie połówki, tworząc pełny klucz
    full_key = half1 + half2

    print(f"Losowo wybrane indeksy: {index1}, {index2}")
    print(f"Połówka 1: {half1}")
    print(f"Połówka 2: {half2}")
    print(f"Pełny klucz: {full_key}")

    return full_key


# Przykład użycia
if __name__ == "__main__":
    filename = "half_keys_indexed.json"  # Plik JSON z połowami kluczy

    # Wygeneruj losowy pełny klucz
    full_key = generate_random_full_key(filename)
