import serial

# Ustawienia portu szeregowego
SERIAL_PORT = 'COM6'  # Port USB UART odbiornika
BAUD_RATE = 9600

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Odbiornik podłączony do {SERIAL_PORT}")
        print("Czekam na wiadomości...")

        buffer = b""
        while True:
            if ser.in_waiting > 0:  # Sprawdź, czy są dane do odebrania
                char = ser.read(1)  # Odbierz bajt

                if char == b"\n":  # Koniec wiadomości
                    received_message = buffer.strip().decode('utf-8', errors='ignore')
                    print(f"Odebrano: {received_message} (BYTE: {buffer})")

                    # Wpisanie odpowiedzi
                    response_message = f"Długość wiadomości {len(received_message)}"
                    ser.write(response_message.encode('utf-8') + b"\n")
                    print(f"Wysłano: {response_message} (BYTE)")

                    buffer = b""  # Wyczyść bufor
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
