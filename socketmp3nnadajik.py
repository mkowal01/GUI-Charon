import socket
import time
from datetime import datetime

# Ustawienia gniazda (socket)
SERVER_IP = '192.168.1.7'  # Adres IP serwera
SERVER_PORT = 12345       # Port serwera
BUFFER_SIZE = 2048# Rozmiar bufora danych


def wyslij_plik(socket, sciezka_pliku):
    """
    Wysyła plik przez socket w porcjach, oczekując potwierdzenia po każdej porcji.

    :param socket: Obiekt socketu.
    :param sciezka_pliku: Ścieżka do pliku do wysłania.
    """
    try:
        with open(sciezka_pliku, 'rb') as plik:
            zawartosc = plik.read()
            rozmiar = len(zawartosc)

            start_time_total = time.time()

            # Wyślij nagłówek z rozmiarem pliku
            naglowek = f"{rozmiar}|".encode('utf-8')
            socket.sendall(naglowek)
            print(f"Wysłano nagłówek: {naglowek.decode('utf-8')}")

            # Oczekiwanie na potwierdzenie nagłówka
            response = socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            if response != "ACK_HEADER":
                print("Nieoczekiwane potwierdzenie nagłówka.")
                return

            print("Odebrano potwierdzenie nagłówka.")

            # Wysyłanie danych w porcjach
            for i in range(0, rozmiar, BUFFER_SIZE):
                start_time = time.time()
                chunk = zawartosc[i:i + BUFFER_SIZE]
                socket.sendall(chunk)
                print(f"Wysłano porcję danych ({len(chunk)} B)")

                # Oczekiwanie na potwierdzenie
                response = socket.recv(BUFFER_SIZE).decode('utf-8').strip()
                end_time = time.time()
                if response != "ACK_CHUNK":
                    print("Nieoczekiwane potwierdzenie porcji danych.")
                    return
                print(f"Potwierdzenie porcji otrzymane (czas: {end_time - start_time:.2f} s)")

            # Wyślij stopkę
            stopka = b"|XXX\n"
            socket.sendall(stopka)
            print("Wysłano stopkę.")

            # Oczekiwanie na potwierdzenie pliku
            response = socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            end_time_total = time.time()
            if response == "ACK_FILE":
                print(f"Odebrano potwierdzenie odbioru pliku. Całkowity czas wysyłania: {end_time_total - start_time_total:.2f} s")
            else:
                print(f"Otrzymano nieoczekiwaną odpowiedź: {response}")
    except Exception as e:
        print(f"Błąd podczas wysyłania pliku: {e}")

def main():
    start_datetime = datetime.now()

    sciezka_pliku = "C:/Users/ninja/OneDrive/Pulpit/Praca/GUI-Charon/Young Leosia - Szklanki.mp3"

    try:
        # Połącz z serwerem
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_IP, SERVER_PORT))
            print(f"Połączono z serwerem {SERVER_IP}:{SERVER_PORT}")

            # Wysyłanie pliku
            wyslij_plik(client_socket, sciezka_pliku)

    except socket.error as e:
        print(f"Błąd socketu: {e}")
    except KeyboardInterrupt:
        print("\nPrzerwanie programu.")

    end_datetime = datetime.now()
    print(f'Start {start_datetime} \n End {end_datetime}')


if __name__ == "__main__":
    main()
