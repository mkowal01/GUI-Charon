import serial

# Ustawienia portu szeregowego
SERIAL_PORT = 'COM6'  # Port USB UART nadajnika
BAUD_RATE = 9600

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Nadajnik podłączony do {SERIAL_PORT}")

        while True:
            # Wpisanie wiadomości
            message = input("Wpisz wiadomość do wysłania: ")
            message_length = len(message)
            byte_message = f"{message_length}|{message}|XXX".encode('utf-8')
            print(byte_message)
            ser.write(byte_message + b"\n")  # Wyślij wiadomość zakończoną '\n'
            print(f"Wysłano (BYTE): {byte_message}")

            # Oczekiwanie na odpowiedź
            response_bytes = b""
            while not response_bytes:
                if ser.in_waiting > 0:
                    response_bytes = ser.readline().strip()

            # Dekodowanie odpowiedzi z bajtów
            response_text = response_bytes.decode('utf-8', errors='ignore')
            print(f"Otrzymano odpowiedź: {response_text} (BYTE: {response_bytes}) (len: {len(response_bytes)})")

    except serial.SerialException as e:
        print(f"Błąd portu szeregowego: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwanie programu.")
    finally:
        ser.close()
        print("Połączenie zamknięte.")


if __name__ == "__main__":
    main()