from PyQt5.QtCore import QThread, pyqtSignal
import socket


class SocketThread(QThread):
    connection_success = pyqtSignal(str)
    connection_error = pyqtSignal(str)
    received_data = pyqtSignal(str)

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port
        self.running = True

    def on_connection_success(self, message):
        """Obsługa sukcesu połączenia."""
        # noinspection PyMethodMayBeStatic
        print(message)

    def on_connection_error(self, message):
        """Obsługa błędu połączenia."""
        # noinspection PyMethodMayBeStatic
        print(message)

    def on_received_data(self, message):
        """Obsługa odebranych danych."""
        # noinspection PyMethodMayBeStatic
        print(message)

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(5)
                self.connection_success.emit(f"[Socket] Próbuję połączyć z {self.ip}:{self.port}...")
                client_socket.connect((self.ip, int(self.port)))
                self.connection_success.emit(f"[Socket] Połączono z {self.ip}:{self.port}.")

                # Wysłanie danych do serwera
                message = "Testowa wiadomość od klienta.\n"
                client_socket.sendall(message.encode('utf-8'))

                # Odbiór danych
                response = client_socket.recv(1024).decode('utf-8')
                self.received_data.emit(f"[Socket] Odebrano od serwera: {response}")

        except Exception as e:
            self.connection_error.emit(f"[Socket] Wystąpił błąd: {e}")

