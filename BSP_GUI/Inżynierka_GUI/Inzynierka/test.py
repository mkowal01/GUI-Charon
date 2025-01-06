import os
import sys
import socket
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabBar, QPushButton, QVBoxLayout, QLabel, QWidget, QHBoxLayout,
                             QStackedWidget, QLineEdit, QFrame, QComboBox)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty, QTime, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QColor

# Import klas z zewnętrznych plików
from text_tab import TextTab
from audio_tab import AudioTab
from localization_tab import LocalizationTab
from manual_tab import ManualTab
from about_tab import AboutTab
from connect_tab import ConnectTab
from socket_thread import SocketThread

# Konfiguracja ścieżki dla Qt plugins
plugin_path = os.path.join(
    os.path.abspath(os.path.dirname(sys.executable)), "..", "Lib", "site-packages", "PyQt5", "Qt5", "plugins",
    "platforms"
)
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_dragging = False
        self.drag_start_pos = None

        # Usunięcie domyślnej ramki i paska tytułu
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Główne ustawienia okna
        self.setWindowTitle("Inżynierka Kowal&Śliwka")
        self.setGeometry(100, 100, 800, 600)

        # Główne widgety i layout
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("""
            QWidget {
                border-radius: 20px;
                background-color: #008000;
                border: 1px solid transparent;
            }
        """)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Usuń wszystkie marginesy
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # Pasek tytułu
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
            QWidget {
                background-color: #008000;
                border-top-left-radius: 20px; 
                border-top-right-radius: 20px;  
                border-bottom-left-radius: 0px; 
                border-bottom-right-radius: 0px; 
            }
        """)

        # Pasek tytułu: elementy
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 10, 0)
        title_layout.setSpacing(5)

        # Tytuł aplikacji
        self.title_label = QLabel("LoRa Application - Inżynierka")
        self.title_label.setStyleSheet("color: white; font-size: 16px; margin-left: 10px;")
        self.title_label.setAlignment(Qt.AlignVCenter)

        # Przyciski na pasku tytułu
        close_button = QPushButton()
        close_button.setFixedSize(15, 15)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #FF605C; /* Czerwony */
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #FF3B30; /* Ciemniejszy czerwony */
            }
        """)
        close_button.clicked.connect(self.close)

        minimize_button = QPushButton()
        minimize_button.setFixedSize(15, 15)
        minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #FFBD44; /* Pomarańczowy */
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #FF9500; /* Ciemniejszy pomarańczowy */
            }
        """)
        minimize_button.clicked.connect(self.showMinimized)

        maximize_button = QPushButton()
        maximize_button.setFixedSize(15, 15)
        maximize_button.setStyleSheet("""
            QPushButton {
                background-color: #28C840; /* Zielony */
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #34C759; /* Ciemniejszy zielony */
            }
        """)
        maximize_button.clicked.connect(self.toggle_maximize_restore)

        # Dodanie elementów do paska tytułu
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(minimize_button)
        title_layout.addWidget(maximize_button)
        title_layout.addWidget(close_button)

        self.title_bar.setLayout(title_layout)
        self.main_layout.addWidget(self.title_bar)

        # Pasek zakładek i przyciski
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

        # Przyciski na pasku zakładek
        self.video_button = QPushButton("VIDEO")
        self.video_button.setFont(QFont("Arial", 18, QFont.Bold))
        self.video_button.setFixedSize(150, 50)
        self.video_button.setStyleSheet("""
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
        self.video_button.clicked.connect(self.Video)

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

        self.header_layout.addWidget(self.tab_bar)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.video_button)
        self.header_layout.addWidget(self.connect_button)

        self.main_layout.addWidget(self.header_widget)

        # Zawartość aplikacji
        self.content_layout = QHBoxLayout()
        self.main_layout.addLayout(self.content_layout)

        self.content_widget = QStackedWidget()
        self.add_start_page()
        self.content_widget.addWidget(TextTab(self))  # TEXT
        self.content_widget.addWidget(AudioTab(self))  # AUDIO
        self.content_widget.addWidget(LocalizationTab(self))  # LOKALIZACJA
        self.content_widget.addWidget(ManualTab())  # INSTRUKCJA OBSŁUGI
        self.content_widget.addWidget(AboutTab())  # O NAS

        self.content_layout.addWidget(self.content_widget)

        # Animacja tła
        self.colors = [
            QColor("#008000"), QColor("#2e8b57"),
            QColor("#618358"), QColor("#19a56f"), QColor("#006633")
        ]
        self.current_color_index = 0
        self.animation = QPropertyAnimation(self, b"background_color")
        self.animation.setDuration(2000)
        self.animation.finished.connect(self.start_next_animation)
        self.start_next_animation()

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

    def start_next_animation(self):
        start_color = self.colors[self.current_color_index]
        next_index = (self.current_color_index + 1) % len(self.colors)
        end_color = self.colors[next_index]

        self.animation.setStartValue(start_color)
        self.animation.setEndValue(end_color)
        self.animation.start()
        self.current_color_index = next_index

    def get_background_color(self):
        return self.palette().color(self.backgroundRole())

    def set_background_color(self, color):
        r, g, b = color.red(), color.green(), color.blue()
        self.central_widget.setStyleSheet(f"""
            QWidget {{
                border-radius: 20px;
                background-color: rgb({r}, {g}, {b});
                border: 1px solid transparent;
            }}
        """)

    background_color = pyqtProperty(QColor, get_background_color, set_background_color)

    def add_start_page(self):
        """Strona startowa"""
        start_widget = QWidget()
        layout = QVBoxLayout()

        horizontal_layout = QHBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("logo.png").scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        thanks_label = QLabel("Podziękowania dla promotora oraz dla ChatGPT za wsparcie w projekcie.")
        thanks_label.setFont(QFont("Arial", 16))
        thanks_label.setAlignment(Qt.AlignLeft)
        thanks_label.setWordWrap(True)

        horizontal_layout.addWidget(logo_label)
        horizontal_layout.addWidget(thanks_label)

        welcome_label = QLabel("Witamy w aplikacji Inżynierka")
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)

        self.time_label = QLabel()
        self.time_label.setFont(QFont("Arial", 18))
        self.time_label.setAlignment(Qt.AlignCenter)
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.update_time()

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

        layout.addStretch()
        layout.addLayout(horizontal_layout)
        layout.addWidget(welcome_label)
        layout.addWidget(self.time_label)
        layout.addLayout(button_layout)
        layout.addStretch()

        start_widget.setLayout(layout)
        self.content_widget.addWidget(start_widget)

    def show_main_ui(self):
        self.header_widget.show()
        self.content_widget.setCurrentIndex(1)

    def create_title_bar(self):
        """Tworzy tytułowy pasek aplikacji."""
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget {
                background-color: #008000;
                border-top-left-radius: 20px; 
                border-top-right-radius: 20px;  
            }
        """)

        # Pasek tytułu: elementy
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(5)

        # Tytuł aplikacji
        title_label = QLabel("LoRa Application - Inżynierka")
        title_label.setStyleSheet("color: white; font-size: 16px;")
        title_label.setAlignment(Qt.AlignVCenter)

        # Przyciski na pasku tytułu
        close_button = QPushButton()
        close_button.setFixedSize(15, 15)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #FF605C; /* Czerwony */
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #FF3B30; /* Ciemniejszy czerwony */
            }
        """)
        close_button.clicked.connect(self.close)

        minimize_button = QPushButton()
        minimize_button.setFixedSize(15, 15)
        minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #FFBD44; /* Pomarańczowy */
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #FF9500; /* Ciemniejszy pomarańczowy */
            }
        """)
        minimize_button.clicked.connect(self.showMinimized)

        maximize_button = QPushButton()
        maximize_button.setFixedSize(15, 15)
        maximize_button.setStyleSheet("""
            QPushButton {
                background-color: #28C840; /* Zielony */
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #34C759; /* Ciemniejszy zielony */
            }
        """)
        maximize_button.clicked.connect(self.toggle_maximize_restore)

        # Dodanie elementów do paska tytułu
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(minimize_button)
        title_layout.addWidget(maximize_button)
        title_layout.addWidget(close_button)

        title_bar.setLayout(title_layout)
        return title_bar

    def update_time(self):
        """Aktualizacja czasu w czasie rzeczywistym na stronie startowej."""
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
        """Zmiana zakładki w zależności od wybranego indeksu."""
        self.content_widget.setCurrentIndex(index + 1)

    def Video(self):
        # Sprawdź, czy pole jest aktywne (czy przycisk ma tekst "AKTYWNE")
        if self.video_button.text() == "AKTYWNE":
            # Przywróć normalne wymiary okna
            original_width = self.width() - 400  # Zmniejsz szerokość o 400 px
            self.resize(original_width, self.height())

            # Usuń placeholder (czarne pole) z układu
            if hasattr(self, 'right_placeholder'):
                self.content_layout.removeWidget(self.right_placeholder)
                self.right_placeholder.deleteLater()
                del self.right_placeholder

            # Zmień przycisk na stan nieaktywny
            self.video_button.setStyleSheet("""
            QPushButton {
                background-color: #FF605C;
                color: white;
                border-radius: 20px;
                padding: 5px 10px;
                border: 2px solid #388E3C;
            }
            QPushButton:hover {
                background-color: #FF3B30;
            }
            QPushButton:pressed {
                background-color: #FF605C;
            }
        """)
            self.video_button.setText("VIDEO")  # Przywróć oryginalny tekst przycisku
            return

        # Jeśli pole nie jest aktywne, dodaj czarne pole i rozszerz okno
        current_width = self.width()
        current_height = self.content_widget.height()

        # Zwiększ szerokość okna o 400 px
        new_width = current_width + 400
        self.resize(new_width, self.height())

        # Stwórz pusty widget jako przestrzeń
        self.right_placeholder = QWidget()
        self.right_placeholder.setStyleSheet("""
            background-color: #333;  /* Ciemnoszary kolor */
            border: 1px dashed #555;  /* Opcjonalna ramka */
        """)

        # Synchronizuj wysokość czarnego pola z widgetem zawartości
        self.right_placeholder.setFixedSize(380, current_height - 20)  # Odejmij marginesy z wysokości

        # Ustaw marginesy w układzie
        self.content_layout.setContentsMargins(0, 0, 10, 0)  # Marginesy 10px z każdej strony
        self.content_layout.setSpacing(0)  # Odstępy między elementami

        # Dodaj placeholder do układu horyzontalnego
        self.content_layout.addWidget(self.right_placeholder)

        # Zmień kolor i tekst przycisku "VIDEO"
        self.video_button,(QFont("Arial", 18, QFont.Bold))
        self.video_button.setStyleSheet("""
            QPushButton {
                background-color: #FF605C;  /* Czerwony odcień */
                color: white;
                border-radius: 20px;
                padding: 5px 10px;
                border: 2px solid #388E3C;  /* Zielona ramka */
            }
            QPushButton:hover {
                background-color: #FF3B30;  /* Ciemniejszy czerwony */
            }
            QPushButton:pressed {
                background-color: #FF605C;  /* Powrót do podstawowego koloru */
            }
        """)
        self.video_button.setText("AKTYWNE")  # Zmieniamy tekst przycisku

    def open_connect_tab(self):
        """Otwiera dynamiczny formularz konfiguracji połączenia."""
        # Ukrycie paska zakładek zamiast usuwania
        self.tab_bar.hide()
        if hasattr(self, 'video_button'):
            self.video_button.hide()

        # Czyszczenie istniejącego układu dynamicznych elementów
        for i in reversed(range(self.header_layout.count())):
            widget = self.header_layout.itemAt(i).widget()
            if widget and widget not in [self.tab_bar, self.video_button]:  # Nie usuwaj paska zakładek i przycisku VIDEO
                widget.deleteLater()

        # Dodanie listy rozwijanej z opcjami
        self.connection_type_dropdown = QComboBox()
        self.connection_type_dropdown.addItems(["Nieustawiono", "LoRa", "WiFi", "Ethernet", "Socket"])
        self.connection_type_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #388E3C;
                color: white;
                border: 2px solid #388E3C;
                border-radius: 15px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox:hover {
                background-color: #1976D2;
            }
            QComboBox:pressed {
                background-color: #388E3C;
            }
        """)
        self.connection_type_dropdown.currentIndexChanged.connect(self.update_connection_form)
        self.header_layout.addWidget(self.connection_type_dropdown)

        # Dynamiczna sekcja połączeń
        self.connection_form = QWidget()
        self.connection_form_layout = QVBoxLayout()
        self.connection_form.setLayout(self.connection_form_layout)
        self.header_layout.addWidget(self.connection_form)

        # Separator
        self.separator_line = QFrame()
        self.separator_line.setFrameShape(QFrame.VLine)
        self.separator_line.setFrameShadow(QFrame.Sunken)
        self.header_layout.addWidget(self.separator_line)

        # Dodanie sekcji logów
        self.log_area = QLabel("Logi połączenia:")
        self.log_area.setStyleSheet("""
            background-color: #333;
            color: white;
            font-size: 14px;
            padding: 10px;
            border: 1px solid #555;
            border-radius: 5px;
        """)
        self.log_area.setWordWrap(True)
        self.header_layout.addWidget(self.log_area)

        # Inicjalizacja formularza dla domyślnego wyboru ("Nieustawiono")
        self.update_connection_form(0)

    def update_connection_form(self, index):
        """Aktualizacja dynamicznego formularza w zależności od wybranego połączenia."""
        # Czyszczenie dynamicznych widżetów
        while self.connection_form_layout.count():
            item = self.connection_form_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Styl pól tekstowych
        common_style = """
            QLineEdit {
                border: 1px solid #C0C0C0;
                border-radius: 5px;
                padding: 5px;
                background-color: #FFFFFF;
                color: #000000;
            }
            QLineEdit:focus {
                border: 1px solid #1976D2;
            }
        """

        if index == 0:  # Nieustawiono
            self.connection_form_layout.addWidget(QLabel("Wybierz typ połączenia z listy powyżej."))

        elif index == 1:  # LoRa
            self.connection_form_layout.addWidget(QLabel("LoRa Settings"))
            self.connection_form_layout.addWidget(QLabel("COM Port:"))
            self.com_port_field = QLineEdit()
            self.com_port_field.setPlaceholderText("np. COM3")
            self.com_port_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.com_port_field)

            self.connection_form_layout.addWidget(QLabel("Baud Rate:"))
            self.baud_rate_field = QLineEdit()
            self.baud_rate_field.setPlaceholderText("np. 9600")
            self.baud_rate_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.baud_rate_field)

        elif index == 2:  # WiFi
            self.connection_form_layout.addWidget(QLabel("WiFi Settings"))
            self.connection_form_layout.addWidget(QLabel("Adres IP:"))
            self.ip_field = QLineEdit()
            self.ip_field.setPlaceholderText("np. 192.168.0.1")
            self.ip_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.ip_field)

            self.connection_form_layout.addWidget(QLabel("Port:"))
            self.port_field = QLineEdit()
            self.port_field.setPlaceholderText("np. 8080")
            self.port_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.port_field)

        elif index == 3:  # Ethernet
            self.connection_form_layout.addWidget(QLabel("Ethernet Settings"))
            self.connection_form_layout.addWidget(QLabel("Adres IP:"))
            self.ip_field = QLineEdit()
            self.ip_field.setPlaceholderText("np. 192.168.1.1")
            self.ip_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.ip_field)

            self.connection_form_layout.addWidget(QLabel("Port:"))
            self.port_field = QLineEdit()
            self.port_field.setPlaceholderText("np. 80")
            self.port_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.port_field)

        elif index == 4:  # Socket
            self.connection_form_layout.addWidget(QLabel("Socket Settings"))
            self.connection_form_layout.addWidget(QLabel("Adres IP:"))
            self.ip_field = QLineEdit()
            self.ip_field.setPlaceholderText("np. 127.0.0.1")
            self.ip_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.ip_field)

            self.connection_form_layout.addWidget(QLabel("Port:"))
            self.port_field = QLineEdit()
            self.port_field.setPlaceholderText("np. 12345")
            self.port_field.setStyleSheet(common_style)
            self.connection_form_layout.addWidget(self.port_field)

        # Dodanie przycisku "Zatwierdź"
        confirm_button = QPushButton("Zatwierdź")
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #388E3C;
                color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        confirm_button.clicked.connect(self.handle_connection)
        self.connection_form_layout.addWidget(confirm_button)

        self.log_area.setText("[Log] Zaktualizowano formularz dla wybranego połączenia.")

    def handle_connection(self):
        """Obsługa połączenia na podstawie wybranego typu."""
        connection_type = self.connection_type_dropdown.currentText()

        if connection_type == "Socket":
            ip = self.ip_field.text() if self.ip_field.text() else "127.0.0.1"
            port = self.port_field.text() if self.port_field.text() else "12345"

            if not ip or not port:
                self.log_area.setText(self.log_area.text() + "\n[Socket] Adres IP i port muszą być podane!")
                print("[Socket] Brak adresu IP lub portu.")
                return

            if hasattr(self, 'client_socket') and self.client_socket:
                self.log_area.setText(self.log_area.text() + "\n[Socket] Połączenie już istnieje.")
                print("[Socket] Połączenie już istnieje.")
            else:
                try:
                    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client_socket.connect((ip, int(port)))
                    self.log_area.setText(self.log_area.text() + f"\n[Socket] Połączono z {ip}:{port}.")
                    print(f"[Socket] Połączono z {ip}:{port}. Przechodzę do Main UI.")
                    self.finalize_connection()
                except Exception as e:
                    self.log_area.setText(self.log_area.text() + f"\n[Socket] Błąd połączenia: {e}")
                    print(f"[Socket] Błąd połączenia: {e}")
                    self.client_socket = None

        elif connection_type == "WiFi":
            # Podobna logika jak dla "Socket"
            ip = self.ip_field.text()
            port = self.port_field.text()
            if not ip or not port:
                self.log_area.setText(self.log_area.text() + "\n[WiFi] Adres IP lub port muszą być podane!")
                return
            try:
                self.test_socket_connection(ip, port)
                self.log_area.setText(self.log_area.text() + "\n[WiFi] Połączono z serwerem.")
                self.finalize_connection()
            except Exception as e:
                self.log_area.setText(self.log_area.text() + f"\n[WiFi] Błąd: {e}")

        elif connection_type == "LoRa":
            # Logika dla LoRa
            com_port = self.com_port_field.text()
            baud_rate = self.baud_rate_field.text()
            if not com_port or not baud_rate:
                self.log_area.setText(self.log_area.text() + "\n[LoRa] Port COM lub Baud Rate muszą być podane!")
                return
            try:
                self.lora_connection = LoRaConnection(com_port, int(baud_rate))
                self.lora_connection.connect()
                self.log_area.setText(self.log_area.text() + "\n[LoRa] Połączono!")
                self.finalize_connection()
            except Exception as e:
                self.log_area.setText(self.log_area.text() + f"\n[LoRa] Błąd: {e}")

        elif connection_type == "Ethernet":
            # Logika dla Ethernet
            ip = self.ip_field.text()
            port = self.port_field.text()
            if not ip or not port:
                self.log_area.setText(self.log_area.text() + "\n[Ethernet] Adres IP lub port muszą być podane!")
                return
            try:
                self.test_socket_connection(ip, port)
                self.log_area.setText(self.log_area.text() + "\n[Ethernet] Połączono z serwerem.")
                self.finalize_connection()
            except Exception as e:
                self.log_area.setText(self.log_area.text() + f"\n[Ethernet] Błąd: {e}")

        elif connection_type == "Nieustawiono":
            self.log_area.setText(self.log_area.text() + "\n[Nieustawiono] Nie wybrano żadnego typu połączenia.")
            print("[Nieustawiono] Nie wybrano żadnego typu połączenia.")
        else:
            self.log_area.setText(self.log_area.text() + f"\n[Nieznany typ] {connection_type} nieobsługiwany.")
            print(f"[Nieznany typ] {connection_type} nieobsługiwany.")

    def handle_disconnect(self):
        """Obsługa rozłączenia."""
        try:
            if hasattr(self, 'client_socket') and self.client_socket:
                self.client_socket.close()
                self.client_socket = None
                self.log_area.setText(self.log_area.text() + "\n[Socket] Połączenie zostało rozłączone.")
                print("[Socket] Połączenie zostało rozłączone.")

                # Ukrycie przycisku "Rozłącz"
                self.disconnect_button.hide()

                # Przywrócenie dynamicznego formularza
                self.connection_type_dropdown.show()
                self.connection_form.show()
                self.separator_line.show()
                self.log_area.show()

            else:
                self.log_area.setText(self.log_area.text() + "\n[Socket] Nie ma aktywnego połączenia do rozłączenia.")
                print("[Socket] Nie ma aktywnego połączenia do rozłączenia.")
        except Exception as e:
            self.log_area.setText(self.log_area.text() + f"\n[Socket] Błąd podczas rozłączania: {e}")
            print(f"[Socket] Błąd podczas rozłączania: {e}")

    def finalize_connection(self):
        """Obsługuje wspólne operacje po nawiązaniu połączenia."""
        # Ukrycie dynamicznego formularza
        self.connection_type_dropdown.hide()
        self.connection_form.hide()
        self.separator_line.hide()
        self.log_area.hide()

        # Dodanie przycisku „Rozłącz”
        self.disconnect_button = QPushButton("ROZŁĄCZ")
        self.disconnect_button.setFont(QFont("Arial", 18, QFont.Bold))
        self.disconnect_button.setFixedSize(150, 50)  # Dopasowanie wielkości
        self.disconnect_button.setStyleSheet("""
            QPushButton {
                background-color: #FF605C;
                color: white;
                border-radius: 20px;
                padding: 5px 10px;
                border: 2px solid #388E3C;
            }
            QPushButton:hover {
                background-color: #FF3B30;
            }
            QPushButton:pressed {
                background-color: #FF605C;
            }
        """)
        self.disconnect_button.clicked.connect(self.handle_disconnect)
        if hasattr(self, 'video_button') and not self.header_layout.findChild(QPushButton, "VIDEO"):
            self.header_layout.addWidget(self.video_button)
        self.video_button.show()
        self.header_layout.addWidget(self.disconnect_button)

        # Powrót do głównego interfejsu
        self.tab_bar.show()  # Pokaż pasek zakładek
        self.show_main_ui()

    def on_connection_success(self, message):
        """Obsługa sukcesu połączenia."""
        self.log_area.setText(self.log_area.text() + f"\n[Socket] {message}")
        print(f"[Socket] {message}")

    def on_connection_error(self, message):
        """Obsługa błędów połączenia."""
        self.log_area.setText(self.log_area.text() + f"\n[Socket] {message}")
        print(f"[Socket] {message}")

    def on_received_data(self, message):
        """Obsługa danych odebranych z serwera."""
        self.log_area.setText(self.log_area.text() + f"\n[Socket] Odebrano: {message}")
        print(f"[Socket] Odebrano: {message}")

    def close_connection(self):
        """Zamykanie istniejącego połączenia."""
        if hasattr(self, 'client_socket') and self.client_socket:
            try:
                self.client_socket.close()
                self.log_area.setText(self.log_area.text() + "\n[Socket] Połączenie zamknięte.")
                self.client_socket = None
            except Exception as e:
                self.log_area.setText(self.log_area.text() + f"\n[Socket] Błąd podczas zamykania połączenia: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
