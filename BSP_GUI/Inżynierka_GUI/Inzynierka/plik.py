# import os
# import sys
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabBar, QVBoxLayout, QLabel, QWidget, QHBoxLayout,
#                              QStackedWidget, QPushButton)
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QFont
#
# from start_page import StartPage
# from text_tab import TextTab
# from audio_tab import AudioTab
# from localization_tab import LocalizationTab
# from manual_tab import ManualTab
# from about_tab import AboutTab
# from connect_tab import ConnectTab
#
# class MainApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # Okno główne
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setWindowTitle("Inżynierka")
#         self.setGeometry(100, 100, 1200, 600)
#
#         self.is_dark_mode = True  # Początkowy tryb ciemny
#
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#
#         self.main_layout = QVBoxLayout()
#         self.main_layout.setContentsMargins(0, 0, 0, 0)
#         self.central_widget.setLayout(self.main_layout)
#
#         # Pasek tytułu
#         self.title_bar = QWidget()
#         self.title_bar.setFixedHeight(40)
#         self.title_bar_layout = QHBoxLayout()
#         self.title_bar_layout.setContentsMargins(10, 0, 10, 0)
#         self.title_bar_layout.setSpacing(5)
#
#         # Tytuł aplikacji
#         self.title_label = QLabel("Inżynierka")
#         self.title_label.setAlignment(Qt.AlignVCenter)
#         self.title_bar_layout.addWidget(self.title_label)
#         self.title_bar_layout.addStretch()
#
#         # Przyciski na pasku tytułu
#         close_button = QPushButton()
#         close_button.setFixedSize(15, 15)
#         close_button.setStyleSheet(self.get_control_button_stylesheet("#FF605C", "#FF3B30"))
#         close_button.clicked.connect(self.close)
#
#         minimize_button = QPushButton()
#         minimize_button.setFixedSize(15, 15)
#         minimize_button.setStyleSheet(self.get_control_button_stylesheet("#FFBD44", "#FF9500"))
#         minimize_button.clicked.connect(self.showMinimized)
#
#         maximize_button = QPushButton()
#         maximize_button.setFixedSize(15, 15)
#         maximize_button.setStyleSheet(self.get_control_button_stylesheet("#28C840", "#34C759"))
#         maximize_button.clicked.connect(self.toggle_maximize_restore)
#
#         self.title_bar_layout.addWidget(minimize_button)
#         self.title_bar_layout.addWidget(maximize_button)
#         self.title_bar_layout.addWidget(close_button)
#         self.title_bar.setLayout(self.title_bar_layout)
#         self.main_layout.addWidget(self.title_bar)
#
#         # Pasek zakładek i przyciski
#         self.header_widget = QWidget()
#         self.header_layout = QHBoxLayout()
#         self.header_widget.setLayout(self.header_layout)
#
#         self.tab_bar = QTabBar()
#         self.tab_bar.setFont(QFont("Arial", 16))
#         self.tab_bar.setFixedHeight(50)
#         self.tab_bar.setStyleSheet(self.get_tab_bar_stylesheet())
#         self.tab_bar.addTab("TEXT")
#         self.tab_bar.addTab("AUDIO")
#         self.tab_bar.addTab("LOKALIZACJA")
#         self.tab_bar.addTab("INSTRUKCJA OBSŁUGI")
#         self.tab_bar.addTab("O NAS")
#         self.tab_bar.currentChanged.connect(self.change_tab)
#         self.tab_bar.setVisible(False)  # Ukrycie zakładek na starcie
#         self.header_layout.addWidget(self.tab_bar)
#
#         self.video_button = QPushButton("VIDEO")
#         self.video_button.setFont(QFont("Arial", 14))
#         self.video_button.setFixedSize(150, 50)
#         self.video_button.setStyleSheet(self.get_button_stylesheet())
#         self.video_button.setVisible(False)
#         self.header_layout.addWidget(self.video_button)
#
#         self.connect_button = QPushButton("POŁĄCZ")
#         self.connect_button.setFont(QFont("Arial", 14))
#         self.connect_button.setFixedSize(150, 50)
#         self.connect_button.setStyleSheet(self.get_button_stylesheet())
#         self.connect_button.setVisible(False)
#         self.connect_button.clicked.connect(self.open_connect_tab)
#         self.header_layout.addWidget(self.connect_button)
#
#         self.main_layout.addWidget(self.header_widget)
#
#         # Zawartość
#         self.content_widget = QStackedWidget()
#         self.start_page = StartPage(self)
#         self.content_widget.addWidget(self.start_page)  # Strona startowa
#         self.content_widget.addWidget(TextTab(self))  # TEXT
#         self.content_widget.addWidget(AudioTab(self))  # AUDIO
#         self.content_widget.addWidget(LocalizationTab(self))  # LOKALIZACJA
#         self.content_widget.addWidget(ManualTab())  # INSTRUKCJA OBSŁUGI
#         self.content_widget.addWidget(AboutTab())  # O NAS
#         self.connect_tab = ConnectTab(self)  # Dodano zakładkę ConnectTab
#         self.content_widget.addWidget(self.connect_tab)  # Zakładka do obsługi "POŁĄCZ"
#         self.main_layout.addWidget(self.content_widget)
#
#         # Ustaw styl aplikacji
#         self.set_stylesheet()
#
#     def set_stylesheet(self):
#         """Ustawia styl aplikacji w zależności od trybu."""
#         if self.is_dark_mode:
#             self.central_widget.setStyleSheet("""
#                 QWidget {
#                     background-color: #121212;
#                     color: white;
#                     border-radius: 20px;
#                 }
#             """)
#             self.title_bar.setStyleSheet("""
#                 QWidget {
#                     background-color: #1976D2;
#                     border-top-left-radius: 20px;
#                     border-top-right-radius: 20px;
#                 }
#             """)
#         else:
#             self.central_widget.setStyleSheet("""
#                 QWidget {
#                     background-color: #FFFFFF;
#                     color: black;
#                     border-radius: 20px;
#                 }
#             """)
#             self.title_bar.setStyleSheet("""
#                 QWidget {
#                     background-color: #F0F0F0;
#                     border-top-left-radius: 20px;
#                     border-top-right-radius: 20px;
#                 }
#             """)
#         self.tab_bar.setStyleSheet(self.get_tab_bar_stylesheet())
#         self.video_button.setStyleSheet(self.get_button_stylesheet())
#         self.connect_button.setStyleSheet(self.get_button_stylesheet())
#
#     def get_tab_bar_stylesheet(self):
#         """Zwraca styl zakładek w zależności od trybu."""
#         if self.is_dark_mode:
#             return """
#                 QTabBar::tab {
#                     background: #2E8B57;
#                     color: white;
#                     padding: 10px 20px;
#                     margin: 2px;
#                     border: 1px solid #C0C0C0;
#                     border-radius: 10px;
#                 }
#                 QTabBar::tab:selected {
#                     background: #1976D2;
#                     border: 2px solid #005cbf;
#                 }
#                 QTabBar::tab:hover {
#                     background: #228B22;
#                 }
#             """
#         else:
#             return """
#                 QTabBar::tab {
#                     background: #E0F7FA;
#                     color: black;
#                     padding: 10px 20px;
#                     margin: 2px;
#                     border: 1px solid #A0A0A0;
#                     border-radius: 10px;
#                 }
#                 QTabBar::tab:selected {
#                     background: #B3E5FC;
#                     border: 2px solid #4682B4;
#                 }
#                 QTabBar::tab:hover {
#                     background: #81D4FA;
#                 }
#             """
#
#     def get_button_stylesheet(self):
#         """Zwraca styl przycisków w zależności od trybu."""
#         if self.is_dark_mode:
#             return """
#                 QPushButton {
#                     background-color: #388E3C;
#                     color: white;
#                     border-radius: 20px;
#                     border: 2px solid #388E3C;
#                 }
#                 QPushButton:hover {
#                     background-color: #1976D2;
#                 }
#                 QPushButton:pressed {
#                     background-color: #388E3C;
#                 }
#             """
#         else:
#             return """
#                 QPushButton {
#                     background-color: #E0F7FA;
#                     color: black;
#                     border-radius: 20px;
#                     border: 2px solid #81D4FA;
#                 }
#                 QPushButton:hover {
#                     background-color: #B3E5FC;
#                 }
#                 QPushButton:pressed {
#                     background-color: #81D4FA;
#                 }
#             """
#
#     def get_control_button_stylesheet(self, default_color, hover_color):
#         """Zwraca styl przycisków kontrolnych (zamknięcie, minimalizacja, maksymalizacja)."""
#         return f"""
#             QPushButton {{
#                 background-color: {default_color};
#                 border-radius: 7px;
#             }}
#             QPushButton:hover {{
#                 background-color: {hover_color};
#             }}
#         """
#
#     def show_main_ui(self):
#         """Pokazuje główny interfejs aplikacji."""
#         self.tab_bar.setVisible(True)
#         self.video_button.setVisible(True)
#         self.connect_button.setVisible(True)
#         self.content_widget.setCurrentIndex(4)
#
#     def open_connect_tab(self):
#         """Przejście do zakładki ConnectTab."""
#         print("[DEBUG] Próba przejścia do ConnectTab")
#         self.tab_bar.setVisible(False)  # Ukrycie zakładek
#         self.video_button.setVisible(False)  # Ukrycie przycisku VIDEO
#         self.connect_button.setVisible(False)  # Ukrycie przycisku POŁĄCZ
#         print("[DEBUG] Ukryto zakładki i przyciski")
#         self.content_widget.setCurrentWidget(self.connect_tab)
#         print("[DEBUG] Przejście do ConnectTab zakończone")
#
#     def change_tab(self, index):
#         print(f"[DEBUG] Zmiana zakładki na indeks: {index}")
#         self.content_widget.setCurrentIndex(index + 1)
#         print("[DEBUG] Zakładka zmieniona")
#
#     def keyPressEvent(self, event):
#         """Obsługa klawisza ESC do przełączania trybu ciemnego/jasnego."""
#         if event.key() == Qt.Key_Escape:
#             self.is_dark_mode = not self.is_dark_mode
#             self.set_stylesheet()
#
#     def toggle_maximize_restore(self):
#         if self.isMaximized():
#             self.showNormal()
#         else:
#             self.showMaximized()
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = MainApp()
#     main_window.show()
#     sys.exit(app.exec_())
#
# # class AudioTab(QWidget):
# #     def __init__(self, parent=None):
# #         super().__init__(parent)
# #         self.parent_window = parent
# #         debug_print("audio_tab", f"Inicjalizacja AudioTab")
# #
# #         # Inicjalizacja obiektu Translate
# #         self.translator = Translate()
# #
# #         # Główny layout siatki
# #         self.grid_layout = QGridLayout()
# #         self.grid_layout.setSpacing(10)
# #         self.grid_layout.setContentsMargins(10, 10, 10, 10)
# #
# #         # Pole do wpisywania tekstu (0,0) do (1,1)
# #         self.text_input = QTextEdit()
# #         self.text_input.setFont(QFont("Arial", 16))
# #         self.text_input.setPlaceholderText("Pole do wpisania tekstu")
# #         self.text_input.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 10px;")
# #         self.text_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
# #         self.grid_layout.addWidget(self.text_input, 0, 0, 2, 4)
# #
# #         # Pole do wyświetlania tłumaczenia (2,0) do (3,1)
# #         self.translation_display = QTextEdit()
# #         self.translation_display.setFont(QFont("Arial", 16))
# #         self.translation_display.setReadOnly(True)
# #         self.translation_display.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 10px;")
# #         self.translation_display.setPlaceholderText("Tutaj pojawi się tłumaczenie...")
# #         self.translation_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
# #         self.grid_layout.addWidget(self.translation_display, 2, 0, 2, 4)
# #
# #         # Nagrywanie, odtwarzanie i kasowanie nagrań (4,0) do (4,5)
# #         # Ikony
# #         self.record_icon = QIcon("microphone.png")
# #         self.recorded_audio_icon = QIcon("recording_audio.png")
# #         self.play_icon = QIcon("play.png")
# #         self.stop_icon = QIcon("pause.png")
# #         self.delete_icon = QIcon("trash.png")
# #
# #         # Przycisk nagrywania (4,0)
# #         self.record_button = QPushButton()
# #         self.record_button.setIcon(self.record_icon)
# #         # self.record_button.setFixedSize(50, 50)
# #         self.record_button.clicked.connect(self.toggle_recording)
# #         self.record_button.setStyleSheet(
# #             "    background-color: #FF4D4D; color: #FFFFFF; padding: 10px; border-radius: 10px;"
# #             "    height: 100px;"
# #             "    border: 1px solid black;"
# #         )
# #         self.grid_layout.addWidget(self.record_button, 4, 0, 1, 1)
# #
# #         # Label statusu nagrywania
# #         self.recording_status_label = QLabel("Brak audio")  # Domyślny napis
# #         self.recording_status_label.setFont(QFont("Arial", 14))
# #         self.recording_status_label.setAlignment(Qt.AlignCenter)
# #         self.recording_status_label.setStyleSheet(
# #             "    background-color: #2196F3; color: #FFFFFF; padding: 10px; border-radius: 10px;"
# #             "    height: 100px;"
# #             "    border: 1px solid black;"
# #         )
# #         self.grid_layout.addWidget(self.recording_status_label, 4, 1, 1, 1)
# #
# #         # Etykieta czasu nagrania
# #         self.time_label = QLabel("00:00")  # Domyślny czas
# #         self.time_label.setFont(QFont("Arial", 14))
# #         self.time_label.setAlignment(Qt.AlignCenter)
# #         self.time_label.setStyleSheet(
# #             "    background-color: #B0BEC5; color: #000000; padding: 10px; border-radius: 10px;"
# #             "    height: 100px;"
# #             "    border: 1px solid black;"
# #         )
# #         self.grid_layout.addWidget(self.time_label, 4, 2, 1, 1)
# #
# #         # Przycisk odtwarzania (4,3)
# #         self.play_button = QPushButton()
# #         self.play_button.setIcon(self.play_icon)
# #         # self.play_button.setFixedSize(50, 50)
# #         self.play_button.clicked.connect(self.toggle_playback)
# #         self.play_button.setEnabled(False)
# #         self.play_button.setStyleSheet(
# #             "    background-color: #4CAF50; color: #FFFFFF; padding: 10px; border-radius: 10px;"
# #             "    height: 100px;"
# #             "    border: 1px solid black;"
# #         )
# #         self.grid_layout.addWidget(self.play_button, 4, 3, 1, 1)
# #
# #         # Przycisk zatrzymywania odtwarzania (4,4)
# #         self.stop_button = QPushButton()
# #         self.stop_button.setIcon(self.stop_icon)
# #         # self.stop_button.setFixedSize(50, 50)
# #         self.stop_button.clicked.connect(self.stop_playback)
# #         self.stop_button.setEnabled(False)
# #         self.stop_button.setStyleSheet(
# #             "    background-color: #FF4D4D; color: #FFFFFF; padding: 10px; border-radius: 10px;"
# #             "    height: 100px;"
# #             "    border: 1px solid black;"
# #         )
# #         self.grid_layout.addWidget(self.stop_button, 4, 4, 1, 1)
# #
# #         # Przycisk kasowania (4,5)
# #         self.delete_button = QPushButton()
# #         self.delete_button.setIcon(self.delete_icon)
# #         # self.delete_button.setFixedSize(50, 50)
# #         self.delete_button.clicked.connect(self.delete_audio)
# #         self.delete_button.setEnabled(False)
# #         self.delete_button.setStyleSheet(
# #             "    background-color: #FF9800; color: #FFFFFF; padding: 10px; border-radius: 10px;"
# #             "    height: 100px;"
# #             "    border: 1px solid black;"
# #         )
# #         self.grid_layout.addWidget(self.delete_button, 4, 5, 1, 1)
# #
# #         # Zmienna audio
# #         self.recording = False
# #         self.frames = []
# #         self.stream = None
# #         self.audio_interface = pyaudio.PyAudio()
# #         self.output_file = "recording.wav"
# #         self.timer = QTimer()
# #         self.timer.timeout.connect(self.update_time)
# #         self.current_time = 0
# #         self.playback_thread = None
# #         self.playback_position = 0  # Pozycja w ramkach
# #
# #         self.setLayout(self.grid_layout)
# #
# #         # Wybór języka (0,2)
# #         self.language_selector = QComboBox()
# #         self.language_selector.setFont(QFont("Arial", 12))
# #         self.language_selector.addItems([
# #             "Polski", "Angielski", "Niemiecki", "Francuski", "Hiszpański",
# #             "Ukraiński", "Rosyjski", "Włoski", "Szwedzki", "Norweski"
# #         ])
# #         self.language_selector.setCurrentIndex(0)  # Ustawienie domyślnej wartości na "Polski"
# #         self.language_selector.setStyleSheet(
# #             "QComboBox {"
# #             "    background-color: white;"
# #             "    border: 1px solid black;"
# #             "    border-radius: 15px;"
# #             "    padding: 5px;"
# #             "    text-align: center;"
# #             "}"
# #             "QComboBox::drop-down {"
# #             "    border: none;"
# #             "    width: 0px;"  # Ukrycie strzałki
# #             "}"
# #             "QComboBox QAbstractItemView {"
# #             "    border: 1px solid black;"
# #             "    border-radius: 15px;"
# #             "    background-color: #1976D2;"  # Kolor tła
# #             "    color: white;"
# #             "    selection-background-color: #0D47A1;"
# #             "    selection-color: white;"
# #             "    outline: none;"  # Usunięcie linii przerywanej
# #             "    padding: 0px;"  # Usunięcie białych końców
# #             "    margin: 0px;"  # Usunięcie marginesów
# #             "}"
# #             "QScrollBar:vertical {"
# #             "    border: none;"
# #             "    background-color: #1976D2;"
# #             "    width: 12px;"
# #             "    margin: 3px 0px 3px 0px;"
# #             "    border-radius: 6px;"  # Zaokrąglenie paska przewijania
# #             "}"
# #             "QScrollBar::handle:vertical {"
# #             "    background-color: #0D47A1;"
# #             "    min-height: 20px;"
# #             "    border-radius: 6px;"  # Zaokrąglenie uchwytu
# #             "}"
# #             "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {"
# #             "    background: none;"
# #             "    height: 0px;"
# #             "}"  # Usunięcie przycisków przewijania
# #             "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {"
# #             "    background: none;"
# #             "}"  # Ukrycie dodatkowego tła przewijania
# #         )
# #         self.language_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
# #         self.language_selector.currentTextChanged.connect(self.on_language_changed)
# #         self.grid_layout.addWidget(self.language_selector, 0, 4, 1, 2)
# #
# #         # Przycisk "Wyczyść" (1,2)
# #         self.clear_button = QPushButton("Wyczyść")
# #         self.clear_button.setFont(QFont("Arial", 12))
# #         self.clear_button.setStyleSheet(
# #             "QPushButton {"
# #             "    background-color: lightgray;"
# #             "    border: 1px solid black;"
# #             "    border-radius: 10px;"
# #             "}"
# #             "QPushButton:hover {"
# #             "    background-color: gray;"
# #             "    color: white;"
# #             "}"
# #         )
# #         self.clear_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
# #         self.clear_button.clicked.connect(self.clear_text)
# #         self.grid_layout.addWidget(self.clear_button, 1, 4, 1, 2)
# #
# #         # Przycisk "Wyślij" (2,2)
# #         self.send_button = QPushButton("WYŚLIJ")
# #         self.send_button.setFont(QFont("Arial", 12, QFont.Bold))
# #         self.send_button.setStyleSheet(
# #             "QPushButton {"
# #             "    border: 1px solid black;"
# #             "    background-color: orange;"
# #             "    border-radius: 10px;"
# #             "}"
# #             "QPushButton:hover {"
# #             "    background-color: blue;"
# #             "    color: white;"
# #             "}"
# #         )
# #         self.send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
# #         self.send_button.clicked.connect(self.send_translated_command)
# #         self.grid_layout.addWidget(self.send_button, 2, 4, 1, 2)
# #
# #         # Gotowe zwroty (0,3) do (4,4)
# #         phrases = [
# #             "PODĄŻAJ ZA MNĄ", "STÓJ", "LEĆ W GÓRĘ", "LEĆ W DÓŁ",
# #             "OBRÓĆ W LEWO", "OBRÓĆ W PRAWO", "START", "LĄDUJ",
# #             "AUTOMATYCZNY", "MANUALNY"
# #         ]
# #
# #         row, col = 0, 6
# #         for phrase in phrases:
# #             phrase_button = QPushButton(phrase)
# #             phrase_button.setFont(QFont("Arial", 10))
# #             phrase_button.setStyleSheet(
# #                 "QPushButton {"
# #                 "    border: 1px solid black;"
# #                 "    background-color: lightblue;"
# #                 "    border-radius: 10px;"
# #                 "}"
# #                 "QPushButton:hover {"
# #                 "    background-color: blue;"
# #                 "    color: white;"
# #                 "}"
# #             )
# #             phrase_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
# #             phrase_button.clicked.connect(lambda _, ph=phrase: self.send_translated_phrase(ph))
# #             self.grid_layout.addWidget(phrase_button, row, col, 1, 2)
# #             col += 2
# #             if col > 8:
# #                 col = 6
# #                 row += 1
# #
# #         self.setLayout(self.grid_layout)
#     def create_map(self, latitude, longitude):
#         """Tworzy mapę za pomocą folium."""
#         try:
#             debug_print("localization_tab", f"Generowanie mapy dla współrzędnych: {latitude}, {longitude}")
#             folium_map = folium.Map(location=[latitude, longitude], zoom_start=15)
#             folium.Marker([latitude, longitude], tooltip="Lokalizacja").add_to(folium_map)
#             folium_map.save(self.map_file)
#             self.map_view.setUrl(QUrl.fromLocalFile(self.map_file))
#             debug_print("localization_tab", "Mapa została wygenerowana i załadowana")
#         except Exception as e:
#             debug_print("localization_tab", f"Błąd podczas generowania mapy: {e}")
#             QMessageBox.critical(self, "Błąd", f"Nie udało się wygenerować mapy: {e}")
#
#     def update_map(self):
#         """Aktualizuje mapę na podstawie wprowadzonych współrzędnych."""
#         try:
#             latitude = float(self.latitude_input.text())
#             longitude = float(self.longitude_input.text())
#             self.create_map(latitude, longitude)
#         except ValueError:
#             debug_print("localization_tab", "Błąd: Nieprawidłowe współrzędne")
#             QMessageBox.warning(self, "Błąd", "Wprowadź poprawne współrzędne.")
#
#
#
#
#
# ===========================================================================================================================
# ===========================================================================================================================
# ===========================================================================================================================
# ===========================================================================================================================
# ===========================================================================================================================
# from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QSizePolicy, QMessageBox
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtGui import QFont
# from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
# from Debuger import debug_print
# import folium
# import os
# import socket
#
# class ResponseThread(QThread):
#     response_received = pyqtSignal(str)
#
#     def __init__(self, connection):
#         super().__init__()
#         self.connection = connection
#         self.running = True
#
#     def run(self):
#         while self.running:
#             try:
#                 data = self.connection.recv(1024)
#                 if not data:
#                     break
#                 message = data.decode('utf-8').strip()
#                 self.response_received.emit(message)
#             except Exception as e:
#                 debug_print("localization_tab", f"Błąd podczas odbierania danych: {e}")
#                 break
#
#     def stop(self):
#         self.running = False
#
# class LocalizationTab(QWidget):
#     def __init__(self, parent=None):  # Dodanie domyślnego argumentu parent
#         super().__init__(parent)  # Przekazanie parent do klasy bazowej
#         self.parent_window = parent  # Przechowywanie referencji do rodzica
#         debug_print("localization_tab", "Inicjalizacja LocalizationTab")
#
#         # Główny layout siatki
#         self.grid_layout = QGridLayout()
#         self.grid_layout.setSpacing(5)
#         self.grid_layout.setContentsMargins(10, 10, 10, 10)
#
#         # Proporcje wierszy i kolumn - wyrównane proporcje
#         for i in range(7):
#             self.grid_layout.setRowStretch(i, 1)
#         for j in range(7):
#             self.grid_layout.setColumnStretch(j, 1)
#
#         # Widget mapy (QWebEngineView zamiast zastępczej etykiety)
#         self.map_view = QWebEngineView()
#         self.map_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.map_file = os.path.join(os.getcwd(), "map.html")
#         debug_print("localization_tab", f"Ścieżka pliku mapy: {self.map_file}")
#         debug_print("localization_tab", "Dodano widżet mapy")
#         self.grid_layout.addWidget(self.map_view, 0, 0, 4, 6)
#
#         # Widget logów (4,0) do (6,5)
#         self.logs_widget = QTextEdit()
#         self.logs_widget.setReadOnly(True)
#         self.logs_widget.setFont(QFont("Arial", 10))
#         self.logs_widget.setPlaceholderText("Logi będą wyświetlane tutaj...")
#         self.logs_widget.setStyleSheet("background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
#         self.logs_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         debug_print("localization_tab", "Dodano widget logów")
#         self.grid_layout.addWidget(self.logs_widget, 4, 0, 3, 6)
#
#         # Przyciski i pola tekstowe
#         button_size = QSizePolicy.Expanding
#         button_style = (
#             "QPushButton {"
#             "    background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;"
#             "}"
#             "QPushButton:hover {"
#             "    background-color: #6a5f31; color: black;"
#             "}"
#         )
#
#         self.start_button = QPushButton("Start")
#         self.start_button.setSizePolicy(button_size, button_size)
#         self.start_button.setStyleSheet(button_style)
#         self.start_button.clicked.connect(self.handle_start_button)
#         debug_print("localization_tab", "Dodano przycisk Start")
#         self.grid_layout.addWidget(self.start_button, 0, 6, 1, 1)
#
#         self.stop_button = QPushButton("Stop")
#         self.stop_button.setSizePolicy(button_size, button_size)
#         self.stop_button.setStyleSheet(button_style)
#         self.stop_button.clicked.connect(self.stop_response_thread)
#         debug_print("localization_tab", "Dodano przycisk Stop")
#         self.grid_layout.addWidget(self.stop_button, 1, 6, 1, 1)
#
#         self.longitude_input = QLineEdit()
#         self.longitude_input.setPlaceholderText("Długość geograficzna")
#         self.longitude_input.setSizePolicy(button_size, button_size)
#         self.longitude_input.setStyleSheet("background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
#         debug_print("localization_tab", "Dodano pole Longitude")
#         self.grid_layout.addWidget(self.longitude_input, 2, 6, 1, 1)
#
#         self.latitude_input = QLineEdit()
#         self.latitude_input.setPlaceholderText("Szerokość geograficzna")
#         self.latitude_input.setSizePolicy(button_size, button_size)
#         self.latitude_input.setStyleSheet("background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
#         debug_print("localization_tab", "Dodano pole Latitude")
#         self.grid_layout.addWidget(self.latitude_input, 3, 6, 1, 1)
#
#         self.set_coordinates_button = QPushButton("Wyznacz koordynaty")
#         self.set_coordinates_button.setSizePolicy(button_size, button_size)
#         self.set_coordinates_button.setStyleSheet(button_style)
#         self.set_coordinates_button.clicked.connect(self.update_map)
#         debug_print("localization_tab", "Dodano przycisk Wyznacz Koordynaty")
#         self.grid_layout.addWidget(self.set_coordinates_button, 4, 6, 1, 1)
#
#         self.speed_display = QLineEdit()
#         self.speed_display.setPlaceholderText("Prędkość")
#         self.speed_display.setReadOnly(True)
#         self.speed_display.setSizePolicy(button_size, button_size)
#         self.speed_display.setStyleSheet("background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
#         debug_print("localization_tab", "Dodano pole Speed")
#         self.grid_layout.addWidget(self.speed_display, 5, 6, 1, 1)
#
#         self.satellites_display = QLineEdit()
#         self.satellites_display.setPlaceholderText("Satelity")
#         self.satellites_display.setReadOnly(True)
#         self.satellites_display.setSizePolicy(button_size, button_size)
#         self.satellites_display.setStyleSheet("background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
#         debug_print("localization_tab", "Dodano pole Satellites")
#         self.grid_layout.addWidget(self.satellites_display, 6, 6, 1, 1)
#
#         self.setLayout(self.grid_layout)
#         debug_print("localization_tab", "Zakończono inicjalizację layoutu")
#
#         # Wątek odpowiedzi
#         self.response_thread = None
#
#         # Początkowe załadowanie mapy
#         self.create_map(52.2297, 21.0122)  # Warszawa jako domyślna lokalizacja
#
#     def create_map(self, latitude, longitude):
#         """Tworzy mapę za pomocą folium."""
#         try:
#             debug_print("localization_tab", f"Generowanie mapy dla współrzędnych: {latitude}, {longitude}")
#             folium_map = folium.Map(location=[latitude, longitude], zoom_start=15)
#             folium.Marker([latitude, longitude], tooltip="Lokalizacja").add_to(folium_map)
#             folium_map.save(self.map_file)
#             self.map_view.setUrl(QUrl.fromLocalFile(self.map_file))
#             debug_print("localization_tab", "Mapa została wygenerowana i załadowana")
#         except Exception as e:
#             debug_print("localization_tab", f"Błąd podczas generowania mapy: {e}")
#             QMessageBox.critical(self, "Błąd", f"Nie udało się wygenerować mapy: {e}")
#
#     def update_map(self):
#         """Aktualizuje mapę na podstawie wprowadzonych współrzędnych."""
#         try:
#             latitude = float(self.latitude_input.text())
#             longitude = float(self.longitude_input.text())
#             self.create_map(latitude, longitude)
#         except ValueError:
#             debug_print("localization_tab", "Błąd: Nieprawidłowe współrzędne")
#             QMessageBox.warning(self, "Błąd", "Wprowadź poprawne współrzędne.")
#
#     def is_connected(self):
#         """Sprawdza, czy aplikacja jest połączona z serwerem."""
#         debug_print("localization_tab", "Rozpoczęto sprawdzanie połączenia...")
#
#         # Sprawdź, czy parent_window istnieje
#         if not self.parent_window:
#             debug_print("localization_tab", "Brak parent_window")
#             return False
#
#         # Sprawdź, czy parent_window zawiera connect_tab
#         if not hasattr(self.parent_window, 'connect_tab'):
#             debug_print("localization_tab", "Brak connect_tab w parent_window")
#             return False
#
#         connect_tab = self.parent_window.connect_tab
#
#         # Sprawdź, czy connect_tab ma wymagane atrybuty
#         if not hasattr(connect_tab, 'connected') or not hasattr(connect_tab, 'connection_type'):
#             debug_print("localization_tab", "Brak atrybutów connected lub connection_type w connect_tab")
#             return False
#
#         # Sprawdź, czy połączenie jest aktywne
#         if not connect_tab.connected:
#             debug_print("localization_tab", "Nie jesteś połączony z serwerem")
#             return False
#
#         debug_print("localization_tab", "Połączenie z serwerem jest aktywne")
#         return True
#
#     def handle_start_button(self):
#         """Wysyła polecenie LOC do serwera i nasłuchuje odpowiedzi."""
#         if not self.is_connected():
#             debug_print("localization_tab", "Połączenie nieaktywne, przerwano wysyłanie.")
#             QMessageBox.warning(self, "Brak połączenia", "Musisz najpierw połączyć się z serwerem, aby wysłać komendę.")
#             return
#
#         command = "LOC"
#         debug_print("localization_tab", f"Przygotowano komendę: {command}")
#
#         try:
#             connect_tab = self.parent_window.connect_tab
#             connection_type = connect_tab.connection_type.currentText()
#             debug_print("localization_tab", f"Typ połączenia: {connection_type}")
#
#             if connection_type == "Socket/WiFi/Ethernet":
#                 if hasattr(connect_tab, 'sock') and connect_tab.sock:
#                     debug_print("localization_tab", "Socket jest aktywny. Próba wysłania komendy...")
#                     connect_tab.sock.sendall(command.encode('utf-8'))
#                     debug_print("localization_tab", f"Wysłano przez socket: {command}")
#                     self.start_response_thread(connect_tab.sock)
#                 else:
#                     debug_print("localization_tab", "Socket nie istnieje lub jest zamknięty.")
#                     QMessageBox.warning(self, "Błąd połączenia", "Socket nie jest aktywny.")
#             elif connection_type == "LoRa":
#                 if hasattr(connect_tab, 'serial_conn') and connect_tab.serial_conn:
#                     debug_print("localization_tab", "Połączenie LoRa aktywne. Próba wysłania komendy...")
#                     connect_tab.serial_conn.write(command.encode('utf-8'))
#                     debug_print("localization_tab", f"Wysłano przez LoRa: {command}")
#                     self.start_response_thread(connect_tab.serial_conn)
#                 else:
#                     debug_print("localization_tab", "LoRa nie istnieje lub jest zamknięta.")
#                     QMessageBox.warning(self, "Błąd połączenia", "LoRa nie jest aktywna.")
#             else:
#                 debug_print("localization_tab", f"Nieobsługiwany typ połączenia: {connection_type}")
#                 QMessageBox.warning(self, "Błąd połączenia", f"Nieobsługiwany typ połączenia: {connection_type}")
#         except Exception as e:
#             debug_print("localization_tab", f"Błąd podczas wysyłania: {e}")
#             QMessageBox.critical(self, "Błąd wysyłania", f"Nie udało się wysłać: {e}")
#
#     def start_response_thread(self, connection):
#         """Uruchamia wątek do nasłuchiwania odpowiedzi od serwera."""
#         if self.response_thread and self.response_thread.isRunning():
#             self.response_thread.stop()
#             self.response_thread.wait()
#
#         self.response_thread = ResponseThread(connection)
#         self.response_thread.response_received.connect(self.update_logs)
#         self.response_thread.start()
#         debug_print("localization_tab", "Uruchomiono wątek nasłuchiwania odpowiedzi.")
#
#     def stop_response_thread(self):
#         """Zatrzymuje wątek odpowiedzi, jeśli jest aktywny."""
#         if self.response_thread and self.response_thread.isRunning():
#             self.response_thread.stop()
#             self.response_thread.wait()
#             self.response_thread = None
#             debug_print("localization_tab", "Wątek odpowiedzi został zatrzymany.")
#
#     def update_logs(self, message):
#         """Aktualizuje logi w polu tekstowym."""
#         self.logs_widget.append(message)
#         debug_print("localization_tab", f"Log: {message}")
#
#
# from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QSizePolicy, QMessageBox
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtGui import QFont
# from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
# from Debuger import debug_print
# import folium
# import os
# import re
# from geopy.distance import geodesic
# from datetime import datetime
#
# class ResponseThread(QThread):
#     response_received = pyqtSignal(str)
#
#     def __init__(self, connection):
#         super().__init__()
#         self.connection = connection
#         self.running = True
#
#     def run(self):
#         while self.running:
#             try:
#                 data = self.connection.recv(1024)
#                 if not data:
#                     break
#                 message = data.decode('utf-8').strip()
#                 self.response_received.emit(message)
#             except Exception as e:
#                 debug_print("localization_tab", f"Błąd podczas odbierania danych: {e}")
#                 break
#
#     def stop(self):
#         self.running = False
#
# class LocalizationTab(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.parent_window = parent
#         debug_print("localization_tab", "Inicjalizacja LocalizationTab")
#
#         self.grid_layout = QGridLayout()
#         self.grid_layout.setSpacing(5)
#         self.grid_layout.setContentsMargins(10, 10, 10, 10)
#
#         for i in range(7):
#             self.grid_layout.setRowStretch(i, 1)
#         for j in range(7):
#             self.grid_layout.setColumnStretch(j, 1)
#
#         self.map_view = QWebEngineView()
#         self.map_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.map_file = os.path.join(os.getcwd(), "map.html")
#         debug_print("localization_tab", f"Ścieżka pliku mapy: {self.map_file}")
#         self.grid_layout.addWidget(self.map_view, 0, 0, 4, 6)
#
#         self.logs_widget = QTextEdit()
#         self.logs_widget.setReadOnly(True)
#         self.logs_widget.setFont(QFont("Arial", 10))
#         self.logs_widget.setPlaceholderText("Logi będą wyświetlane tutaj...")
#         self.logs_widget.setStyleSheet("background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
#         self.logs_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.grid_layout.addWidget(self.logs_widget, 4, 0, 3, 6)
#
#         button_size = QSizePolicy.Expanding
#         button_style = (
#             "QPushButton {"
#             "    background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;"
#             "}"
#             "QPushButton:hover {"
#             "    background-color: #6a5f31; color: black;"
#             "}"
#         )
#
#         self.start_button = QPushButton("Start")
#         self.start_button.setSizePolicy(button_size, button_size)
#         self.start_button.setStyleSheet(button_style)
#         self.start_button.clicked.connect(self.handle_start_button)
#         self.grid_layout.addWidget(self.start_button, 0, 6, 1, 1)
#
#         self.stop_button = QPushButton("Stop")
#         self.stop_button.setSizePolicy(button_size, button_size)
#         self.stop_button.setStyleSheet(button_style)
#         self.stop_button.clicked.connect(self.stop_response_thread)
#         self.grid_layout.addWidget(self.stop_button, 1, 6, 1, 1)
#
#         self.longitude_input = QLineEdit()
#         self.longitude_input.setPlaceholderText("Długość geograficzna")
#         self.longitude_input.setSizePolicy(button_size, button_size)
#         self.longitude_input.setStyleSheet("background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
#         self.grid_layout.addWidget(self.longitude_input, 2, 6, 1, 1)
#
#         self.latitude_input = QLineEdit()
#         self.latitude_input.setPlaceholderText("Szerokość geograficzna")
#         self.latitude_input.setSizePolicy(button_size, button_size)
#         self.latitude_input.setStyleSheet("background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
#         self.grid_layout.addWidget(self.latitude_input, 3, 6, 1, 1)
#
#         self.set_coordinates_button = QPushButton("Wyznacz koordynaty")
#         self.set_coordinates_button.setSizePolicy(button_size, button_size)
#         self.set_coordinates_button.setStyleSheet(button_style)
#         self.set_coordinates_button.clicked.connect(self.update_map)
#         self.grid_layout.addWidget(self.set_coordinates_button, 4, 6, 1, 1)
#
#         self.speed_display = QLineEdit()
#         self.speed_display.setPlaceholderText("Prędkość")
#         self.speed_display.setReadOnly(True)
#         self.speed_display.setSizePolicy(button_size, button_size)
#         self.speed_display.setStyleSheet("background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
#         self.grid_layout.addWidget(self.speed_display, 5, 6, 1, 1)
#
#         self.satellites_display = QLineEdit()
#         self.satellites_display.setPlaceholderText("Satelity")
#         self.satellites_display.setReadOnly(True)
#         self.satellites_display.setSizePolicy(button_size, button_size)
#         self.satellites_display.setStyleSheet("background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
#         self.grid_layout.addWidget(self.satellites_display, 6, 6, 1, 1)
#
#         self.setLayout(self.grid_layout)
#         debug_print("localization_tab", "Zakończono inicjalizację layoutu")
#
#         self.response_thread = None
#         self.previous_coordinates = None
#         self.previous_time = None
#
#         self.create_map(52.2297, 21.0122)
#
#     def create_map(self, latitude, longitude):
#         try:
#             self.folium_map = folium.Map(location=[latitude, longitude], zoom_start=15)
#             folium.Marker([latitude, longitude], tooltip="Lokalizacja").add_to(self.folium_map)
#             self.folium_map.save(self.map_file)
#             self.map_view.setUrl(QUrl.fromLocalFile(self.map_file))
#         except Exception as e:
#             QMessageBox.critical(self, "Błąd", f"Nie udało się wygenerować mapy: {e}")
#
#     def update_map(self):
#         try:
#             latitude = float(self.latitude_input.text())
#             longitude = float(self.longitude_input.text())
#             self.create_map(latitude, longitude)
#         except ValueError:
#             QMessageBox.warning(self, "Błąd", "Wprowadź poprawne współrzędne.")
#
#     def is_connected(self):
#         """Sprawdza, czy aplikacja jest połączona z serwerem."""
#         debug_print("localization_tab", "Rozpoczęto sprawdzanie połączenia...")
#
#         # Sprawdź, czy parent_window istnieje
#         if not self.parent_window:
#             debug_print("localization_tab", "Brak parent_window")
#             return False
#
#         # Sprawdź, czy parent_window zawiera connect_tab
#         if not hasattr(self.parent_window, 'connect_tab'):
#             debug_print("localization_tab", "Brak connect_tab w parent_window")
#             return False
#
#         connect_tab = self.parent_window.connect_tab
#
#         # Sprawdź, czy connect_tab ma wymagane atrybuty
#         if not hasattr(connect_tab, 'connected') or not hasattr(connect_tab, 'connection_type'):
#             debug_print("localization_tab", "Brak atrybutów connected lub connection_type w connect_tab")
#             return False
#
#         # Sprawdź, czy połączenie jest aktywne
#         if not connect_tab.connected:
#             debug_print("localization_tab", "Nie jesteś połączony z serwerem")
#             return False
#
#         debug_print("localization_tab", "Połączenie z serwerem jest aktywne")
#         return True
#
#     def handle_start_button(self):
#         """Wysyła polecenie LOC do serwera i nasłuchuje odpowiedzi."""
#         if not self.is_connected():
#             debug_print("localization_tab", "Połączenie nieaktywne, przerwano wysyłanie.")
#             QMessageBox.warning(self, "Brak połączenia", "Musisz najpierw połączyć się z serwerem, aby wysłać komendę.")
#             return
#
#         command = "LOC"
#         debug_print("localization_tab", f"Przygotowano komendę: {command}")
#
#         try:
#             connect_tab = self.parent_window.connect_tab
#             connection_type = connect_tab.connection_type.currentText()
#             debug_print("localization_tab", f"Typ połączenia: {connection_type}")
#
#             if connection_type == "Socket/WiFi/Ethernet":
#                 if hasattr(connect_tab, 'sock') and connect_tab.sock:
#                     debug_print("localization_tab", "Socket jest aktywny. Próba wysłania komendy...")
#                     connect_tab.sock.sendall(command.encode('utf-8'))
#                     debug_print("localization_tab", f"Wysłano przez socket: {command}")
#                     self.start_response_thread(connect_tab.sock)
#                 else:
#                     debug_print("localization_tab", "Socket nie istnieje lub jest zamknięty.")
#                     QMessageBox.warning(self, "Błąd połączenia", "Socket nie jest aktywny.")
#             elif connection_type == "LoRa":
#                 if hasattr(connect_tab, 'serial_conn') and connect_tab.serial_conn:
#                     debug_print("localization_tab", "Połączenie LoRa aktywne. Próba wysłania komendy...")
#                     connect_tab.serial_conn.write(command.encode('utf-8'))
#                     debug_print("localization_tab", f"Wysłano przez LoRa: {command}")
#                     self.start_response_thread(connect_tab.serial_conn)
#                 else:
#                     debug_print("localization_tab", "LoRa nie istnieje lub jest zamknięta.")
#                     QMessageBox.warning(self, "Błąd połączenia", "LoRa nie jest aktywna.")
#             else:
#                 debug_print("localization_tab", f"Nieobsługiwany typ połączenia: {connection_type}")
#                 QMessageBox.warning(self, "Błąd połączenia", f"Nieobsługiwany typ połączenia: {connection_type}")
#         except Exception as e:
#             debug_print("localization_tab", f"Błąd podczas wysyłania: {e}")
#             QMessageBox.critical(self, "Błąd wysyłania", f"Nie udało się wysłać: {e}")
#
#     def start_response_thread(self, connection):
#         if self.response_thread and self.response_thread.isRunning():
#             self.response_thread.stop()
#             self.response_thread.wait()
#
#         self.response_thread = ResponseThread(connection)
#         self.response_thread.response_received.connect(self.update_logs)
#         self.response_thread.start()
#
#     def stop_response_thread(self):
#         if self.response_thread and self.response_thread.isRunning():
#             self.response_thread.stop()
#             self.response_thread.wait()
#             self.response_thread = None
#
#     def update_logs(self, message):
#         self.logs_widget.append(message)
#         parsed_data = self.parse_log(message)
#         if parsed_data:
#             latitude, longitude, satellites, timestamp = parsed_data
#             self.update_map_view(latitude, longitude)
#             self.update_satellite_widget(satellites)
#             self.calculate_speed(latitude, longitude, timestamp)
#
#     def parse_log(self, log_line):
#         debug_print("localization_tab", f"Parsing log: {log_line}")
#         match = re.search(r"Szerokość: ([\d.]+), Długość: ([\d.]+) \| Liczba widocznych satelitów: (\d+)", log_line)
#         if match:
#             latitude = float(match.group(1))
#             longitude = float(match.group(2))
#             satellites = int(match.group(3))
#             time_match = re.search(r"Czas: ([\d:.]+)", log_line)
#             timestamp = time_match.group(1) if time_match else None
#             debug_print("localization_tab",
#                         f"Parsed data - Latitude: {latitude}, Longitude: {longitude}, Satellites: {satellites}, Timestamp: {timestamp}")
#             return latitude, longitude, satellites, timestamp
#         debug_print("localization_tab", "Failed to parse log.")
#         return None
#
#     def update_map_view(self, latitude, longitude):
#         debug_print("localization_tab", f"Updating map with coordinates: {latitude}, {longitude}")
#         if self.previous_coordinates:
#             folium.PolyLine([self.previous_coordinates, (latitude, longitude)], color="blue").add_to(self.folium_map)
#         folium.Marker([latitude, longitude], tooltip=f"Lat: {latitude}, Lon: {longitude}").add_to(self.folium_map)
#         self.previous_coordinates = (latitude, longitude)
#         self.folium_map.save(self.map_file)
#         # Wymuszenie odświeżenia mapy
#         self.map_view.setUrl(QUrl(""))  # Ustawienie pustego URL, aby wyczyścić widok
#         self.map_view.setUrl(QUrl.fromLocalFile(self.map_file))  # Ponowne załadowanie mapy
#
#     def update_satellite_widget(self, satellites):
#         self.satellites_display.setText(str(satellites))
#
#     def calculate_speed(self, latitude, longitude, timestamp):
#         if self.previous_coordinates and self.previous_time:
#             current_coordinates = (latitude, longitude)
#             distance = geodesic(self.previous_coordinates, current_coordinates).meters
#             time_delta = (datetime.strptime(timestamp, "%H:%M:%S.%f") - self.previous_time).total_seconds()
#             if time_delta > 0:
#                 speed = distance / time_delta
#                 self.speed_display.setText(f"{speed:.2f} m/s")
#         self.previous_time = datetime.strptime(timestamp, "%H:%M:%S.%f")
import serial
import serial.tools.list_ports
import time
import threading

COM_PORT = "COM4"  # Symulowany port LoRa
BAUD_RATE = 9600
STOP_EMULATOR = False  # Flaga zatrzymania emulatora

def is_com_available(port):
    """Sprawdza, czy COM jest dostępny."""
    ports = [p.device for p in serial.tools.list_ports.comports()]
    return port in ports

def fake_lora_device():
    """Emulator LoRa na COM8 bez blokowania portu."""
    global STOP_EMULATOR
    print(f"🎯 Emulator LoRa działa na {COM_PORT} @ {BAUD_RATE} baud")

    while not STOP_EMULATOR:
        try:
            # Sprawdzamy, czy port jest dostępny
            if not is_com_available(COM_PORT):
                print(f"⚠️ Port {COM_PORT} nie jest dostępny! Czekam...")
                time.sleep(2)
                continue

            # Otwieramy port na chwilę, aby nie blokować
            with serial.Serial(COM_PORT, BAUD_RATE, timeout=1) as ser:
                if ser.in_waiting:
                    received_data = ser.readline().decode("utf-8").strip()
                    print(f"📩 Otrzymano: {received_data}")

                    # Symulowana odpowiedź LoRa
                    if received_data == "PING":
                        response = "PONG\n"
                    elif received_data.startswith("DATA:"):
                        response = f"ACK:{received_data[5:]}\n"
                    else:
                        response = "ERROR: Unknown command\n"

                    time.sleep(0.2)  # Symulacja czasu przetwarzania
                    ser.write(response.encode("utf-8"))
                    print(f"📤 Wysłano: {response.strip()}")

        except serial.SerialException as e:
            print(f"❌ Błąd dostępu do {COM_PORT}: {e}")

        time.sleep(0.5)  # Krótka pauza, aby inny program mógł używać portu

if __name__ == "__main__":
    # Uruchamiamy emulator w tle
    emulator_thread = threading.Thread(target=fake_lora_device, daemon=True)
    emulator_thread.start()

    try:
        while True:
            cmd = input("💻 Wpisz komendę do wysłania (PING, DATA:123, exit): ")
            if cmd.lower() == "exit":
                STOP_EMULATOR = True
                break

            try:
                if not is_com_available(COM_PORT):
                    print(f"⚠️ Port {COM_PORT} nie jest dostępny!")
                    continue

                with serial.Serial(COM_PORT, BAUD_RATE, timeout=1) as ser:
                    ser.write(f"{cmd}\n".encode("utf-8"))
                    time.sleep(0.5)  # Czekamy na odpowiedź
                    response = ser.readline().decode("utf-8").strip()
                    print(f"💡 Odpowiedź z LoRa: {response}")
            except serial.SerialException as e:
                print(f"❌ Błąd przy wysyłaniu danych: {e}")

    except KeyboardInterrupt:
        STOP_EMULATOR = True  # Zatrzymanie emulatora
        print("🔴 Emulator zatrzymany.")
