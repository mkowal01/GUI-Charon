from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
import socket
import serial
from Debuger import debug_print

class ConnectTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent
        self.connected = False  # Stan połączenia
        debug_print("connection_tab", f"connection")
        debug_print("connection_tab", f"Inicjalizacja ConnectTab")

        # Layout główny zakładki
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Layout dla wyboru trybu połączenia (nad zakładkami)
        self.connection_bar = QWidget()
        self.connection_bar.setFixedHeight(60)
        self.connection_bar_layout = QHBoxLayout()
        self.connection_bar_layout.setContentsMargins(10, 0, 10, 0)
        self.connection_bar_layout.setSpacing(10)
        self.connection_bar.setLayout(self.connection_bar_layout)

        # Dropdown wyboru metody połączenia
        self.connection_type = QComboBox()
        self.connection_type.addItems(["Socket/WiFi/Ethernet", "LoRa"])
        self.connection_type.setFixedSize(200, 40)
        self.connection_type.setStyleSheet("""
            QComboBox {
                border: 2px solid #1976D2;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: white;
                background-color: #121212;
            }
            QComboBox::drop-down {
                border: 0px;
            }
        """)
        self.connection_type.currentIndexChanged.connect(self.update_connection_fields)
        self.connection_bar_layout.addWidget(self.connection_type)

        # Pole do wpisywania IP (dla Socket/WiFi/Ethernet)
        self.ip_label = QLabel("IP Address:")
        self.ip_label.setStyleSheet("color: white; font-size: 14px;")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("127.0.0.1")
        self.ip_input.setFixedSize(150, 40)
        self.ip_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #1976D2;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: white;
                background-color: #121212;
            }
        """)
        self.connection_bar_layout.addWidget(self.ip_label)
        self.connection_bar_layout.addWidget(self.ip_input)

        # Pole do wpisywania Portu (dla Socket/WiFi/Ethernet)
        self.port_label = QLabel("Port:")
        self.port_label.setStyleSheet("color: white; font-size: 14px;")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("12345")
        self.port_input.setFixedSize(150, 40)
        self.port_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #1976D2;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: white;
                background-color: #121212;
            }
        """)
        self.connection_bar_layout.addWidget(self.port_label)
        self.connection_bar_layout.addWidget(self.port_input)

        # Pole do wpisywania COM (dla LoRa)
        self.com_label = QLabel("Podaj COM:")
        self.com_label.setStyleSheet("color: white; font-size: 14px;")
        self.com_port_input = QLineEdit()
        self.com_port_input.setPlaceholderText("Podaj COM")
        self.com_port_input.setFixedSize(150, 40)
        self.com_port_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #1976D2;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: white;
                background-color: #121212;
            }
        """)
        self.connection_bar_layout.addWidget(self.com_label)
        self.connection_bar_layout.addWidget(self.com_port_input)

        # Pole do wpisywania Baud Rate (dla LoRa)
        self.baud_label = QLabel("Baud Rate:")
        self.baud_label.setStyleSheet("color: white; font-size: 14px;")
        self.baud_rate_input = QLineEdit()
        self.baud_rate_input.setPlaceholderText("Baud Rate")
        self.baud_rate_input.setFixedSize(150, 40)
        self.baud_rate_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #1976D2;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: white;
                background-color: #121212;
            }
        """)
        self.connection_bar_layout.addWidget(self.baud_label)
        self.connection_bar_layout.addWidget(self.baud_rate_input)

        # Przycisk zatwierdzenia
        self.confirm_button = QPushButton("Zatwierdź")
        self.confirm_button.setFixedSize(150, 40)
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border-radius: 10px;
                border: 2px solid #1976D2;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.confirm_button.clicked.connect(self.toggle_connection)
        self.connection_bar_layout.addWidget(self.confirm_button)

        # Przycisk powrotu do głównego widoku
        self.back_button = QPushButton("Wróć")
        self.back_button.setFixedSize(150, 40)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #FF6F00;
                color: white;
                border-radius: 10px;
                border: 2px solid #FF6F00;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
        """)
        self.back_button.clicked.connect(self.go_back_to_main)
        self.connection_bar_layout.addWidget(self.back_button)

        # Komunikat o stanie połączenia
        self.status_label = QLabel("Nie połączono")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; color: red;")
        self.main_layout.addWidget(self.connection_bar)
        self.main_layout.addWidget(self.status_label)

        # Ukrycie pól dla LoRa na starcie
        self.com_label.hide()
        self.com_port_input.hide()
        self.baud_label.hide()
        self.baud_rate_input.hide()

        debug_print("connection_tab", f"ConnectTab zainicjalizowany poprawnie")

    def update_connection_fields(self):
        """Aktualizuje widoczność pól w zależności od wybranej metody połączenia."""
        debug_print("connection_tab", f"Wybrano metodę połączenia: {self.connection_type.currentText()}")
        if self.connection_type.currentText() == "LoRa":
            # Pokazujemy pola dla LoRa
            self.ip_label.hide()
            self.ip_input.hide()
            self.port_label.hide()
            self.port_input.hide()
            self.com_label.show()
            self.com_port_input.show()
            self.baud_label.show()
            self.baud_rate_input.show()

            # Ustawiamy domyślne wartości dla LoRa
            if not self.com_port_input.text():  # Jeśli pole COM jest puste
                self.com_port_input.setText("COM8")
            if not self.baud_rate_input.text():  # Jeśli pole Baud Rate jest puste
                self.baud_rate_input.setText("9600")
        else:
            # Pokazujemy pola dla Socket/WiFi/Ethernet
            self.com_label.hide()
            self.com_port_input.hide()
            self.baud_label.hide()
            self.baud_rate_input.hide()
            self.ip_label.show()
            self.ip_input.show()
            self.port_label.show()
            self.port_input.show()

    def toggle_connection(self):
        """Obsługuje nawiązywanie i rozłączanie połączenia."""
        if self.connected:
            self.disconnect()
        else:
            self.confirm_connection()

    def confirm_connection(self):
        """Nawiązuje połączenie w zależności od wybranej metody."""
        connection_type = self.connection_type.currentText()
        debug_print("connection_tab", f"Wybrano metodę połączenia: {connection_type}")
        try:
            if connection_type == "Socket/WiFi/Ethernet":
                ip_address = self.ip_input.text() or "127.0.0.1"
                port = int(self.port_input.text() or "12345")
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(5)  # Timeout 5 sekund
                self.sock.connect((ip_address, port))
                self.status_label.setText(f"Połączono z {ip_address}:{port}")
                self.status_label.setStyleSheet("font-size: 18px; color: green;")
                self.confirm_button.setText("Rozłącz")
                self.connected = True
                debug_print("connection_tab", f"Połączono z {ip_address}:{port}")
            elif connection_type == "LoRa":
                com_port = self.com_port_input.text()
                baud_rate = int(self.baud_rate_input.text())
                self.serial_conn = serial.Serial(com_port, baud_rate, timeout=2)
                self.status_label.setText(f"Połączono z LoRa (COM: {com_port}, Baud: {baud_rate})")
                self.status_label.setStyleSheet("font-size: 18px; color: green;")
                self.confirm_button.setText("Rozłącz")
                self.connected = True
                debug_print("connection_tab", f"Połączono z LoRa (COM: {com_port}, Baud: {baud_rate})")
            else:
                self.status_label.setText("Nieznana metoda połączenia")
                self.status_label.setStyleSheet("font-size: 18px; color: red;")
        except Exception as e:
            self.status_label.setText(f"Błąd połączenia: {e}")
            self.status_label.setStyleSheet("font-size: 18px; color: red;")
            debug_print("connection_tab", f"Nie udało się połączyć: {e}")

    def disconnect(self):
        """Rozłącza aktywne połączenie."""
        try:
            if self.connection_type.currentText() == "Socket/WiFi/Ethernet" and hasattr(self, 'sock'):
                self.sock.close()
                debug_print("connection_tab", f"Rozłączono z Socket/WiFi/Ethernet")
            elif self.connection_type.currentText() == "LoRa" and hasattr(self, 'serial_conn'):
                self.serial_conn.close()
                debug_print("connection_tab", f"Rozłączono z LoRa")
            self.status_label.setText("Nie połączono")
            self.status_label.setStyleSheet("font-size: 18px; color: red;")
            self.confirm_button.setText("Zatwierdź")
            self.connected = False
        except Exception as e:
            debug_print("connection_tab", f"[ERROR] Nie udało się rozłączyć: {e}")

    def go_back_to_main(self):
        """Powrót do głównego widoku aplikacji."""
        debug_print("connection_tab", f"Powrót do głównego widoku")
        if self.parent:
            self.parent.show_main_ui()
            self.parent.update_connect_button("Rozłącz" if self.connected else "Połącz")
