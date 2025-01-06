import serial
import struct

# Ustawienia portu szeregowego
SERIAL_PORT = 'COM6'  # Port USB UART nadajnika
BAUD_RATE = 9600

def wyslij_rozmiar(serial_port, rozmiar):
    """
    Wysyła rozmiar danych przez port szeregowy.

    :param serial_port: Obiekt portu szeregowego.
    :param rozmiar: Rozmiar danych do wysłania jako liczba całkowita.
    """
    try:
        rozmiar_pakiet = struct.pack('>I', rozmiar)  # Zapisz w formacie big-endian
        serial_port.write(rozmiar_pakiet)
        print(f"Wysłano rozmiar danych: {rozmiar} B")
    except Exception as e:
        print(f"Błąd podczas wysyłania rozmiaru danych: {e}")

def wyslij_plik(serial_port, sciezka_pliku):
    """
    Wysyła plik przez port szeregowy.

    :param serial_port: Obiekt portu szeregowego.
    :param sciezka_pliku: Ścieżka do pliku do wysłania.
    """
    try:
        with open(sciezka_pliku, 'rb') as plik:
            zawartosc = plik.read()
            rozmiar = len(zawartosc)

            # Wyślij rozmiar pliku
            wyslij_rozmiar(serial_port, rozmiar)

            # Wyślij dane pliku z nagłówkiem i stopką
            naglowek = f"{rozmiar}|".encode('utf-8')
            stopka = b"|XXX"
            pelna_wiadomosc = naglowek + zawartosc + stopka

            serial_port.write(pelna_wiadomosc)
            print(f"Wysłano plik: {sciezka_pliku} (Rozmiar: {rozmiar} B)")
    except Exception as e:
        print(f"Błąd podczas wysyłania pliku: {e}")

def main():
    sciezka_pliku = "C:/Users/ninja/OneDrive/Pulpit/Praca/GUI-Charon/nagranie_wzmocnione.mp3"

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Nadajnik podłączony do {SERIAL_PORT}")

        # Wysyłanie pliku
        wyslij_plik(ser, sciezka_pliku)

        # Oczekiwanie na odpowiedź
        response = ser.read_until(b"\n").decode('utf-8', errors='ignore').strip()
        if response:
            print(f"Otrzymano odpowiedź: {response}")

    except serial.SerialException as e:
        print(f"Błąd portu szeregowego: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwanie programu.")
    finally:
        ser.close()
        print("Połączenie zamknięte.")

if __name__ == "__main__":
    main()
