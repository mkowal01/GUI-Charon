import sounddevice as sd
import soundfile as sf
import numpy as np

# Parametry nagrywania
czas_nagrania = 2  # czas nagrania w sekundach
czestotliwosc_probkowania = 44100  # częstotliwość próbkowania w Hz
nazwa_pliku = 'nagranie_wzmocnione.wav'  # nazwa pliku wyjściowego
wspolczynnik_wzmocnienia = 10.0  # wartość wzmacniająca (np. 2.0 = 200% głośności)

print("Rozpoczynam nagrywanie...")

# Nagrywanie dźwięku
nagranie = sd.rec(int(czas_nagrania * czestotliwosc_probkowania), samplerate=czestotliwosc_probkowania, channels=2, dtype='float32')
sd.wait()  # oczekiwanie na zakończenie nagrywania

print("Nagrywanie zakończone. Przetwarzanie dźwięku...")

# Wzmocnienie dźwięku
nagranie_wzmocnione = nagranie * wspolczynnik_wzmocnienia

# Zabezpieczenie przed przesterowaniem
nagranie_wzmocnione = np.clip(nagranie_wzmocnione, -1.0, 1.0)

print("Zapisuję wzmocnione nagranie do pliku...")

# Zapis wzmocnionego nagrania do pliku
sf.write(nazwa_pliku, nagranie_wzmocnione, czestotliwosc_probkowania)

print(f"Wzmocnione nagranie zapisane jako {nazwa_pliku}")
