# start_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont, QPixmap

class StartPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_ui()

    def setup_ui(self):
        """Tworzy interfejs strony startowej."""
        horizontal_layout = QHBoxLayout()

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("logo.png").scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        thanks_label = QLabel()
        thanks_label.setText("""
            <p style="text-align: justify; font-family: Arial; font-size: 16px; font-style: italic; color: white; line-height: 1.6;">
                Wyrażam serdeczne podziękowania dla naszego promotora, <br>
                dr inż. kpt. Krzysztofa Górskiego, za nieocenione wsparcie, <br>
                cierpliwość oraz cenne wskazówki, które umożliwiły nam <br>
                realizację i ukończenie niniejszej pracy inżynierskiej. <br>
                Jego wiedza, doświadczenie oraz zaangażowanie <br>
                były dla nas niezwykle inspirujące i miały kluczowe <br>
                znaczenie dla osiągnięcia wyznaczonych celów projektu.
            </p>
        """)
        thanks_label.setFont(QFont("Arial", 16, QFont.StyleItalic, QFont.Bold))  # Czcionka kursywą
        thanks_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)  # Wyśrodkowanie pionowe, wyrównanie do prawej
        thanks_label.setWordWrap(True)  # Zawijanie tekstu
        thanks_label.setStyleSheet("""
            QLabel {
                color: white;            /* Kolor tekstu */
                padding: 20px;           /* Odstęp wewnętrzny */
                margin: 20px 0;          /* Odstęp od góry i dołu */
                line-height: 1.6;        /* Zwiększenie odstępów między liniami */
                max-width: 800px;        /* Ograniczenie szerokości tekstu */
            }
        """)

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
        start_button.setStyleSheet(self.get_button_stylesheet())
        start_button.clicked.connect(self.start_application)

        exit_button = QPushButton("Zamknij")
        exit_button.setFont(QFont("Arial", 14))
        exit_button.setFixedSize(150, 50)
        exit_button.setStyleSheet(self.get_button_stylesheet())
        exit_button.clicked.connect(self.main_app.close)

        button_layout.addWidget(start_button)
        button_layout.addWidget(exit_button)

        self.layout.addStretch()
        self.layout.addLayout(horizontal_layout)
        self.layout.addWidget(welcome_label)
        self.layout.addWidget(self.time_label)
        self.layout.addLayout(button_layout)
        self.layout.addStretch()

    def start_application(self):
        """Aktywuje główny interfejs aplikacji i otwiera zakładkę 'Instrukcja obsługi'."""
        self.main_app.show_main_ui()
        self.main_app.tab_bar.setCurrentIndex(3)  # Ustawia zakładkę na 'Instrukcja obsługi'

    def update_time(self):
        """Aktualizacja czasu w czasie rzeczywistym."""
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_label.setText(f"Aktualny czas: {current_time}")

    def get_button_stylesheet(self):
        """Zwraca styl przycisków w zależności od trybu aplikacji."""
        is_dark_mode = self.main_app.is_dark_mode
        if is_dark_mode:
            return """
                QPushButton {
                    background-color: #000000; /* Czarny kolor tła */
                    color: #FFFFFF;           /* Biały kolor tekstu */
                    border-radius: 15px;
                    border: 2px solid #6a5f31; /* Niebieski obrys */
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
                    border-radius: 15px;
                    border: 2px solid #6a5f31;
                }
                QPushButton:hover {
                    background-color: #B3E5FC;
                }
                QPushButton:pressed {
                    background-color: #81D4FA;
                }
            """
