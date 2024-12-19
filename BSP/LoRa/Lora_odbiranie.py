import serial
import binascii  # Do konwersji z HEX

# Ustawienia portu szeregowego
SERIAL_PORT = 'COM8'  # Port USB UART odbiornika
BAUD_RATE = 9600


def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Odbiornik podłączony do {SERIAL_PORT}")
        print("Czekam na wiadomości...")

        buffer = ""
        while True:
            if ser.in_waiting > 0:  # Sprawdź, czy są dane do odebrania
                char = ser.read(1).decode('ascii', errors='ignore')

                if char == "\n":  # Koniec wiadomości
                    hex_message = buffer.strip()
                    try:
                        # Dekodowanie wiadomości z HEX na tekst
                        received_message = bytes.fromhex(hex_message).decode('utf-8')
                        print(f"Odebrano: {received_message} (HEX: {hex_message})")
                    except ValueError:
                        print(f"Błąd dekodowania HEX: {hex_message}")
                        buffer = ""
                        continue

                    buffer = ""  # Wyczyść bufor

                    # Wpisanie odpowiedzi
                    response_message = input("Odpowiedź do nadawcy: ")
                    response_hex = binascii.hexlify(response_message.encode('utf-8')).decode('ascii')
                    ser.write((response_hex + "\n").encode('ascii'))
                    print(f"Wysłano (HEX): {response_hex}")
                else:
                    buffer += char

    except serial.SerialException as e:
        print(f"Błąd portu szeregowego: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwanie programu.")
    finally:
        ser.close()
        print("Połączenie zamknięte.")


if __name__ == "__main__":
    main()
