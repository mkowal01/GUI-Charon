from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import socket


class ConnectTab(QWidget):
    def __init__(self, connect_button, disconnect_button, show_main_ui_callback):
        super().__init__()

        self.connect_button = connect_button
        self.disconnect_button = disconnect_button
        self.show_main_ui_callback = show_main_ui_callback  # Funkcja powrotu do głównego interfejsu
        self.client_socket = None

        self.connection_type_dropdown = None
        self.ip_field = None
        self.port_field = None
        self.com_port_field = None
        self.baud_rate_field = None
        self.log_area = None

        # Główny layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        # Inicjalizacja UI
        self.setup_ui()

    def setup_ui(self):
        """Konfiguruje początkowy interfejs użytkownika."""
        # Lista rozwijana dla typu połączenia
        self.connection_type_dropdown = QComboBox()
        self.connection_type_dropdown.addItems(["Nieustawiono", "LoRa", "WiFi", "Ethernet", "Socket"])
        self.connection_type_dropdown.currentIndexChanged.connect(self.update_connection_form)
        self.layout.addWidget(self.connection_type_dropdown)

        # Dynamiczny formularz
        self.connection_form = QWidget()
        self.connection_form_layout = QVBoxLayout()
        self.connection_form.setLayout(self.connection_form_layout)
        self.layout.addWidget(self.connection_form)

        # Separator
        self.separator_line = QFrame()
        self.separator_line.setFrameShape(QFrame.HLine)
        self.separator_line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.separator_line)

        # Logi
        self.log_area = QLabel("Logi połączenia:")
        self.log_area.setStyleSheet("""
            background-color: #333;
            color: white;
            font-size: 14px;
            padding: 10px;
            border: 1px solid #555;
            border-radius: 5px;
        """)
        self.log_area.setWordWrap(True)
        self.layout.addWidget(self.log_area)

        # Inicjalizacja formularza
        self.update_connection_form(0)

    def update_connection_form(self, index):
        """Aktualizacja dynamicznego formularza w zależności od wybranego typu połączenia."""
        # Czyszczenie dynamicznych widżetów
        while self.connection_form_layout.count():
            item = self.connection_form_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Styl pól tekstowych
        common_style = """
            QLineEdit {
                border: 1px solid #C0C0C0;
                border-radius: 5px;
                padding: 5px;
                background-color: #FFFFFF;
                color: #000000;
            }
            QLineEdit:focus {
                border: 1px solid #1976D2;
            }
        """

        if index == 0:  # Nieustawiono
            self.connection_form_layout.addWidget(QLabel("Wybierz typ połączenia z listy powyżej."))

        elif index == 1:  # LoRa
            self.connection_form_layout.addWidget(QLabel("LoRa Settings"))
            self.com_port_field = QLineEdit()
            self.com_port_field.setPlaceholderText("np. COM3")
            self.com_port_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.com_port_field)

            self.baud_rate_field = QLineEdit()
            self.baud_rate_field.setPlaceholderText("np. 9600")
            self.baud_rate_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.baud_rate_field)

        elif index in [2, 3, 4]:  # WiFi, Ethernet, Socket
            self.connection_form_layout.addWidget(QLabel("Adres IP:"))
            self.ip_field = QLineEdit()
            self.ip_field.setPlaceholderText("np. 127.0.0.1")
            self.ip_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.ip_field)

            self.connection_form_layout.addWidget(QLabel("Port:"))
            self.port_field = QLineEdit()
            self.port_field.setPlaceholderText("np. 12345")
            self.port_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.port_field)

        # Dodanie przycisku "Zatwierdź"
        confirm_button = QPushButton("Zatwierdź")
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #388E3C;
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        confirm_button.clicked.connect(self.handle_connection)
        self.connection_form_layout.addWidget(confirm_button)

    def handle_connection(self):
        """Obsługa logiki połączenia w zależności od wybranego typu."""
        connection_type = self.connection_type_dropdown.currentText()

        if connection_type == "Socket":
            ip = self.ip_field.text() if self.ip_field else None
            port = self.port_field.text() if self.port_field else None

            if not ip or not port:
                self.log_area.setText(self.log_area.text() + "\n[Socket] Adres IP i port muszą być podane!")
                return

            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((ip, int(port)))
                self.log_area.setText(self.log_area.text() + f"\n[Socket] Połączono z {ip}:{port}.")
                self.finalize_connection()
            except Exception as e:
                self.log_area.setText(self.log_area.text() + f"\n[Socket] Błąd połączenia: {e}")

        elif connection_type == "WiFi":
            self.log_area.setText(self.log_area.text() + "\n[WiFi] Obsługa WiFi jeszcze niezaimplementowana.")
        elif connection_type == "LoRa":
            self.log_area.setText(self.log_area.text() + "\n[LoRa] Obsługa LoRa jeszcze niezaimplementowana.")
        elif connection_type == "Ethernet":
            self.log_area.setText(self.log_area.text() + "\n[Ethernet] Obsługa Ethernet jeszcze niezaimplementowana.")
        else:
            self.log_area.setText(self.log_area.text() + "\n[Nieustawiono] Nie wybrano żadnego typu połączenia.")

    def finalize_connection(self):
        """Przełączenie interfejsu po udanym połączeniu."""
        self.connect_button.hide()
        self.disconnect_button.show()

        # Powrót do głównego interfejsu
        if callable(self.show_main_ui_callback):
            self.show_main_ui_callback()

    def handle_disconnect(self):
        """Rozłącza istniejące połączenie."""
        try:
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
                self.log_area.setText(self.log_area.text() + "\n[Socket] Połączenie zostało rozłączone.")
            else:
                self.log_area.setText(self.log_area.text() + "\n[Socket] Nie ma aktywnego połączenia.")
        except Exception as e:
            self.log_area.setText(self.log_area.text() + f"\n[Socket] Błąd podczas rozłączania: {e}")

        # Przywrócenie przycisku "Połącz"
        self.connect_button.show()
        self.disconnect_button.hide()
