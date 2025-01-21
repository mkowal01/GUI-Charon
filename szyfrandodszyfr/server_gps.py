import serial
import pynmea2
import socket
import time
import threading
from datetime import datetime

# Funkcja do parsowania danych NMEA
def parse_nmea_data(data):
    try:
        if data.startswith('$GPGSV') or data.startswith('$GLGSV') or data.startswith('$GAGSV'):
            # Liczba widocznych satelitów z komunikatów GSV
            msg = pynmea2.parse(data)
            return {'type': 'satellites', 'satellites': msg.num_sv_in_view}
        elif data.startswith('$GNGGA'):
            # Pozycja GPS i czas z komunikatów GGA
            msg = pynmea2.parse(data)
            if msg.latitude and msg.longitude and msg.timestamp:
                return {
                    'type': 'position',
                    'latitude': msg.latitude,
                    'longitude': msg.longitude,
                    'timestamp': msg.timestamp
                }
    except pynmea2.ParseError:
        pass
    return None

# Funkcja do wyświetlania danych w emulatorze
def display_text_in_emulator(text):
    print(f"[DEBUG] Wyświetlanie w emulatorze: {text}")
    time.sleep(3)  # Symulacja wyświetlania przez emulator

# Serwer TCP
def start_tcp_server(latest_position):
    host = '192.168.1.4'
    port = 8080

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen(5)
            print(f"[TCP] Serwer nasłuchuje na porcie {port}")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"[TCP] Połączono z {client_address}")
                with client_socket:
                    while True:
                        data = client_socket.recv(1024).decode('utf-8').strip()
                        if not data:
                            break

                        print(f"[TCP] Otrzymano dane: {data}")
                        display_text_in_emulator(data)

                        # Odpowiedź lokalizacją
                        if latest_position['latitude'] and latest_position['longitude']:
                            response = f"Lokalizacja: Szerokość {latest_position['latitude']}, Długość {latest_position['longitude']}"
                            client_socket.sendall(response.encode('utf-8'))
                        else:
                            client_socket.sendall(b"Brak danych lokalizacji.")
    except Exception as e:
        print(f"[ERROR] Błąd w serwerze TCP: {e}")

# Główna funkcja programu
def main():
    port = "COM8"  # Zmień na właściwy port
    baudrate = 38400

    latest_position = {'latitude': None, 'longitude': None, 'timestamp': None}

    try:
        with serial.Serial(port, baudrate, timeout=1) as gps:
            print("Połączono z modułem GPS.")

            # Wątek dla serwera TCP
            threading.Thread(target=start_tcp_server, args=(latest_position,), daemon=True).start()

            while True:
                line = gps.readline().decode('ascii', errors='ignore').strip()
                if line:
                    parsed_data = parse_nmea_data(line)

                    if parsed_data:
                        if parsed_data['type'] == 'position':
                            latest_position.update(parsed_data)

                time.sleep(0.1)  # Małe opóźnienie, aby zmniejszyć obciążenie CPU

    except serial.SerialException as e:
        print(f"Błąd połączenia z modułem GPS: {e}")

if __name__ == "__main__":
    main()
