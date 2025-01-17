from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTextEdit, QComboBox, QSizePolicy, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from translatepy import Translate
from Debuger import debug_print


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
        self.text_input.setFont(QFont("Arial", 16))
        self.text_input.setPlaceholderText("Pole do wpisania tekstu")
        self.text_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.text_input, 0, 0, 3, 2)  # rowspan=3, colspan=2

        # Wstawienie listy wyboru języka (0,2)
        debug_print("text_tab", f"Tworzenie listy wyboru języka")
        self.language_selector = QComboBox()
        self.language_selector.setFont(QFont("Arial", 12))
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
        self.translation_display.setFont(QFont("Arial", 16))
        self.translation_display.setReadOnly(True)
        self.translation_display.setPlaceholderText("Tutaj pojawi się tłumaczenie...")
        self.translation_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.translation_display, 0, 3, 3, 2)

        # Dodanie przycisku "Wyczyść" (1,2)
        debug_print("text_tab", f"Tworzenie przycisku 'Wyczyść'")
        self.clear_button = QPushButton("Wyczyść")
        self.clear_button.setFont(QFont("Arial", 12))
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
            button.setFont(QFont("Arial", 10))
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
        send_button.setFont(QFont("Arial", 12, QFont.Bold))
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
        """Wysyła przetłumaczony tekst lub tekst użytkownika na serwer."""
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
            connect_tab = self.parent_window.connect_tab
            if connect_tab.connection_type.currentText() == "Socket/WiFi/Ethernet":
                connect_tab.sock.sendall(command.encode('utf-8'))
                debug_print("text_tab", f"Wysłano: {command}")
            elif connect_tab.connection_type.currentText() == "LoRa":
                connect_tab.serial_conn.write(command.encode('utf-8'))
                debug_print("text_tab", f"Wysłano przez LoRa: {command}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd wysyłania", f"Nie udało się wysłać: {e}")

    def send_command(self, command):
        """Wysyła wybraną komendę bezpośrednio."""
        if not self.is_connected():
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
            connect_tab = self.parent_window.connect_tab

            if connect_tab.connection_type.currentText() == "Socket/WiFi/Ethernet":
                connect_tab.sock.sendall(translated_command.encode('utf-8'))
                debug_print("text_tab", f"Wysłano: {translated_command}")
            elif connect_tab.connection_type.currentText() == "LoRa":
                connect_tab.serial_conn.write(translated_command.encode('utf-8'))
                debug_print("text_tab", f"Wysłano przez LoRa: {translated_command}")
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
