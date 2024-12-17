import os
import pyttsx3
from playsound import playsound



def odtworz_wav(sciezka_pliku):
    """
    Odtwarza dźwięk z pliku WAV za pomocą playsound.

    :param sciezka_pliku: Ścieżka do pliku WAV.
    """
    try:
        print(f"Odtwarzam: {sciezka_pliku}")
        playsound(sciezka_pliku)
        print("Odtwarzanie zakończone.")
    except Exception as e:
        print(f"Błąd podczas odtwarzania pliku WAV: {e}")

def tekst_na_mowe(tekst, sciezka_wyjscia=None):
    """
    Generuje mowę z tekstu i opcjonalnie zapisuje ją do pliku WAV.

    :param tekst: Tekst do zamiany na mowę.
    :param sciezka_wyjscia: Ścieżka do pliku WAV, w którym zapisana będzie mowa. Jeśli None, mowa będzie tylko odtworzona.
    """
    try:
        engine = pyttsx3.init()

        # Ustawienia silnika mowy
        engine.setProperty('rate', 150)  # Szybkość mowy
        engine.setProperty('volume', 1.0)  # Głośność (0.0 do 1.0)

        if sciezka_wyjscia:
            # Zapis do pliku WAV
            engine.save_to_file(tekst, sciezka_wyjscia)
            engine.runAndWait()
            print(f"Mowa zapisana do pliku: {sciezka_wyjscia}")
        else:
            # Odtwarzanie mowy
            engine.say(tekst)
            engine.runAndWait()
            print("Odtwarzanie mowy zakończone.")
    except Exception as e:
        print(f"Błąd podczas generowania mowy z tekstu: {e}")


import pyttsx3


def zmien_glos(indeks_glosu=0):
    """
    Zmienia głos w silniku mowy pyttsx3.

    :param indeks_glosu: Indeks głosu z listy dostępnych głosów.
    """
    try:
        # Inicjalizacja silnika
        engine = pyttsx3.init()

        # Pobranie dostępnych głosów
        glosy = engine.getProperty('voices')
        print("Dostępne głosy:")
        for i, glos in enumerate(glosy):
            print(f"{i}: {glos.name} - {glos.languages}")

        # Wybór głosu
        if indeks_glosu < len(glosy):
            engine.setProperty('voice', glosy[indeks_glosu].id)
            print(f"Ustawiono głos: {glosy[indeks_glosu].name}")
        else:
            print(f"Błąd: indeks {indeks_glosu} poza zakresem.")

        # Przykładowy tekst
        engine.say("To jest przykład zmienionego głosu.")
        engine.runAndWait()
    except Exception as e:
        print(f"Błąd: {e}")




# Przykład użycia:
if __name__ == "__main__":
    # Odtwarzanie pliku WAV
    print("Odtwarzanie pliku WAV...")
    odtworz_wav("nagranie_wzmocnione.wav")

    # Tekst na mowę
    print("Generowanie mowy z tekstu...")
    # tekst = "Witaj w świecie Python. To jest przykład tekstu na mowę."
   #tekst_na_mowe("Witaj szymek.")

