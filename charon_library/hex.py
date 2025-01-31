def plik_na_bajty(sciezka_pliku, sciezka_bajty):
    """
    Konwertuje plik na surowe bajty i zapisuje wynik w nowym pliku.

    :param sciezka_pliku: Ścieżka do pliku wejściowego.
    :param sciezka_bajty: Ścieżka do pliku wyjściowego z reprezentacją bajtów.
    """
    try:
        with open(sciezka_pliku, 'rb') as plik:
            zawartosc = plik.read()
        with open(sciezka_bajty, 'wb') as plik_bajty:
            plik_bajty.write(zawartosc)
        print(f"Plik został przekonwertowany na bajty i zapisany jako: {sciezka_bajty}")
    except Exception as e:
        print(f"Błąd podczas konwersji pliku na bajty: {e}")

def bajty_na_plik(sciezka_bajty, sciezka_wyjscie):
    """
    Przywraca oryginalny plik z surowych bajtów.

    :param sciezka_bajty: Ścieżka do pliku z bajtami.
    :param sciezka_wyjscie: Ścieżka do oryginalnego pliku wyjściowego.
    """
    try:
        with open(sciezka_bajty, 'rb') as plik_bajty:
            zawartosc = plik_bajty.read()
        with open(sciezka_wyjscie, 'wb') as plik_wyjscie:
            plik_wyjscie.write(zawartosc)
            print(zawartosc)
        print(f"Plik został przywrócony z bajtów i zapisany jako: {sciezka_wyjscie}")
    except Exception as e:
        print(f"Błąd podczas przywracania pliku z bajtów: {e}")

# Przykład użycia:
sciezka_wejsciowa = 'C:/Users/ninja/OneDrive/Pulpit/Praca/GUI-Charon/nagranie_wzmocnione.mp3'  # Ścieżka do oryginalnego pliku
sciezka_bajty = 'received_file.bin'  # Ścieżka do pliku bajtów
sciezka_wyjscie = 'nagranie_odtworzone.mp3'  # Ścieżka do odtworzonego pliku

# Konwersja pliku na bajty
# plik_na_bajty(sciezka_wejsciowa, sciezka_bajty)
# Przywrócenie pliku z bajtów
bajty_na_plik(sciezka_bajty, sciezka_wyjscie)

