import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabBar, QPushButton, QVBoxLayout,
    QLabel, QWidget, QHBoxLayout, QStackedWidget
)
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont, QPixmap

# Import klas z zewnętrznych plików
from text_tab import TextTab
from audio_tab import AudioTab
from localization_tab import LocalizationTab
from manual_tab import ManualTab
from about_tab import AboutTab
from connect_tab import ConnectTab

# Konfiguracja ścieżki dla Qt plugins
plugin_path = os.path.join(
    os.path.abspath(os.path.dirname(sys.executable)), "..", "Lib", "site-packages", "PyQt5", "Qt5", "plugins",
    "platforms"
)
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ustawienia okna
        self.setWindowTitle("LoRa Application - Inżynierka")
        self.setGeometry(100, 100, 1200, 800)

        # Główny widget i layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Pasek zakładek i przycisk (poczatkowo ukryte)
        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout()
        self.header_widget.setLayout(self.header_layout)

        self.tab_bar = QTabBar()
        self.tab_bar.setFont(QFont("Arial", 18, QFont.Bold))
        self.tab_bar.setFixedHeight(50)
        self.style_tab_bar()
        self.tab_bar.addTab("TEXT")
        self.tab_bar.addTab("AUDIO")
        self.tab_bar.addTab("LOKALIZACJA")
        self.tab_bar.addTab("INSTRUKCJA OBSŁUGI")
        self.tab_bar.addTab("O NAS")
        self.tab_bar.currentChanged.connect(self.change_tab)

        self.connect_button = QPushButton("POŁĄCZ")
        self.connect_button.setFont(QFont("Arial", 18, QFont.Bold))
        self.connect_button.setFixedSize(150, 50)
        self.connect_button.setStyleSheet("""
            QPushButton {
                background-color: #388E3C;
                color: white;
                border-radius: 20px;
                border: 2px solid #388E3C;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        self.connect_button.clicked.connect(self.open_connect_tab)

        # Dodanie elementów do paska
        self.header_layout.addWidget(self.tab_bar)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.connect_button)

        # Dodanie widżetu paska na górze aplikacji
        self.main_layout.addWidget(self.header_widget)

        # Zawartość zakładek i strony startowej
        self.content_widget = QStackedWidget()
        self.add_start_page()
        self.content_widget.addWidget(TextTab())  # TEXT
        self.content_widget.addWidget(AudioTab())  # AUDIO
        self.content_widget.addWidget(LocalizationTab())  # LOKALIZACJA
        self.content_widget.addWidget(ManualTab())  # INSTRUKCJA OBSŁUGI
        self.content_widget.addWidget(AboutTab())  # O NAS

        # Dodanie widżetu zawartości poniżej paska
        self.main_layout.addWidget(self.content_widget)

        # Ukrycie elementów zakładek i przycisku poczatkowo
        self.header_widget.hide()

    def add_start_page(self):
        """Strona startowa"""
        start_widget = QWidget()
        layout = QVBoxLayout()

        #Układ poziomy dla logo i tekstu
        horizontal_layout = QHBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("wspolne.jpeg").scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        # Podziękowania
        thanks_label = QLabel("Podziękowania dla promotora oraz dla ChatGPT za wsparcie w projekcie.")
        thanks_label.setFont(QFont("Arial", 16))
        thanks_label.setAlignment(Qt.AlignLeft)
        thanks_label.setWordWrap(True)

        # Dodanie elementów do układu poziomego
        horizontal_layout.addWidget(logo_label)
        horizontal_layout.addWidget(thanks_label)

        # Tekst powitalny
        welcome_label = QLabel("Witamy w aplikacji Inżynierka")
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)

        # Czas
        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 18))
        self.time_label.setAlignment(Qt.AlignCenter)
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

        # Przyciski
        button_layout = QHBoxLayout()
        start_button = QPushButton("Rozpocznij")
        start_button.setFont(QFont("Arial", 14))
        start_button.setFixedSize(150, 50)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #388E3C;
                color: white;
                border-radius: 15px;
                border: 2px solid #388E3C;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        start_button.clicked.connect(self.show_main_ui)

        exit_button = QPushButton("Zamknij")
        exit_button.setFont(QFont("Arial", 14))
        exit_button.setFixedSize(150, 50)
        exit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #388E3C;
                        color: white;
                        border-radius: 15px;
                        border: 2px solid #388E3C;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                    QPushButton:pressed {
                        background-color: #388E3C;
                    }
                """)
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(start_button)
        button_layout.addWidget(exit_button)

        # Układ strony startowej
        layout.addStretch()
        layout.addLayout(horizontal_layout)
        layout.addWidget(welcome_label)
        layout.addWidget(self.time_label)
        layout.addLayout(button_layout)
        layout.addStretch()

        start_widget.setLayout(layout)
        self.content_widget.addWidget(start_widget)  # Dodanie jako pierwszej strony

    def show_main_ui(self):
        """Pokazuje zakładki i przycisk POŁĄCZ."""
        self.header_widget.show()
        self.content_widget.setCurrentIndex(1)  # Przejdź do zakładki TEXT

    def update_time(self):
        """Aktualizacja wyświetlanego czasu."""
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_label.setText(f"Aktualny czas: {current_time}")

    def style_tab_bar(self):
        """Stylizacja paska zakładek."""
        self.tab_bar.setStyleSheet("""
            QTabBar::tab {
                background: #388E3C;
                color: #FFFFFF;
                padding: 10px;
                border: 1px solid #C0C0C0;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QTabBar::tab:hover {
                background: #1976D2;
                color: #FFFFFF;
            }
            QTabBar::tab:selected {
                background: #388E3C;
                color: #FFFFFF;
                border-bottom: 2px solid #0078D7;
            }
        """)

    def change_tab(self, index):
        """Zmiana zawartości zakładki."""
        self.content_widget.setCurrentIndex(index + 1)  # Zakładki zaczynają się od indeksu 1

    def open_connect_tab(self):
        """Otwieranie zakładki Połącz."""
        self.connect_window = ConnectTab()
        self.connect_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
