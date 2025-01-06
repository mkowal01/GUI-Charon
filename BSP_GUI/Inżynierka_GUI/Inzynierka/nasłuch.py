import socket
import threading

def server_mode(port):
    """Uruchamia tryb serwera."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print(f"[SERVER] Serwer nasłuchuje na porcie {port}...")

    def handle_client(client_socket, address):
        print(f"[SERVER] Połączono z {address}")
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                    # Serwer: log przy zamykaniu połączenia
                print(f"[SERVER] Połączenie z {address} zostało zakończone przez klienta.")
                print(f"[SERVER] Odebrano od {address}: {data.decode('utf-8')}")
                client_socket.sendall("Wiadomość odebrana.\n".encode('utf-8'))
        except ConnectionResetError:
            print(f"[SERVER] Połączenie z {address} zostało przerwane.")
        finally:
            print(f"[SERVER] Rozłączono z {address}")
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

    while True:
        message = input("[CLIENT] Wpisz wiadomość (lub 'exit' aby zakończyć): ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"[CLIENT] Odpowiedź serwera: {response}")

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
