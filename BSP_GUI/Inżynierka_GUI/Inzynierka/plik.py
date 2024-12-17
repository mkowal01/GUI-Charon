import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QTabBar, QPushButton, QVBoxLayout,
    QLabel, QWidget, QHBoxLayout, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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
        self.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)

        # Główny layout
        main_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Pasek zakładek i przycisk
        header_layout = QHBoxLayout()
        self.tab_bar = QTabBar()
        self.tab_bar.setFont(QFont("Arial", 12, QFont.Bold))
        self.tab_bar.setFixedHeight(50)
        self.style_tab_bar()

        # Dodanie zakładek do paska
        self.tab_bar.addTab("TEXT")
        self.tab_bar.addTab("AUDIO")
        self.tab_bar.addTab("LOKALIZACJA")
        self.tab_bar.addTab("INSTRUKCJA OBSŁUGI")
        self.tab_bar.addTab("O NAS")
        self.tab_bar.currentChanged.connect(self.change_tab)

        # Dodanie przycisku Połącz
        connect_button = QPushButton("POŁĄCZ")
        connect_button.setFont(QFont("Arial", 18, QFont.Bold))
        connect_button.setFixedSize(150, 50)
        connect_button.setStyleSheet("""
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
        connect_button.clicked.connect(self.open_connect_tab)

        # Dodanie elementów do paska
        header_layout.addWidget(self.tab_bar)
        header_layout.addStretch()
        header_layout.addWidget(connect_button)

        # Dodanie paska do głównego layoutu
        main_layout.addLayout(header_layout)

        # Dodanie pola na zawartość zakładek
        self.content_widget = QStackedWidget()
        self.content_widget.addWidget(TextTab())
        self.content_widget.addWidget(AudioTab())
        self.content_widget.addWidget(LocalizationTab())
        self.content_widget.addWidget(ManualTab())
        self.content_widget.addWidget(AboutTab())
        main_layout.addWidget(self.content_widget)

    def style_tab_bar(self):
        """Stylizacja paska zakładek."""
        font = QFont("Arial", 18, QFont.Bold)
        self.tab_bar.setFont(font)
        self.tab_bar.setStyleSheet("""
            QTabBar::pane {
                border: 6px solid #C0C0C0;
                background: #F0F0F0;
            }
            QTabBar::tab {
                background: #388E3C;
                color: #FFFFFF;
                border: 1px solid #C0C0C0;
                padding: 10px;
                margin-right: 0px;
                font-weight: bold;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QTabBar::tab:selected {
                background: #388E3C;
                color: #FFFFFF;
                border-bottom: 2px solid #0078D7;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
            QTabBar::tab:hover {
                background: #1976D2;
                color: #FFFFFF;
            }
        """)

    def change_tab(self, index):
        """Zmiana zawartości zakładki."""
        self.content_widget.setCurrentIndex(index)

    def open_connect_tab(self):
        """Funkcja otwierająca plik connect_tab."""
        self.connect_window = ConnectTab()
        self.connect_window.show()

    def keyPressEvent(self, event):
        """Zamykanie okna po wciśnięciu ESC."""
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
