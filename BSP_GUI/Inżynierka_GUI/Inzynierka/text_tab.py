import socket
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon


class TextTab(QWidget):
    def __init__(self):
        super().__init__()

        # Główny layout siatki
        layout = QGridLayout()
        layout.setSpacing(10)  # Ustaw odstępy między elementami

        # Pole tekstowe (lewa górna część)
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Wpisz tekst tutaj...")
        self.text_input.setFont(QFont("Times New Roman", 12))
        self.text_input.setFixedSize(600, 200)
        layout.addWidget(self.text_input, 0, 0, 4, 4)  # Zajmuje kilka kolumn i wierszy

        # Strzałka (obrazek/ikona nieaktywna)
        self.arrow_label = QLabel()
        self.arrow_label.setFixedSize(50, 50)
        self.arrow_label.setStyleSheet("border: 2px solid black; background-color: #E0E0E0;")
        layout.addWidget(self.arrow_label, 0, 4, alignment=Qt.AlignCenter)

        # Lista wyboru języka (po prawej stronie)
        self.language_label = QLabel("Język:")
        self.language_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.language_label, 0, 5)

        self.language_combo = QComboBox()
        self.language_combo.addItems(["Polski", "Angielski", "Niemiecki", "Francuski", "Hiszpański", "Ukraiński", "Rosyjski", "Włoski"])
        self.language_combo.setFixedWidth(150)
        layout.addWidget(self.language_combo, 0, 6)

        # Lista wyboru czcionki (poniżej języka)
        self.font_label = QLabel("Czcionka:")
        self.font_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.font_label, 2, 5)

        self.font_combo = QComboBox()
        self.font_combo.addItems(["10x20.bdf", "6x12.bdf", "7x14.bdf", "8x13.bdf", "9x18.bdf", "helvR12.bdf"])
        self.font_combo.setFixedWidth(150)
        layout.addWidget(self.font_combo, 2, 6)

        # Przycisk "Gotowe Zwroty" (poniżej czcionki)
        self.ready_phrases_button = QPushButton("Gotowe Zwroty")
        self.ready_phrases_button.clicked.connect(self.toggle_ready_phrases)
        self.ready_phrases_button.setFixedWidth(150)
        layout.addWidget(self.ready_phrases_button, 4, 6)

        # Kontener gotowych zwrotów (ukryty na początku)
        self.ready_phrases_buttons = []
        self.ready_phrases = ["Zwrot1", "Zwrot2", "Zwrot3", "Zwrot4", "Zwrot5",
                              "Zwrot6", "Zwrot7", "Zwrot8", "Zwrot9", "Zwrot10"]

        self.ready_phrases_layout = QGridLayout()
        row, col = 5, 0
        for i, phrase in enumerate(self.ready_phrases):
            button = QPushButton(phrase)
            button.setFixedSize(120, 30)
            button.clicked.connect(lambda checked, p=phrase: self.text_input.setText(p))
            button.setVisible(False)  # Ukryte na starcie
            self.ready_phrases_buttons.append(button)
            layout.addWidget(button, row, col)
            col += 1
            if col > 4:  # Maksymalnie 5 kolumn
                col = 0
                row += 1

        # Przycisk wysyłania (prawy dolny róg)
        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon.fromTheme("media-playback-start"))  # Ikona strzałki
        self.send_button.setIconSize(QSize(40, 40))
        self.send_button.setFixedSize(60, 60)
        self.send_button.setStyleSheet("background-color: white; border: 2px solid black; border-radius: 10px;")
        self.send_button.clicked.connect(self.send_text)
        layout.addWidget(self.send_button, row + 1, 6, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def toggle_ready_phrases(self):
        """Pokazuje lub ukrywa gotowe zwroty."""
        visible = self.ready_phrases_buttons[0].isVisible()
        for btn in self.ready_phrases_buttons:
            btn.setVisible(not visible)

    def send_text(self):
        """Symulacja wysyłania tekstu."""
        self.send_button.setStyleSheet("background-color: #1976D2; border: 2px solid #1976D2;")
        QTimer.singleShot(1000, self.reset_send_button)

    def reset_send_button(self):
        """Reset przycisku wysyłania po animacji."""
        self.send_button.setStyleSheet("background-color: white; border: 2px solid black; border-radius: 10px;")
