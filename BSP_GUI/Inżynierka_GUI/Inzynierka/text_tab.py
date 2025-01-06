from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTextEdit, QComboBox, QSizePolicy, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from translatepy import Translate


class TextTab(QWidget):
    def __init__(self, parent=None):  # Dodanie domyślnego argumentu parent
        super().__init__(parent)  # Przekazanie parent do klasy bazowej
        self.parent_window = parent  # Przechowywanie referencji do rodzica

        print("Inicjalizacja TextTab")

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
        print("Tworzenie pola do wpisywania tekstu")
        self.text_input = QTextEdit()
        self.text_input.setFont(QFont("Arial", 16))
        self.text_input.setPlaceholderText("Pole do wpisania tekstu")
        self.text_input.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 10px;")
        self.text_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.text_input, 0, 0, 3, 2)  # rowspan=3, colspan=2

        # Wstawienie listy wyboru języka (0,2)
        print("Tworzenie listy wyboru języka")
        self.language_selector = QComboBox()
        self.language_selector.setFont(QFont("Arial", 12))
        self.language_selector.addItems([
            "Polski", "Angielski", "Niemiecki", "Francuski", "Hiszpański",
            "Ukraiński", "Rosyjski", "Włoski", "Szwedzki", "Norweski"
        ])
        self.language_selector.setCurrentIndex(0)  # Ustawienie domyślnej wartości na "Polski"
        self.language_selector.setStyleSheet(
            "QComboBox {"
            "    background-color: white;"
            "    border: 1px solid black;"
            "    border-radius: 15px;"
            "    padding: 5px;"
            "    text-align: center;"
            "}"
            "QComboBox::drop-down {"
            "    border: none;"
            "    width: 0px;"  # Ukrycie strzałki
            "}"
            "QComboBox QAbstractItemView {"
            "    border: 1px solid black;"
            "    border-radius: 15px;"
            "    background-color: #1976D2;"  # Kolor tła
            "    color: white;"
            "    selection-background-color: #0D47A1;"
            "    selection-color: white;"
            "    outline: none;"  # Usunięcie linii przerywanej
            "    padding: 0px;"  # Usunięcie białych końców
            "    margin: 0px;"  # Usunięcie marginesów
            "}"
            "QScrollBar:vertical {"
            "    border: none;"
            "    background-color: #1976D2;"
            "    width: 12px;"
            "    margin: 3px 0px 3px 0px;"
            "    border-radius: 6px;"  # Zaokrąglenie paska przewijania
            "}"
            "QScrollBar::handle:vertical {"
            "    background-color: #0D47A1;"
            "    min-height: 20px;"
            "    border-radius: 6px;"  # Zaokrąglenie uchwytu
            "}"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {"
            "    background: none;"
            "    height: 0px;"
            "}"  # Usunięcie przycisków przewijania
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {"
            "    background: none;"
            "}"  # Ukrycie dodatkowego tła przewijania
        )
        self.language_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.language_selector.currentTextChanged.connect(self.translate_text)
        self.grid_layout.addWidget(self.language_selector, 0, 2, 1, 1)

        # Pole do wyświetlania tłumaczenia (0,3 - 2,4)
        print("Tworzenie pola do wyświetlania tłumaczenia")
        self.translation_display = QTextEdit()
        self.translation_display.setFont(QFont("Arial", 16))
        self.translation_display.setReadOnly(True)
        self.translation_display.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 10px;")
        self.translation_display.setPlaceholderText("Tutaj pojawi się tłumaczenie...")
        self.translation_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.translation_display, 0, 3, 3, 2)

        # Dodanie przycisku "Wyczyść" (1,2)
        print("Tworzenie przycisku 'Wyczyść'")
        self.clear_button = QPushButton("Wyczyść")
        self.clear_button.setFont(QFont("Arial", 12))
        self.clear_button.setStyleSheet(
            "QPushButton {"
            "    background-color: lightgray;"
            "    border: 1px solid black;"
            "    border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: gray;"
            "    color: white;"
            "}"
        )
        self.clear_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clear_button.clicked.connect(self.clear_text)
        self.grid_layout.addWidget(self.clear_button, 1, 2, 1, 1)

        # Lista komend
        commands = [
            "PODĄŻAJ ZA MNĄ", "STÓJ", "LEĆ W GÓRĘ", "LEĆ W DÓŁ",
            "OBRÓĆ W LEWO", "OBRÓĆ W PRAWO", "START", "LĄDUJ",
            "AUTOMATYCZNY", "MANUALNY"
        ]

        # Dodawanie przycisków do siatki
        row, col = 3, 0
        for command in commands:
            button = QPushButton(command)
            button.setFont(QFont("Arial", 10))
            button.setStyleSheet("""
                QPushButton {
                    border: 1px solid black; 
                    background-color: lightblue; 
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: blue; 
                    color: white;
                }
            """)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect(lambda _, cmd=command: self.send_translated_command(cmd))
            self.grid_layout.addWidget(button, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1

        # Dodanie przycisku "WYŚLIJ" (2,2)
        send_button = QPushButton("WYŚLIJ")
        send_button.setFont(QFont("Arial", 12, QFont.Bold))
        send_button.setStyleSheet("""
            QPushButton {
                border: 1px solid black; 
                background-color: orange; 
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: blue; 
                color: white;
            }
        """)
        send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        send_button.clicked.connect(self.send_text_to_server)
        self.grid_layout.addWidget(send_button, 2, 2)

        self.setLayout(self.grid_layout)

    def translate_text(self, text):
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
            print(f"[DEBUG] Tłumaczenie na {self.language_selector.currentText()}: {translation.result}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się przetłumaczyć tekstu: {e}")

    def clear_text(self):
        """Czyści pola tekstowe i tłumaczenia."""
        self.text_input.clear()
        self.translation_display.clear()

    def send_text_to_server(self):
        """Wysyła przetłumaczony tekst lub tekst użytkownika na serwer."""
        translated_text = self.translation_display.toPlainText().strip()
        user_text = self.text_input.toPlainText().strip()

        if translated_text:
            self.send_command("TX " + translated_text)
        elif user_text:
            self.send_command("TX " + user_text)
        else:
            QMessageBox.warning(self, "Błąd", "Pole tekstowe i tłumaczenie są puste. Wpisz tekst, aby go wysłać.")

    def send_translated_command(self, phrase):
        """Tłumaczy i wysyła wybraną frazę w odpowiednim języku."""
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
            translation = self.translator.translate(phrase, target_language)
            self.send_command("TX " + translation.result)
            print(
                f"[DEBUG] Wysłano przetłumaczoną frazę ({self.language_selector.currentText()}): {translation.result}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się przetłumaczyć frazy: {e}")

    def send_command(self, command):
        parent = self.parent_window
        if hasattr(parent, 'client_socket') and parent.client_socket:
            try:
                parent.client_socket.sendall(command.encode('utf-8'))
                print(f"Wysłano: {command}")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się wysłać: {e}")
        else:
            QMessageBox.warning(self, "Brak połączenia", "Nie jesteś połączony z serwerem.")
