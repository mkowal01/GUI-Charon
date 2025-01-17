import time
from datetime import datetime

import serial

# Ustawienia portu szeregowego
SERIAL_PORT = 'COM6'  # Port USB UART odbiornika
BAUD_RATE = 9600
CHUNK_SIZE = 1024  # Rozmiar pojedynczej porcji danych w bajtach

def zapisz_plik(output_file, dane):

    with open(output_file, "wb") as f:
        f.write(dane)
    print(f"Plik zapisany jako {output_file}")

def odbierz_plik(serial_port, output_file):
    """
    Odbiera plik przez port szeregowy w porcjach, wysyłając potwierdzenie po każdej porcji.

    :param serial_port: Obiekt portu szeregowego.
    :param output_file: Ścieżka do pliku wyjściowego.
    """
    try:
        buffer = b""
        start_time_total = time.time()
        # Odbierz nagłówek
        header = serial_port.read_until(b"|").decode('utf-8', errors='ignore').strip('|')
        rozmiar = int(header)
        print(f"Oczekiwana długość pliku: {rozmiar} B")

        # Wysłanie potwierdzenia odbioru nagłówka
        serial_port.write(b"ACK_HEADER\n")

        # Odbieranie danych w porcjach
        while len(buffer) < rozmiar:
            start_time = time.time()
            chunk = serial_port.read(min(CHUNK_SIZE, rozmiar - len(buffer)))
            buffer += chunk
            end_time = time.time()
            print(f"Odebrano porcję danych ({len(chunk)} B, łącznie: {len(buffer)}/{rozmiar} B, czas: {end_time - start_time:.2f} s)")

            # Wysłanie potwierdzenia odbioru porcji
            serial_port.write(b"ACK_CHUNK\n")

        # Odbierz stopkę
        stopka = serial_port.read_until(b"\n").decode('utf-8', errors='ignore').strip()
        if stopka == "|XXX":
            print("Odebrano poprawną stopkę.")
        else:
            print("Nieprawidłowa stopka danych.")
            return

        # Zapisanie odebranych danych do pliku
        zapisz_plik(output_file, buffer)

        # Wysłanie potwierdzenia odbioru pliku
        serial_port.write(b"ACK_FILE\n")
        end_time_total = time.time()
        print(f"Całkowity czas odbioru pliku: {end_time_total - start_time_total:.2f} s")
    except Exception as e:
        print(f"Błąd podczas odbioru pliku: {e}")

def main():
    start_datetime = datetime.now()
    output_file = "szyfrandodszyfr/received_file.bin"

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
        print(f"Odbiornik podłączony do {SERIAL_PORT}")

        # Odbieranie pliku
        odbierz_plik(ser, output_file)

    except serial.SerialException as e:
        print(f"Błąd portu szeregowego: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwanie programu.")
    finally:
        ser.close()
        print("Połączenie zamknięte.")
    end_datetime = datetime.now()
    print(f'Start {start_datetime} \n End {end_datetime}')
if __name__ == "__main__":
    main()
