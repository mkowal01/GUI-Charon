from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Główny layout poziomy dzielący stronę na dwie części
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)

        # Sekcja Macieja Kowala
        left_frame = QFrame()
        left_layout = QVBoxLayout()

        # Dodanie zdjęcia
        photo_label = QLabel()
        photo_pixmap = QPixmap("ZDJĘCIE.PNG").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        photo_label.setPixmap(photo_pixmap)
        photo_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(photo_label)

        # Dodanie opisu Macieja Kowala
        maciej_description = QLabel(
            """<b><span style='font-size:18px;'>Maciej Kowal</span></b> – był studentem Akademii Wojsk Lądowych im. generała Tadeusza Kościuszki we Wrocławiu 
            na kierunku informatyka, specjalność bezpieczeństwo w cyberprzestrzeni. Aktywnie działał w Naukowym Kole Łączności 
            i Elektroniki. Pasjonuje się programowaniem, nowymi technologiami oraz innowacyjnymi rozwiązaniami informatycznymi.<br><br>
            <b>Jest współautorem następujących publikacji:</b><br>
            - „Wykorzystanie bezzałogowych systemów powietrznych do zdalnego przekazywania wiadomości tekstowych i głosowych”
              opublikowanego w czasopiśmie Elektronika – konstrukcje, technologie, zastosowania oraz prezentowanego podczas XXIII
              Krajowej Konferencji Elektroników.<br>
            - „Koncepcja systemu kontroli, sterowania i zarządzania BSP wykorzystującego technologię wirtualnej i rozszerzonej
              rzeczywistości” opublikowanego w czasopiśmie Przegląd Elektrotechniczny oraz prezentowanego podczas XXIII Krajowej
              Konferencji Elektroników.<br><br>
            <b>Osiągnięcia:</b><br>
            - Pierwsze miejsce w Konkursie o Nagrodę Ministra Obrony Narodowej w kategorii „Wsparcie” za projekt Bezzałogowego
              Systemu Powietrznego „CHARON”, służącego do nagłaśniania i wyświetlania komunikatów.<br>
            - Wyróżnienie w Konkursie o Nagrodę Ministra Obrony Narodowej w kategorii „Wsparcie” za projekt Bezzałogowego Systemu
              Powietrznego „EURYT”, służącego do transportu.<br>
            - Pierwsze miejsce w Konkursie o Nagrodę Ministra Obrony Narodowej w kategorii „Wsparcie” za projekt Bezzałogowego
              Systemu Powietrznego „AETHER”, stworzony system zdalnej detekcji skażeń chemicznych i radiologicznych.
            """
        )
        maciej_description.setWordWrap(True)
        maciej_description.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        maciej_description.setStyleSheet("font-size: 14px;")
        left_layout.addWidget(maciej_description)

        left_frame.setLayout(left_layout)

        # Sekcja Jakuba Wiśniewskiego
        right_frame = QFrame()
        right_layout = QVBoxLayout()

        # Dodanie zdjęcia
        photo_label_jakub = QLabel()
        photo_pixmap_jakub = QPixmap("ZDJĘCIE1.PNG").scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        photo_label_jakub.setPixmap(photo_pixmap_jakub)
        photo_label_jakub.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(photo_label_jakub)

        # Dodanie opisu Jakuba Wiśniewskiego
        jakub_description = QLabel(
            """<b><span style='font-size:18px;'>Jakub Wiśniewski</span></b> – był studentem Akademii Wojsk Lądowych im. generała Tadeusza Kościuszki we Wrocławiu 
            na kierunku informatyka, specjalność bezpieczeństwo w cyberprzestrzeni. Aktywnie działał w Naukowym Kole Łączności 
            i Elektroniki. Pasjonuje się programowaniem, nowymi technologiami oraz innowacyjnymi rozwiązaniami informatycznymi.<br><br>
            <b>Osiągnięcia:</b><br>
            - Uzyskanie 1 miejsca w konkursie ministerstwa obrony narodowej pt. Konkurs o nagrodę Ministra Obrony Narodowej za realizację projektu Bezzałogowego Systemu Powietrznego, Bezzałogowego Systemu Lądowego lub Bezzałogowego Systemu Morskiego do zastosowań związanych z obronnością i bezpieczeństwem państwa.<br>
            - Uzyskanie 2 miejsca w konkursie ministerstwa obrony narodowej pt. Konkurs o nagrodę Ministra Obrony Narodowej za realizację projektu Bezzałogowego Systemu Powietrznego, Bezzałogowego Systemu Lądowego lub Bezzałogowego Systemu Morskiego do zastosowań związanych z obronnością i bezpieczeństwem państwa.<br>
            - Uzyskanie wyróżnienia w konkursie ministerstwa obrony narodowej pt. Konkurs o nagrodę Ministra Obrony Narodowej za realizację projektu Bezzałogowego Systemu Powietrznego, Bezzałogowego Systemu Lądowego lub Bezzałogowego Systemu Morskiego do zastosowań związanych z obronnością i bezpieczeństwem państwa.<br>
            - Artykuł w czasopiśmie: „Elektronika - konstrukcje, technologie, zastosowania”, a tytuł artykułu: „Wykorzystanie bezzałogowych systemów powietrznych do zdalnego przekazywania wiadomości tekstowych i głosowych”.
            """
        )
        jakub_description.setWordWrap(True)
        jakub_description.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        jakub_description.setStyleSheet("font-size: 14px;")
        right_layout.addWidget(jakub_description)

        right_frame.setLayout(right_layout)

        # Dodanie sekcji do głównego layoutu
        main_layout.addWidget(left_frame)
        main_layout.addWidget(right_frame)

        self.setLayout(main_layout)
