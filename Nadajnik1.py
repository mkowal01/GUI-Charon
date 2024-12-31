import serial
import binascii  # Do konwersji na HEX

# Ustawienia portu szeregowego
SERIAL_PORT = 'COM4'  # Port USB UART nadajnika
BAUD_RATE = 9600


def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Nadajnik podłączony do {SERIAL_PORT}")

        while True:
            # Wpisanie wiadomości
            message = input("Wpisz wiadomość do wysłania: ")

            # Konwersja wiadomości na HEX
            hex_message = binascii.hexlify(message.encode('utf-8')).decode('ascii')
            ser.write((hex_message + "\n").encode('ascii'))  # Wyślij HEX zakończony '\n'
            print(f"Wysłano (HEX): {hex_message}")

            # Oczekiwanie na odpowiedź
            response_hex = ""
            while not response_hex:
                if ser.in_waiting > 0:
                    response_hex = ser.readline().decode('ascii', errors='ignore').strip()

            # Dekodowanie odpowiedzi z HEX
            response_text = bytes.fromhex(response_hex).decode('utf-8', errors='ignore')
            print(f"Otrzymano odpowiedź: {response_text} (HEX: {response_hex})")

    except serial.SerialException as e:
        print(f"Błąd portu szeregowego: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwanie programu.")
    finally:
        ser.close()
        print("Połączenie zamknięte.")


if __name__ == "__main__":
    main()
