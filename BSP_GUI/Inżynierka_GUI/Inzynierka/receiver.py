import socket

def start_receiver():
    host = '127.0.0.1'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print("Odbiornik uruchomiony. Oczekiwanie na dane...")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Połączono z {addr}")
                data = conn.recv(1024).decode()
                if data:
                    print(f"Odebrano: {data}")
                    conn.sendall("Potwierdzam odbiór danych.".encode())

if __name__ == "__main__":
    start_receiver()
