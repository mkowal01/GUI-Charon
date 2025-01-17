import socket
import threading
import time
from datetime import datetime

# Przykładowe dane GPS
GPS_DATA = [
    "Czas: 07:01:04.051 | Pozycja: Szeroko\u015b\u0107: 51.15993266666667, D\u0142ugo\u015b\u0107: 17.137928166666665 | Liczba widocznych satelit\u00f3w: 09",
    "Czas: 07:01:07.078 | Pozycja: Szeroko\u015b\u0107: 51.159932, D\u0142ugo\u015b\u0107: 17.1379305 | Liczba widocznych satelit\u00f3w: 06",
    "Czas: 07:01:10.098 | Pozycja: Szeroko\u015b\u0107: 51.159934, D\u0142ugo\u015b\u0107: 17.1379355 | Liczba widocznych satelit\u00f3w: 05",
    "Czas: 07:01:13.156 | Pozycja: Szeroko\u015b\u0107: 51.159933333333335, D\u0142ugo\u015b\u0107: 17.137939 | Liczba widocznych satelit\u00f3w: 02",
    "Czas: 07:01:16.202 | Pozycja: Szeroko\u015b\u0107: 51.1599345, D\u0142ugo\u015b\u0107: 17.137940666666665 | Liczba widocznych satelit\u00f3w: 05",
    "Czas: 07:01:19.239 | Pozycja: Szeroko\u015b\u0107: 51.159926166666665, D\u0142ugo\u015b\u0107: 17.137950166666666 | Liczba widocznych satelit\u00f3w: 05",
    "Czas: 07:01:22.299 | Pozycja: Szeroko\u015b\u0107: 51.159922333333334, D\u0142ugo\u015b\u0107: 17.137953666666668 | Liczba widocznych satelit\u00f3w: 05",
    "Czas: 07:01:25.397 | Pozycja: Szeroko\u015b\u0107: 51.1599205, D\u0142ugo\u015b\u0107: 17.137956166666665 | Liczba widocznych satelit\u00f3w: 05",
    "Czas: 07:01:28.492 | Pozycja: Szeroko\u015b\u0107: 51.159929, D\u0142ugo\u015b\u0107: 17.137955666666667 | Liczba widocznych satelit\u00f3w: 02"
]

def server_mode(port):
    """Uruchamia tryb serwera."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"[SERVER] Serwer nasłuchuje na porcie {port}...")

    def handle_client(client_socket, address):
        print(f"[SERVER] Połączono z {address}")
        try:
            send_loc_responses = False

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8').strip()
                print(f"[SERVER] Odebrano od {address}: {message}")

                if message == "LOC":
                    print(f"[SERVER] Otrzymano polecenie LOC od {address}. Wysyłanie danych GPS...")
                    send_loc_responses = True

                    # Wysyłanie danych GPS w osobnym wątku
                    def send_responses():
                        index = 0
                        while send_loc_responses:
                            try:
                                current_data = GPS_DATA[index % len(GPS_DATA)]
                                client_socket.sendall(f"{current_data}\n".encode('utf-8'))
                                print(f"[SERVER] Wysłano do {address}: {current_data}")
                                index += 1
                                time.sleep(1)  # Wysyłaj co sekundę
                            except (ConnectionResetError, BrokenPipeError):
                                print(f"[SERVER] Połączenie z {address} zostało przerwane.")
                                break

                    threading.Thread(target=send_responses, daemon=True).start()

                else:
                    client_socket.sendall("Wiadomość odebrana.\n".encode('utf-8'))
                    print(f"[SERVER] Wysłano odpowiedź do {address}: Wiadomość odebrana.")

        except ConnectionResetError:
            print(f"[SERVER] Połączenie z {address} zostało przerwane.")
        finally:
            print(f"[SERVER] Rozłączono z {address}")
            send_loc_responses = False
            client_socket.close()

    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

def client_mode(ip, port):
    """Uruchamia tryb klienta."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, port))
        print(f"[CLIENT] Połączono z serwerem {ip}:{port}")
    except ConnectionRefusedError:
        print(f"[CLIENT] Nie udało się połączyć z serwerem {ip}:{port}")
        return

    try:
        while True:
            message = input("[CLIENT] Wpisz wiadomość (lub 'exit' aby zakończyć): ")
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"[CLIENT] Odpowiedź serwera: {response}")
    except ConnectionResetError:
        print("[CLIENT] Połączenie z serwerem zostało przerwane.")
    finally:
        client_socket.close()
        print("[CLIENT] Rozłączono.")

if __name__ == "__main__":
    print("=== Aplikacja do testowania Wi-Fi ===")
    mode = input("Wybierz tryb (server/client): ").strip().lower()

    if mode == "server":
        port = int(input("Podaj port do nasłuchiwania: "))
        server_mode(port)
    elif mode == "client":
        ip = input("Podaj adres IP serwera: ").strip()
        port = int(input("Podaj port serwera: "))
        client_mode(ip, port)
    else:
        print("Nieznany tryb. Wybierz 'server' lub 'client'.")
