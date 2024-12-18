import socket
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel


class AudioTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel("Wybierz plik audio do wysłania:")
        layout.addWidget(self.label)

        self.send_file_button = QPushButton("Wybierz i wyślij plik audio")
        self.send_file_button.clicked.connect(self.send_file)
        layout.addWidget(self.send_file_button)

        self.setLayout(layout)

    def send_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik audio", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            file_name = file_path.split("/")[-1]
            with open(file_path, "rb") as file:
                file_data = file.read()
            self.send_data(f"FILE:{file_name}".encode() + b"\n" + file_data)

    def send_data(self, data):
        host = '127.0.0.1'
        port = 12345
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))
                client_socket.sendall(data)
                print("Wysłano plik audio")
        except Exception as e:
            print(f"Błąd: {e}")
