from PyQt5.QtWidgets import QWidget, QGridLayout, QTextEdit, QComboBox, QSizePolicy, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from translatepy import Translate


class AudioTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        print("Inicjalizacja AudioTab")

        # Inicjalizacja obiektu Translate
        self.translator = Translate()

        # Główny layout siatki
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        # Pole do wpisywania tekstu (0,0) do (1,1)
        self.text_input = QTextEdit()
        self.text_input.setFont(QFont("Arial", 16))
        self.text_input.setPlaceholderText("Pole do wpisania tekstu")
        self.text_input.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 10px;")
        self.text_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.text_input, 0, 0, 2, 2)

        # Pole do wyświetlania tłumaczenia (2,0) do (3,1)
        self.translation_display = QTextEdit()
        self.translation_display.setFont(QFont("Arial", 16))
        self.translation_display.setReadOnly(True)
        self.translation_display.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 10px;")
        self.translation_display.setPlaceholderText("Tutaj pojawi się tłumaczenie...")
        self.translation_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.translation_display, 2, 0, 2, 2)

        # Przycisk do nagrywania (4,0)
        self.record_button = QPushButton("Nagrywanie")
        self.record_button.setFont(QFont("Arial", 12))
        self.record_button.setStyleSheet(
            "QPushButton {"
            "    background-color: lightgreen;"
            "    border: 1px solid black;"
            "    border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: green;"
            "    color: white;"
            "}"
        )
        self.record_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.record_button, 4, 0)

        # Przycisk do odtwarzania (4,1)
        self.play_button = QPushButton("Odtwarzanie nagrania")
        self.play_button.setFont(QFont("Arial", 12))
        self.play_button.setStyleSheet(
            "QPushButton {"
            "    background-color: lightblue;"
            "    border: 1px solid black;"
            "    border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: blue;"
            "    color: white;"
            "}"
        )
        self.play_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.play_button, 4, 1)

        # Przycisk do kasowania nagrania (4,2)
        self.delete_button = QPushButton("Kasowanie nagrania")
        self.delete_button.setFont(QFont("Arial", 12))
        self.delete_button.setStyleSheet(
            "QPushButton {"
            "    background-color: lightcoral;"
            "    border: 1px solid black;"
            "    border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: red;"
            "    color: white;"
            "}"
        )
        self.delete_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.delete_button, 4, 2)

        # Wybór języka (0,2)
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
            "}"
            "QComboBox:hover {"
            "    background-color: lightgray;"
            "}"
        )
        self.language_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.language_selector.currentTextChanged.connect(self.on_language_changed)
        self.grid_layout.addWidget(self.language_selector, 0, 2)

        # Przycisk "Wyczyść" (1,2)
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
        self.grid_layout.addWidget(self.clear_button, 1, 2)

        # Przycisk "Wyślij" (2,2)
        self.send_button = QPushButton("WYŚLIJ")
        self.send_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.send_button.setStyleSheet(
            "QPushButton {"
            "    border: 1px solid black;"
            "    background-color: orange;"
            "    border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: blue;"
            "    color: white;"
            "}"
        )
        self.send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.send_button.clicked.connect(self.send_translated_command)
        self.grid_layout.addWidget(self.send_button, 2, 2)

        # Gotowe zwroty (0,3) do (4,4)
        phrases = [
            "PODĄŻAJ ZA MNĄ", "STÓJ", "LEĆ W GÓRĘ", "LEĆ W DÓŁ",
            "OBRÓĆ W LEWO", "OBRÓĆ W PRAWO", "START", "LĄDUJ",
            "AUTOMATYCZNY", "MANUALNY"
        ]

        row, col = 0, 3
        for phrase in phrases:
            phrase_button = QPushButton(phrase)
            phrase_button.setFont(QFont("Arial", 10))
            phrase_button.setStyleSheet(
                "QPushButton {"
                "    border: 1px solid black;"
                "    background-color: lightblue;"
                "    border-radius: 10px;"
                "}"
                "QPushButton:hover {"
                "    background-color: blue;"
                "    color: white;"
                "}"
            )
            phrase_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            phrase_button.clicked.connect(lambda _, ph=phrase: self.send_translated_phrase(ph))
            self.grid_layout.addWidget(phrase_button, row, col)
            col += 1
            if col > 4:
                col = 3
                row += 1

        self.setLayout(self.grid_layout)

    def clear_text(self):
        """Czyści pola tekstowe i tłumaczenia."""
        self.text_input.clear()
        self.translation_display.clear()

    def send_translated_command(self):
        """Wysyła przetłumaczony tekst lub tekst użytkownika na serwer."""
        translated_text = self.translation_display.toPlainText().strip()
        user_text = self.text_input.toPlainText().strip()

        if translated_text:
            self.send_command("AU " + translated_text)
        elif user_text:
            self.send_command("AU " + user_text)
        else:
            QMessageBox.warning(self, "Błąd", "Pole tekstowe i tłumaczenie są puste. Wpisz tekst, aby go wysłać.")

    def send_translated_phrase(self, phrase):
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
            print(f"[DEBUG] Wysłano przetłumaczoną frazę ({self.language_selector.currentText()}): {translation.result}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się przetłumaczyć frazy: {e}")

    def on_language_changed(self):
        """Obsługuje automatyczne tłumaczenie tekstu przy zmianie języka."""
        self.translate_text()

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
            print(f"[DEBUG] Tłumaczenie na {self.language_selector.currentText()}: {translation.result}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się przetłumaczyć tekstu: {e}")

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
