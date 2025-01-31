from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTextEdit, QComboBox, QSizePolicy, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from translatepy import Translate
from Debuger import debug_print
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from os import urandom
import json
from loralibery import encrypt_data, decrypt_data


class TextTab(QWidget):
    def __init__(self, parent=None):  # Dodanie domyślnego argumentu parent
        super().__init__(parent)  # Przekazanie parent do klasy bazowej
        self.parent_window = parent  # Przechowywanie referencji do rodzica

        debug_print("text_tab", f"Inicjalizacja TextTab")

        # Inicjalizacja obiektu Translate
        self.translator = Translate()

        # Główny layout siatki
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        # Ustaw proporcje dla wierszy i kolumn
        for i in range(5):
            self.grid_layout.setRowStretch(i, 1)
            self.grid_layout.setColumnStretch(i, 1)

        # Wstawienie pola do wpisywania tekstu (0,0)
        debug_print("text_tab", f"Tworzenie pola do wpisywania tekstu")
        self.text_input = QTextEdit()
        self.text_input.setFont(QFont("Arial", 22, QFont.Bold))
        self.text_input.setPlaceholderText("Pole do wpisania tekstu")
        self.text_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.text_input, 0, 0, 3, 2)  # rowspan=3, colspan=2

        # Wstawienie listy wyboru języka (0,2)
        debug_print("text_tab", f"Tworzenie listy wyboru języka")
        self.language_selector = QComboBox()
        self.language_selector.setFont(QFont("Arial", 22, QFont.Bold))
        self.language_selector.addItems([
            "Polski", "Angielski", "Niemiecki", "Francuski", "Hiszpański",
            "Ukraiński", "Rosyjski", "Włoski", "Szwedzki", "Norweski"
        ])
        self.language_selector.setCurrentIndex(0)  # Ustawienie domyślnej wartości na "Polski"
        self.language_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.language_selector.currentTextChanged.connect(self.translate_text)
        self.grid_layout.addWidget(self.language_selector, 0, 2, 1, 1)

        # Pole do wyświetlania tłumaczenia (0,3 - 2,4)
        debug_print("text_tab", f"Tworzenie pola do wyświetlania tłumaczenia")
        self.translation_display = QTextEdit()
        self.translation_display.setFont(QFont("Arial", 22, QFont.Bold))
        self.translation_display.setReadOnly(True)
        self.translation_display.setPlaceholderText("Tutaj pojawi się tłumaczenie...")
        self.translation_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.translation_display, 0, 3, 3, 2)

        # Dodanie przycisku "Wyczyść" (1,2)
        debug_print("text_tab", f"Tworzenie przycisku 'Wyczyść'")
        self.clear_button = QPushButton("Wyczyść")
        self.clear_button.setFont(QFont("Arial", 22, QFont.Bold))
        self.clear_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clear_button.clicked.connect(self.clear_text)
        self.grid_layout.addWidget(self.clear_button, 1, 2, 1, 1)

        # Lista komend
        self.commands = [
            "PODĄŻAJ ZA MNĄ", "STÓJ", "LEĆ W GÓRĘ", "LEĆ W DÓŁ",
            "OBRÓĆ W LEWO", "OBRÓĆ W PRAWO", "START", "LĄDUJ",
            "AUTOMATYCZNY", "MANUALNY"
        ]

        self.command_buttons = []  # Przechowywanie referencji do przycisków

        # Dodawanie przycisków do siatki
        row, col = 3, 0
        for command in self.commands:
            button = QPushButton(command)
            button.setFont(QFont("Arial", 22, QFont.Bold))
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect(lambda _, cmd=command: self.send_command(cmd))
            self.command_buttons.append(button)
            self.grid_layout.addWidget(button, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1

        # Dodanie przycisku "WYŚLIJ" (2,2)
        send_button = QPushButton("WYŚLIJ")
        send_button.setFont(QFont("Arial", 22, QFont.Bold))
        send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        send_button.clicked.connect(self.send_text_to_server)
        self.grid_layout.addWidget(send_button, 2, 2)

        self.setLayout(self.grid_layout)

        # Ustawienie stylu na podstawie trybu
        self.update_styles()

    def update_styles(self):
        """Aktualizuje style elementów w zależności od trybu aplikacji."""
        is_dark_mode = self.parent_window.is_dark_mode if self.parent_window else True
        text_color = "white" if is_dark_mode else "black"
        background_color = "#1E1E1E" if is_dark_mode else "white"
        border_color = "#6a5f31" if is_dark_mode else "#A0A0A0"

        self.text_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {background_color};
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 10px;
            }}
        """)
        self.translation_display.setStyleSheet(f"""
            QTextEdit {{
                background-color: {background_color};
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 10px;
            }}
        """)
        self.language_selector.setStyleSheet(f"""
            QComboBox {{
                background-color: {background_color};
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 10px;
                padding: 5px;
            }}
        """)

        for button in self.findChildren(QPushButton):
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {background_color};
                    color: {text_color};
                    border: 2px solid {border_color};
                    border-radius: 10px;
                }}
                QPushButton:hover {{
                    background-color: {border_color};
                    color: white;
                }}
            """)

    def translate_text(self):
        """Tłumaczy tekst w polu tekstowym na wybrany język."""
        source_text = self.text_input.toPlainText().strip()
        if not source_text:
            self.translation_display.clear()
            return

        target_language_map = {
            "Polski": "pl",
            "Angielski": "en",
            "Niemiecki": "de",
            "Francuski": "fr",
            "Hiszpański": "es",
            "Ukraiński": "uk",
            "Rosyjski": "ru",
            "Włoski": "it",
            "Szwedzki": "sv",
            "Norweski": "no"
        }

        target_language = target_language_map.get(self.language_selector.currentText(), "pl")

        try:
            translation = self.translator.translate(source_text, target_language)
            self.translation_display.setPlainText(translation.result)
            debug_print("text_tab", f"Tłumaczenie na {self.language_selector.currentText()}: {translation.result}")
        except Exception as e:
            QMessageBox.critical(self, debug_print("text_tab", f"Błąd", f"Nie udało się przetłumaczyć tekstu: {e}"))

    def clear_text(self):
        """Czyści pola tekstowe i tłumaczenia."""
        self.text_input.clear()
        self.translation_display.clear()

    def is_connected(self):
        """Sprawdza, czy aplikacja jest połączona z serwerem."""
        if not self.parent_window or not hasattr(self.parent_window, 'connect_tab'):
            QMessageBox.warning(self, "Brak połączenia", "Nie można wykonać akcji. Brak połączenia z serwerem.")
            return False

        connect_tab = self.parent_window.connect_tab
        if not connect_tab.connected:
            QMessageBox.warning(self, "Brak połączenia", "Nie jesteś połączony z serwerem. Proszę się połączyć.")
            return False

        return True

    def send_text_to_server(self):
        """
        Wysyła zaszyfrowany tekst na serwer z "TX" i indeksami kluczy.
        Obsługuje zarówno sockety, jak i LoRę.
        """
        if not self.is_connected():
            return

        translated_text = self.translation_display.toPlainText().strip()
        user_text = self.text_input.toPlainText().strip()

        if translated_text:
            command = "TX " + translated_text
        elif user_text:
            command = "TX " + user_text
        else:
            QMessageBox.warning(self, "Błąd", "Pole tekstowe i tłumaczenie są puste. Wpisz tekst, aby go wysłać.")
            return

        try:
            # Ścieżka do pliku JSON z połówkami kluczy
            json_file = "half_keys_indexed.json"

            # Sprawdzenie istnienia pliku
            import os
            if not os.path.exists(json_file):
                QMessageBox.critical(self, "Błąd wysyłania", f"Plik kluczy {json_file} nie istnieje.")
                return

            # Szyfrowanie komendy z prefiksem "TX"
            # encrypted_command = encrypt_data(translated_command.encode('utf-8'), json_file)
            encrypted_data, index1, index2, iv, tag = encrypt_data(command.encode('utf-8'))
            message = (index1.to_bytes(1, 'little') +
                       index2.to_bytes(1, 'big') +
                       iv +
                       encrypted_data +
                       tag)
            # Wysyłanie danych przez socket lub LoRę
            connect_tab = self.parent_window.connect_tab
            response = ""

            if connect_tab.connection_type.currentText() == "Socket/WiFi/Ethernet":
                connect_tab.sock.sendall(message)
                debug_print("text_tab", f"Wysłano zaszyfrowaną wiadomość przez socket: {message}")

                # Oczekiwanie na odpowiedź
                connect_tab.sock.settimeout(5)  # Timeout na 5 sekund
                response = connect_tab.sock.recv(1024)  # Odbiór do 1024 bajtów
                self.handle_server_response(response)
                debug_print("text_tab", f"Otrzymano odpowiedź z serwera: {response}")

            elif connect_tab.connection_type.currentText() == "LoRa":
                connect_tab.serial_conn.write(message)
                debug_print("text_tab", f"Wysłano zaszyfrowaną wiadomość przez LoRę: {message}")

                # Oczekiwanie na odpowiedź (dla LoRy trzeba odpowiednio skonfigurować)
                response = connect_tab.serial_conn.read_until( b'\n')  # Przykład: oczekiwanie na dane zakończone znakiem nowej linii
                self.handle_server_response(response)
                debug_print("text_tab", f"Otrzymano odpowiedź przez LoRę: {response}")
            else:
                QMessageBox.warning(self, "Błąd", "Niewłaściwy typ połączenia.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd wysyłania", f"Nie udało się wysłać wiadomości: {e}")

    def send_command(self, command):
        """
        Wysyła wybraną komendę zaszyfrowaną z "TX" i indeksami kluczy.
        Obsługuje zarówno sockety, jak i LoRę.
        """
        if not self.is_connected():
            return

        if not command:
            QMessageBox.warning(self, "Błąd", "Komenda jest pusta. Nie można jej wysłać.")
            return

        target_language_map = {
            "Polski": "pl",
            "Angielski": "en",
            "Niemiecki": "de",
            "Francuski": "fr",
            "Hiszpański": "es",
            "Ukraiński": "uk",
            "Rosyjski": "ru",
            "Włoski": "it",
            "Szwedzki": "sv",
            "Norweski": "no"
        }

        target_language = target_language_map.get(self.language_selector.currentText(), "pl")

        try:
            translation = self.translator.translate(command, target_language)
            translated_command = "TX " + translation.result

            # Ścieżka do pliku JSON z połówkami kluczy
            json_file = "half_keys_indexed.json"

            # Sprawdzenie istnienia pliku
            import os
            if not os.path.exists(json_file):
                QMessageBox.critical(self, "Błąd wysyłania", f"Plik kluczy {json_file} nie istnieje.")
                return

            # Szyfrowanie komendy z prefiksem "TX"
            # encrypted_command = encrypt_data(translated_command.encode('utf-8'), json_file)
            encrypted_data, index1, index2, iv, tag = encrypt_data(translated_command.encode('utf-8'))
            message = (index1.to_bytes(1, 'little') +
                       index2.to_bytes(1, 'big') +
                       iv +
                       encrypted_data +
                       tag)
            # Wysyłanie danych przez socket lub LoRę
            connect_tab = self.parent_window.connect_tab
            response = None

            if connect_tab.connection_type.currentText() == "Socket/WiFi/Ethernet":
                connect_tab.sock.sendall(message)
                debug_print("text_tab", f"Wysłano zaszyfrowaną komendę przez socket: {message.hex()}")

                # Oczekiwanie na odpowiedź
                connect_tab.sock.settimeout(5)  # Timeout na 5 sekund
                response = connect_tab.sock.recv(1024)  # Odbiór do 1024 bajtów
                self.handle_server_response(response)
                debug_print("text_tab", f"Otrzymano odpowiedź z serwera: {response}")

            elif connect_tab.connection_type.currentText() == "LoRa":
                connect_tab.serial_conn.write(message)
                debug_print("text_tab", f"Wysłano zaszyfrowaną komendę przez LoRę: {message.hex()}")

                # Oczekiwanie na odpowiedź (dla LoRy trzeba odpowiednio skonfigurować)
                response = connect_tab.serial_conn.read_until(b'\n')  # Przykład: oczekiwanie na dane zakończone znakiem nowej linii
                self.handle_server_response(response)
                debug_print("text_tab", f"Otrzymano odpowiedź przez LoRę: {response}")
            else:
                QMessageBox.warning(self, "Błąd", "Niewłaściwy typ połączenia.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd wysyłania", f"Nie udało się wysłać komendy: {e}")

    def setup_command_buttons(self):
        """Tworzy przyciski komend z obsługą sprawdzania połączenia."""
        row, col = 3, 0
        for command in self.commands:
            button = QPushButton(command)
            button.setFont(QFont("Arial", 10))
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect(lambda _, cmd=command: self.send_command(cmd))
            self.command_buttons.append(button)
            self.grid_layout.addWidget(button, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1

    def handle_server_response(self, response: bytes):
        """
        Obsługuje odpowiedź z serwera, dekodując ją i wyświetlając w logach.

        Args:
            response (bytes): Odebrane dane z serwera.
        """
        try:
            # Rozpakowanie wiadomości (zakładamy format zgodny z funkcją szyfrowania)
            index1 = response[0]
            index2 = response[1]
            iv = response[2:14]  # 12 bajtów IV
            tag = response[-16:]  # Ostatnie 16 bajtów to tag
            encrypted_data = response[14:-16]  # Reszta to dane

            # Dekodowanie wiadomości
            decrypted_message = decrypt_data(encrypted_data, index1, index2, iv, tag)
            debug_print("text_tab", f"Otrzymano i odszyfrowano wiadomość: {decrypted_message}")

            # Przekazanie do logów LocalizationTab
            if hasattr(self.parent_window, 'localization_tab'):
                self.parent_window.localization_tab.update_logs(decrypted_message)
                debug_print("text_tab", "Przekazano odszyfrowaną wiadomość do LocalizationTab.")
            else:
                debug_print("text_tab", "Nie znaleziono LocalizationTab w parent_window.")
        except Exception as e:
            debug_print("text_tab", f"Błąd podczas obsługi odpowiedzi: {e}")
