import socket
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QComboBox, QSizePolicy, QSpacerItem, QTextEdit, QHBoxLayout, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon


class TextTab(QWidget):
    def __init__(self):
        super().__init__()

        # Główny layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Layout dla głównego obszaru wpisywania i translacji
        input_translate_layout = QGridLayout()
        input_translate_layout.setSpacing(10)

        # Pole tekstowe do wpisywania
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Wpisz tekst tutaj...")
        self.text_input.setFont(QFont("Times New Roman", 12))
        self.text_input.setFixedHeight(50)
        input_translate_layout.addWidget(self.text_input, 0, 0, 1, 2)

        # Ikona translacji
        self.translation_icon = QLabel()
        self.translation_icon.setFixedSize(50, 50)
        self.translation_icon.setStyleSheet("border: 2px solid black; background-color: #E0E0E0;")
        input_translate_layout.addWidget(self.translation_icon, 0, 2, alignment=Qt.AlignCenter)

        # Lista wyboru języka
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "Polski", "Angielski", "Niemiecki", "Francuski", "Hiszpański", "Ukraiński", "Rosyjski", "Włoski"
        ])
        self.language_combo.setFixedWidth(150)
        self.language_combo.currentTextChanged.connect(self.translate_text)
        input_translate_layout.addWidget(self.language_combo, 0, 3)

        # Pole przetłumaczonego tekstu
        self.translated_text = QTextEdit()
        self.translated_text.setPlaceholderText("Tutaj pojawi się przetłumaczony tekst...")
        self.translated_text.setReadOnly(True)
        self.translated_text.setFixedHeight(50)
        input_translate_layout.addWidget(self.translated_text, 0, 4, 1, 2)

        layout.addLayout(input_translate_layout)

        # Czcionka
        font_layout = QHBoxLayout()
        self.font_label = QLabel("Czcionka:")
        self.font_label.setFont(QFont("Arial", 10, QFont.Bold))
        font_layout.addWidget(self.font_label)

        self.font_combo = QComboBox()
        self.font_combo.addItems([
            "10x20.bdf", "6x12.bdf", "7x14.bdf", "8x13.bdf", "9x18.bdf", "helvR12.bdf"
        ])
        self.font_combo.setFixedWidth(150)
        font_layout.addWidget(self.font_combo)
        font_layout.addStretch()
        layout.addLayout(font_layout)

        # Gotowe Zwroty
        self.ready_phrases_button = QPushButton("Gotowe Zwroty")
        self.ready_phrases_button.clicked.connect(self.toggle_ready_phrases)
        layout.addWidget(self.ready_phrases_button)

        # Przestrzeń na przyciski gotowych zwrotów w pionie
        self.ready_phrases_area = QScrollArea()
        self.ready_phrases_area.setWidgetResizable(True)
        self.ready_phrases_area.setVisible(False)

        self.ready_phrases_widget = QWidget()
        self.ready_phrases_layout = QVBoxLayout()
        self.ready_phrases_widget.setLayout(self.ready_phrases_layout)
        self.ready_phrases_area.setWidget(self.ready_phrases_widget)

        self.ready_phrases = [
            "Zwrot1", "Zwrot2", "Zwrot3", "Zwrot4", "Zwrot5",
            "Zwrot6", "Zwrot7", "Zwrot8", "Zwrot9", "Zwrot10"
        ]
        for phrase in self.ready_phrases:
            button = QPushButton(phrase)
            button.setFixedSize(150, 30)
            button.clicked.connect(lambda checked, p=phrase: self.add_ready_phrase(p))
            self.ready_phrases_layout.addWidget(button)

        layout.addWidget(self.ready_phrases_area)

        self.ready_phrases_output = QLabel("")
        self.ready_phrases_output.setFixedHeight(50)
        self.ready_phrases_output.setStyleSheet("border: 1px solid gray;")
        layout.addWidget(self.ready_phrases_output)

        self.setLayout(layout)

    def translate_text(self):
        """Funkcja symulująca translację."""
        input_text = self.text_input.text()
        selected_language = self.language_combo.currentText()
        if input_text:
            self.translated_text.setText(f"[Tłumaczenie na {selected_language}]: {input_text}")

    def toggle_ready_phrases(self):
        """Pokazuje lub ukrywa gotowe zwroty."""
        visible = self.ready_phrases_area.isVisible()
        self.ready_phrases_area.setVisible(not visible)

    def add_ready_phrase(self, phrase):
        """Dodaje gotowy zwrot do wyjścia."""
        self.ready_phrases_output.setText(f"{phrase}")