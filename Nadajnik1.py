import serial
import binascii  # Do konwersji na HEX
from datetime import datetime  # Do dodawania czasu

# Ustawienia portu szeregowego
SERIAL_PORT = 'COM3'  # Port USB UART nadajnika
BAUD_RATE = 9600

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Nadajnik podłączony do {SERIAL_PORT}")

        total_sent = 0  # Licznik wysłanych danych
        total_received = 0  # Licznik odebranych danych

        while True:
            # Wpisanie wiadomości
            message = input("Wpisz wiadomość do wysłania: ")

            # Sprawdzenie, czy wiadomość ma zostać wysłana w formacie HEX
            if message.startswith("!HEX!"):
                hex_message = message[5:].strip()  # Pobierz część po "!HEX!"
                try:
                    # Sprawdzenie poprawności HEX
                    binascii.unhexlify(hex_message)
                except binascii.Error:
                    print("Błąd: Nieprawidłowy format HEX.")
                    continue
            else:
                # Konwersja wiadomości na HEX
                hex_message = binascii.hexlify(message.encode('utf-8')).decode('ascii')

            timestamp_send = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Czas wysłania
            ser.write((hex_message + "\n").encode('ascii'))  # Wyślij HEX zakończony '\n'
            total_sent += len(hex_message) + 1  # Zwiększ licznik o długość wysłanej wiadomości + '\n'
            print(f"[{timestamp_send}] Wysłano (HEX): {hex_message}")

            # Oczekiwanie na odpowiedź
            response_hex = ""
            while not response_hex:
                if ser.in_waiting > 0:
                    response_hex = ser.readline().decode('ascii', errors='ignore').strip()

            total_received += len(response_hex)  # Zwiększ licznik o długość odebranej wiadomości

            # Dekodowanie odpowiedzi z HEX
            response_text = bytes.fromhex(response_hex).decode('utf-8', errors='ignore')
            timestamp_receive = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Czas odbioru
            print(f"[{timestamp_receive}] Otrzymano odpowiedź: {response_text} (HEX: {response_hex})")

            # Wyświetlenie statystyk przesyłu danych
            print(f"\nStatystyki przesyłu danych:")
            print(f"  Wysłano: {total_sent} bajtów")
            print(f"  Odebrano: {total_received} bajtów")

    except serial.SerialException as e:
        print(f"Błąd portu szeregowego: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwanie programu.")
    finally:
        ser.close()
        print("Połączenie zamknięte.")

if __name__ == "__main__":
    main()
             