import time
from datetime import datetime
import socket

# Ustawienia gniazda (socket)
SERVER_IP = '192.168.1.3'  # Adres IP serwera
SERVER_PORT = 12345       # Port serwera
BUFFER_SIZE = 2048        # Rozmiar bufora danych

def zapisz_plik(output_file, dane):
    """
    Zapisuje odebrane dane do pliku.

    :param output_file: Ścieżka do pliku wyjściowego.
    :param dane: Odebrane dane w bajtach.
    """
    with open(output_file, "wb") as f:
        f.write(dane)
    print(f"Plik zapisany jako {output_file}")

def odbierz_plik(client_socket, output_file):
    """
    Odbiera plik przez socket w porcjach, wysyłając potwierdzenie po każdej porcji.

    :param client_socket: Obiekt socketu klienta.
    :param output_file: Ścieżka do pliku wyjściowego.
    """
    try:
        buffer = b""
        start_time_total = time.time()

        # Odbierz nagłówek
        header = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip('|')
        rozmiar = int(header)
        print(f"Oczekiwana długość pliku: {rozmiar} B")

        # Wysłanie potwierdzenia odbioru nagłówka
        client_socket.sendall(b"ACK_HEADER\n")

        # Odbieranie danych w porcjach
        while len(buffer) < rozmiar:
            start_time = time.time()
            chunk = client_socket.recv(min(BUFFER_SIZE, rozmiar - len(buffer)))
            buffer += chunk
            end_time = time.time()
            print(f"Odebrano porcję danych ({len(chunk)} B, łącznie: {len(buffer)}/{rozmiar} B, czas: {end_time - start_time:.2f} s)")

            # Wysłanie potwierdzenia odbioru porcji
            client_socket.sendall(b"ACK_CHUNK\n")

        # Odbierz stopkę
        stopka = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
        if stopka == "|XXX":
            print("Odebrano poprawną stopkę.")
        else:
            print("Nieprawidłowa stopka danych.")
            return

        # Zapisanie odebranych danych do pliku
        zapisz_plik(output_file, buffer)

        # Wysłanie potwierdzenia odbioru pliku
        client_socket.sendall(b"ACK_FILE\n")
        end_time_total = time.time()
        print(f"Całkowity czas odbioru pliku: {end_time_total - start_time_total:.2f} s")
    except Exception as e:
        print(f"Błąd podczas odbioru pliku: {e}")

def main():
    start_datetime = datetime.now()
    output_file = "charon_library/received_file.bin"

    try:
        # Tworzenie socketu serwera
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((SERVER_IP, SERVER_PORT))
            server_socket.listen(1)
            print(f"Serwer nasłuchuje na {SERVER_IP}:{SERVER_PORT}")

            # Akceptowanie połączenia
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Połączono z {client_address}")

                # Odbieranie pliku
                odbierz_plik(client_socket, output_file)

    except socket.error as e:
        print(f"Błąd socketu: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwanie programu.")

    end_datetime = datetime.now()
    print(f'Start {start_datetime} \n End {end_datetime}')

if __name__ == "__main__":
    main()
