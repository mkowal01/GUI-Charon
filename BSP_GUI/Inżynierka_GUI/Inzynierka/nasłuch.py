import socket
import threading
import time
import os

# Tworzenie katalogu do zapisu plików audio
RECORDING_DIR = "recording"
os.makedirs(RECORDING_DIR, exist_ok=True)


def receive_file(client_socket, filename):
    """Odbiera plik MP3 od klienta i zapisuje go jako plik binarny."""
    filepath = os.path.join(RECORDING_DIR, filename)
    print(f"[SERVER] Odbieranie pliku {filename}...")

    with open(filepath, "wb") as file:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            file.write(data)

    print(f"[SERVER] Plik zapisany jako '{filepath}'.")


def server_mode(port):
    """Uruchamia tryb serwera."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"[SERVER] Serwer nasłuchuje na porcie {port}...")

    def handle_client(client_socket, address):
        print(f"[SERVER] Połączono z {address}")
        try:
            file_path = None
            file_size = None
            received_bytes = 0
            file = None

            while True:
                # Odbieramy pierwszą wiadomość jako UTF-8 (komendę AU_FILE)
                data = client_socket.recv(1024)
                if not data:
                    break

                try:
                    decoded_data = data.decode("utf-8").strip()
                    print(f"[SERVER] Odebrano od {address}: {decoded_data}")

                    if decoded_data.startswith("AU_FILE"):
                        # Parsowanie nazwy pliku i rozmiaru
                        _, filename, file_size = decoded_data.split(":")
                        file_size = int(file_size)
                        file_path = os.path.join(RECORDING_DIR, filename)
                        print(f"[SERVER] Oczekiwanie na plik audio: {filename} ({file_size} bajtów)")

                        # Otwieramy plik do zapisu
                        file = open(file_path, "wb")
                        received_bytes = 0

                        # Odpowiedź do klienta
                        client_socket.sendall("READY".encode("utf-8"))
                        continue  # Przechodzimy do odbioru pliku

                except UnicodeDecodeError:
                    # Jeśli nie można zdekodować danych, traktujemy je jako binarne
                    if file:
                        file.write(data)
                        received_bytes += len(data)
                        print(f"[SERVER] Otrzymano {received_bytes}/{file_size} bajtów")

                        # Zamykamy plik, gdy cały plik zostanie przesłany
                        if received_bytes >= file_size:
                            print(f"[SERVER] Plik zapisany jako '{file_path}'")
                            file.close()
                            file = None
                            client_socket.sendall("FILE_RECEIVED".encode("utf-8"))
                            break  # Kończymy po otrzymaniu całego pliku

            print(f"[SERVER] Rozłączono z {address}")

        except ConnectionResetError:
            print(f"[SERVER] Połączenie z {address} zostało przerwane.")
        finally:
            if file:
                file.close()
            client_socket.close()

    while True:
        client_socket, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()


def send_file(client_socket, filename):
    """Wysyła plik MP3 do serwera."""
    try:
        with open(filename, "rb") as file:
            client_socket.sendall(f"SEND_MP3 {os.path.basename(filename)}".encode('utf-8'))
            time.sleep(1)  # Krótka przerwa, aby uniknąć kolizji danych
            while chunk := file.read(4096):
                client_socket.sendall(chunk)
        print(f"[CLIENT] Wysłano plik audio: {filename}")
    except FileNotFoundError:
        print(f"[CLIENT] Plik {filename} nie istnieje.")


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
            message = input("[CLIENT] Wpisz wiadomość ('exit' aby zakończyć, 'send_mp3 {nazwa}' aby wysłać plik MP3): ")
            if message.lower() == 'exit':
                break
            elif message.startswith("send_mp3"):
                _, filename = message.split(" ", 1)
                send_file(client_socket, filename)
            else:
                client_socket.send(message.encode('utf-8'))
                response = client_socket.recv(1024).decode('utf-8')
                print(f"[CLIENT] Odpowiedź serwera: {response}")
    except ConnectionResetError:
        print("[CLIENT] Połączenie z serwerem zostało przerwane.")
    finally:
        client_socket.close()
        print("[CLIENT] Rozłączono.")


if __name__ == "__main__":
    print("=== Aplikacja do przesyłania plików audio MP3 ===")
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
