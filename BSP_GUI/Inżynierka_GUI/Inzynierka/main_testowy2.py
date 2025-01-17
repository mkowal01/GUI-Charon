import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QHBoxLayout,
                             QTabBar, QStackedWidget, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from start_page import StartPage
from text_tab import TextTab
from audio_tab import AudioTab
from localization_tab import LocalizationTab
from manual_tab import ManualTab
from about_tab import AboutTab
from connect_tab import ConnectTab
from Debuger import debug_print

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        debug_print("main_testowy2",f"MAIN_UI")
        # Ustawienia głównego okna
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("Inżynierka")
        self.setGeometry(100, 100, 1200, 600)
        self.last_tab_index = 0

        self.is_dark_mode = True  # Początkowy tryb ciemny

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.main_layout)

        # Pasek tytułu
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(10, 0, 10, 0)
        self.title_bar_layout.setSpacing(5)

        self.title_label = QLabel("Inżynierka")
        self.title_label.setAlignment(Qt.AlignVCenter)
        self.title_bar_layout.addWidget(self.title_label)
        self.title_bar_layout.addStretch()

        close_button = QPushButton()
        close_button.setFixedSize(15, 15)
        close_button.setStyleSheet(self.get_control_button_stylesheet("#FF605C", "#FF3B30"))
        close_button.clicked.connect(self.close)

        minimize_button = QPushButton()
        minimize_button.setFixedSize(15, 15)
        minimize_button.setStyleSheet(self.get_control_button_stylesheet("#FFBD44", "#FF9500"))
        minimize_button.clicked.connect(self.showMinimized)

        maximize_button = QPushButton()
        maximize_button.setFixedSize(15, 15)
        maximize_button.setStyleSheet(self.get_control_button_stylesheet("#28C840", "#34C759"))
        maximize_button.clicked.connect(self.toggle_maximize_restore)

        self.title_bar_layout.addWidget(minimize_button)
        self.title_bar_layout.addWidget(maximize_button)
        self.title_bar_layout.addWidget(close_button)
        self.title_bar.setLayout(self.title_bar_layout)
        self.main_layout.addWidget(self.title_bar)

        # Pasek zakładek i przyciski
        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout()
        self.header_widget.setLayout(self.header_layout)

        self.tab_bar = QTabBar()
        self.tab_bar.setFont(QFont("Arial", 16))
        self.tab_bar.setFixedHeight(50)
        self.tab_bar.setMaximumWidth(1000)
        self.tab_bar.setStyleSheet(self.get_tab_bar_stylesheet())
        self.tab_bar.addTab("TEXT")
        self.tab_bar.addTab("AUDIO")
        self.tab_bar.addTab("LOKALIZACJA")
        self.tab_bar.addTab("INSTRUKCJA")
        self.tab_bar.addTab("O NAS")
        self.tab_bar.currentChanged.connect(self.change_tab)
        self.tab_bar.setVisible(False)

        self.header_layout.setContentsMargins(5, 0, 0, 0)  # Dodanie marginesu 5 po lewej stronie
        self.header_layout.addWidget(self.tab_bar, alignment=Qt.AlignLeft)

        self.video_button = QPushButton("VIDEO")
        self.video_button.setFont(QFont("Arial", 14))
        self.video_button.setFixedSize(150, 50)
        self.video_button.setStyleSheet(self.get_button_stylesheet())
        self.video_button.setVisible(False)
        self.header_layout.addWidget(self.video_button)

        self.connect_button = QPushButton("POŁĄCZ")
        self.connect_button.setFont(QFont("Arial", 14))
        self.connect_button.setFixedSize(150, 50)
        self.connect_button.setStyleSheet(self.get_button_stylesheet())
        self.connect_button.setVisible(False)
        self.connect_button.clicked.connect(self.open_connect_tab)
        self.header_layout.addWidget(self.connect_button)

        self.main_layout.addWidget(self.header_widget)

        # Zawartość
        self.content_widget = QStackedWidget()
        self.start_page = StartPage(self)
        self.content_widget.addWidget(self.start_page)
        self.content_widget.addWidget(TextTab(self))
        self.content_widget.addWidget(AudioTab(self))
        self.content_widget.addWidget(LocalizationTab(self))
        self.content_widget.addWidget(ManualTab())
        self.content_widget.addWidget(AboutTab())
        self.connect_tab = ConnectTab(self)
        self.content_widget.addWidget(self.connect_tab)
        self.main_layout.addWidget(self.content_widget)

        # Ustawienia stylu aplikacji
        self.set_stylesheet()

    def set_stylesheet(self):
        if self.is_dark_mode:
            self.central_widget.setStyleSheet("""
                QWidget {
                    background-color: #121212;
                    color: white;
                    border-radius: 20px;
                }
            """)
            self.title_bar.setStyleSheet("""
                QWidget {
                    background-color: #6a5f31;
                    border-top-left-radius: 20px;
                    border-top-right-radius: 20px;
                }
            """)
        else:
            self.central_widget.setStyleSheet("""
                QWidget {
                    background-color: #FFFFFF;
                    color: black;
                    border-radius: 20px;
                }
            """)
            self.title_bar.setStyleSheet("""
                QWidget {
                    background-color: #F0F0F0;
                    border-top-left-radius: 20px;
                    border-top-right-radius: 20px;
                }
            """)
        self.tab_bar.setStyleSheet(self.get_tab_bar_stylesheet())
        self.video_button.setStyleSheet(self.get_button_stylesheet())
        self.connect_button.setStyleSheet(self.get_button_stylesheet())

    def get_tab_bar_stylesheet(self):
        if self.is_dark_mode:
            return """
                QTabBar::tab {
                    background: #000000; /* Czarny kolor tła */
                    color: #FFFFFF;      /* Biały kolor tekstu */
                    width: 150;         /* Automatyczna szerokość */
                    padding: 8px 0px;  /* Wyrównane wypełnienie */
                    margin: 0px;        /* Brak odstępów między zakładkami */
                    border: 2px solid #6a5f31; /* Niebieski obrys */
                    border-radius: 10px;  /* Zaokrąglone rogi */
                }
                QTabBar::tab:selected {
                    background: #1E1E1E;  /* Aktywny kolor */
                    border: 3px solid #6a5f34; /* Grubszy niebieski obrys */
                }
                QTabBar::tab:hover {
                    background: #2E2E2E;  /* Kolor przy najechaniu */
                }
            """
        else:
            return """
                QTabBar::tab {
                    background: #E0F7FA;
                    color: black;
                    width: 150;         /* Automatyczna szerokość */
                    padding: 8px 0px;  /* Wyrównane wypełnienie */
                    margin: 0px;        /* Brak odstępów między zakładkami */
                    border: 1px solid #A0A0A0;
                    border-radius: 10px;
                }
                QTabBar::tab:selected {
                    background: #B3E5FC;
                    border: 2px solid #4682B4;
                }
                QTabBar::tab:hover {
                    background: #81D4FA;
                }
            """

    def get_button_stylesheet(self):
        if self.is_dark_mode:
            return """
                QPushButton {
                    background-color: #000000; /* Czarny kolor tła */
                    color: #FFFFFF;           /* Biały kolor tekstu */
                    border-radius: 10px;
                    margin: 0px 5px;
                    border: 2px solid #6a5f31; /* Niebieski obrys */
                    padding: 5px 15px;       /* Wyrównanie wypełnienia */
                }
                QPushButton:hover {
                    background-color: #6a5f34; /* Niebieski kolor przy najechaniu */
                }
                QPushButton:pressed {
                    background-color: #000000; /* Czarny kolor po kliknięciu */
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #E0F7FA;
                    color: black;
                    border-radius: 10px;
                    margin: 0px 5px;
                    border: 2px solid #81D4FA;
                    padding: 5px 15px;       /* Wyrównanie wypełnienia */
                }
                QPushButton:hover {
                    background-color: #B3E5FC;
                }
                QPushButton:pressed {
                    background-color: #81D4FA;
                }
            """

    def get_control_button_stylesheet(self, default_color, hover_color):
        return f"""
            QPushButton {{
                background-color: {default_color};
                border-radius: 7px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    def show_main_ui(self):
        self.tab_bar.setVisible(True)
        self.video_button.setVisible(True)
        self.connect_button.setVisible(True)
        self.content_widget.setCurrentIndex(self.last_tab_index + 1)

    def open_connect_tab(self):
        debug_print("main_testowy2",f"Przejście do ConnectTab")
        self.content_widget.setCurrentWidget(self.connect_tab)

    def change_tab(self, index):
        debug_print("main_testowy2",f"Zmiana zakładki na indeks: {index}")
        self.last_tab_index = index
        self.content_widget.setCurrentIndex(index + 1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.is_dark_mode = not self.is_dark_mode
            self.set_stylesheet()

    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        """Obsługa kliknięcia lewego przycisku myszy na pasku tytułu."""
        if event.button() == Qt.LeftButton and self.title_bar.underMouse():
            self.is_dragging = True
            self.drag_start_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Obsługa przesuwania okna."""
        if self.is_dragging:
            self.move(event.globalPos() - self.drag_start_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Obsługa zwolnienia lewego przycisku myszy."""
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            event.accept()

    def update_connect_button(self, text):
        self.connect_button.setText(text)
        debug_print("main_testowy2",f"Przycisk 'Połącz' zmieniony na: {text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
