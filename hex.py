def plik_na_hex(sciezka_pliku, sciezka_hex):
    """
    Konwertuje plik na reprezentację HEX i zapisuje wynik w nowym pliku.

    :param sciezka_pliku: Ścieżka do pliku wejściowego.
    :param sciezka_hex: Ścieżka do pliku wyjściowego z reprezentacją HEX.
    """
    try:
        with open(sciezka_pliku, 'rb') as plik:
            zawartosc = plik.read()
        with open(sciezka_hex, 'w') as plik_hex:
            plik_hex.write(zawartosc.hex())
        print(f"Plik został przekonwertowany na HEX i zapisany jako: {sciezka_hex}")
    except Exception as e:
        print(f"Błąd podczas konwersji pliku na HEX: {e}")


def hex_na_plik(sciezka_hex, sciezka_wyjscie):
    """
    Przywraca oryginalny plik z reprezentacji HEX.

    :param sciezka_hex: Ścieżka do pliku z reprezentacją HEX.
    :param sciezka_wyjscie: Ścieżka do oryginalnego pliku wyjściowego.
    """
    try:
        with open(sciezka_hex, 'r') as plik_hex:
            zawartosc_hex = plik_hex.read()
        with open(sciezka_wyjscie, 'wb') as plik_wyjscie:
            plik_wyjscie.write(bytes.fromhex(zawartosc_hex))
        print(f"Plik został przywrócony z HEX i zapisany jako: {sciezka_wyjscie}")
    except Exception as e:
        print(f"Błąd podczas przywracania pliku z HEX: {e}")


# Przykład użycia:
sciezka_wejsciowa = 'nagranie_wzmocnione.wav'  # Ścieżka do oryginalnego pliku
sciezka_hex = 'plik_hex.txt'  # Ścieżka do pliku HEX
sciezka_wyjscie = 'nagranie_wzmocnione2.wav'  # Ścieżka do odtworzonego pliku

# Konwersja pliku na HEX
plik_na_hex(sciezka_wejsciowa, sciezka_hex)
# Przywrócenie pliku z HEX
hex_na_plik(sciezka_hex, sciezka_wyjscie)
