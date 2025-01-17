import serial
import struct

# Ustawienia portu szeregowego
SERIAL_PORT = 'COM6'  # Port USB UART nadajnika
BAUD_RATE = 9600

CHUNK_SIZE = 1024  # Rozmiar pojedynczej porcji danych w bajtach

def wyslij_plik(serial_port, sciezka_pliku):
    """
    Wysyła plik przez port szeregowy w porcjach, oczekując potwierdzenia po każdej porcji.

    :param serial_port: Obiekt portu szeregowego.
    :param sciezka_pliku: Ścieżka do pliku do wysłania.
    """
    try:
        with open(sciezka_pliku, 'rb') as plik:
            zawartosc = plik.read()
            rozmiar = len(zawartosc)

            # Wyślij nagłówek z rozmiarem pliku
            naglowek = f"{rozmiar}|".encode('utf-8')
            serial_port.write(naglowek)
            print(f"Wysłano nagłówek: {naglowek.decode('utf-8')}")

            # Oczekiwanie na potwierdzenie nagłówka
            response = serial_port.read_until(b"\n").decode('utf-8', errors='ignore').strip()
            if response != "ACK_HEADER":
                print("Nieoczekiwane potwierdzenie nagłówka.")
                return

            print("Odebrano potwierdzenie nagłówka.")

            # Wysyłanie danych w porcjach
            for i in range(0, rozmiar, CHUNK_SIZE):
                chunk = zawartosc[i:i + CHUNK_SIZE]
                serial_port.write(chunk)
                print(f"Wysłano porcję danych ({len(chunk)} B)")

                # Oczekiwanie na potwierdzenie
                response = serial_port.read_until(b"\n").decode('utf-8', errors='ignore').strip()
                if response != "ACK_CHUNK":
                    print("Nieoczekiwane potwierdzenie porcji danych.")
                    return

            # Wyślij stopkę
            stopka = b"|XXX\n"
            serial_port.write(stopka)
            print("Wysłano stopkę.")

            # Oczekiwanie na potwierdzenie pliku
            response = serial_port.read_until(b"\n").decode('utf-8', errors='ignore').strip()
            if response == "ACK_FILE":
                print("Odebrano potwierdzenie odbioru pliku.")
            else:
                print(f"Otrzymano nieoczekiwaną odpowiedź: {response}")
    except Exception as e:
        print(f"Błąd podczas wysyłania pliku: {e}")

def main():
    sciezka_pliku = "C:/Users/ninja/OneDrive/Pulpit/Praca/GUI-Charon/nagranie_wzmocnione.mp3"

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        print(f"Nadajnik podłączony do {SERIAL_PORT}")

        # Wysyłanie pliku
        wyslij_plik(ser, sciezka_pliku)

    except serial.SerialException as e:
        print(f"Błąd portu szeregowego: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwanie programu.")
    finally:
        ser.close()
        print("Połączenie zamknięte.")

if __name__ == "__main__":
    main()
