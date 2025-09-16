import os
from PyQt5.QtWidgets import QWidget, QGridLayout, QTextEdit, QComboBox, QSizePolicy, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from translatepy import Translate
import wave
import pyaudio
from Debuger import debug_print
from loralibery import encrypt_data, decrypt_data

class PlaybackThread(QThread):
    playback_finished = pyqtSignal()  # Sygnał zakończenia odtwarzania

    def __init__(self, audio_file, start_frame=0, parent=None):
        super().__init__(parent)
        self.audio_file = audio_file
        self.start_frame = start_frame
        self.current_frame = start_frame
        self.is_playing = True

    def run(self):
        try:
            wf = wave.open(self.audio_file, "rb")
            audio_interface = pyaudio.PyAudio()

            stream = audio_interface.open(
                format=audio_interface.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )

            # Przesuwanie do odpowiedniej ramki
            wf.setpos(self.start_frame)

            data = wf.readframes(1024)
            while data and self.is_playing:
                stream.write(data)
                self.current_frame = wf.tell()
                data = wf.readframes(1024)

            stream.stop_stream()
            stream.close()
            audio_interface.terminate()
            wf.close()
        finally:
            self.playback_finished.emit()

    def stop(self):
        self.is_playing = False


class AudioTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.connect_tab = self.parent_window.connect_tab  # Referencja do ConnectTab
        debug_print("audio_tab", f"Inicjalizacja AudioTab")

        # Inicjalizacja obiektu Translate
        self.translator = Translate()

        # Główny layout siatki
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        # Pole do wpisywania tekstu (0,0) do (1,1)
        self.text_input = QTextEdit()
        self.text_input.setFont(QFont("Arial", 22, QFont.Bold))
        self.text_input.setPlaceholderText("Pole do wpisania tekstu")
        self.text_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.text_input, 0, 0, 2, 4)

        # Pole do wyświetlania tłumaczenia (2,0) do (3,1)
        self.translation_display = QTextEdit()
        self.translation_display.setFont(QFont("Arial", 22, QFont.Bold))
        self.translation_display.setReadOnly(True)
        self.translation_display.setPlaceholderText("Tutaj pojawi się tłumaczenie...")
        self.translation_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.translation_display, 2, 0, 2, 4)

        # Ikony
        self.record_icon = QIcon("microphone.png")
        self.recorded_audio_icon = QIcon("recording_audio.png")
        self.play_icon = QIcon("play.png")
        self.stop_icon = QIcon("pause.png")
        self.delete_icon = QIcon("trash.png")

        # Przycisk nagrywania (4,0)
        self.record_button = QPushButton()
        self.record_button.setIcon(self.record_icon)
        self.record_button.clicked.connect(self.toggle_recording)
        self.record_button.setStyleSheet(
                "    height: 100px;"
            )
        self.grid_layout.addWidget(self.record_button, 4, 0, 1, 1)

        # Label statusu nagrywania
        self.recording_status_label = QLabel("Brak audio")  # Domyślny napis
        self.recording_status_label.setFont(QFont("Arial", 22, QFont.Bold))
        self.recording_status_label.setAlignment(Qt.AlignCenter)
        self.grid_layout.addWidget(self.recording_status_label, 4, 1, 1, 1)

        # Etykieta czasu nagrania
        self.time_label = QLabel("00:00")  # Domyślny czas
        self.time_label.setFont(QFont("Arial", 22, QFont.Bold))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.grid_layout.addWidget(self.time_label, 4, 2, 1, 1)

        # Przycisk odtwarzania (4,3)
        self.play_button = QPushButton()
        self.play_button.setIcon(self.play_icon)
        self.play_button.clicked.connect(self.toggle_playback)
        self.play_button.setEnabled(False)
        self.grid_layout.addWidget(self.play_button, 4, 3, 1, 1)

        # Przycisk zatrzymywania odtwarzania (4,4)
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.stop_icon)
        self.stop_button.clicked.connect(self.stop_playback)
        self.stop_button.setEnabled(False)
        self.grid_layout.addWidget(self.stop_button, 4, 4, 1, 1)

        # Przycisk kasowania (4,5)
        self.delete_button = QPushButton()
        self.delete_button.setIcon(self.delete_icon)
        self.delete_button.clicked.connect(self.delete_audio)
        self.delete_button.setEnabled(False)
        self.grid_layout.addWidget(self.delete_button, 4, 5, 1, 1)

        # Zmienna audio
        self.recording = False
        self.frames = []
        self.stream = None
        self.audio_interface = pyaudio.PyAudio()
        self.output_file = "recording.mp3"
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.current_time = 0
        self.playback_thread = None
        self.playback_position = 0  # Pozycja w ramkach

        self.setLayout(self.grid_layout)

        # Wybór języka (0,4)
        self.language_selector = QComboBox()
        self.language_selector.setFont(QFont("Arial", 22, QFont.Bold))
        self.language_selector.setFixedHeight(125)
        self.language_selector.addItems([
            "Polski", "Angielski", "Niemiecki", "Francuski", "Hiszpański",
            "Ukraiński", "Rosyjski", "Włoski", "Szwedzki", "Norweski"
        ])
        self.language_selector.setCurrentIndex(0)
        self.language_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.language_selector.currentTextChanged.connect(self.on_language_changed)
        self.grid_layout.addWidget(self.language_selector, 0, 4, 1, 2)

        # Przycisk "Wyczyść" (1,4)
        self.clear_button = QPushButton("Wyczyść")
        self.clear_button.setFont(QFont("Arial", 22, QFont.Bold))
        self.clear_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clear_button.clicked.connect(self.clear_text)
        self.grid_layout.addWidget(self.clear_button, 1, 4, 1, 2)

        # Przycisk "Wyślij" (2,4)
        self.send_button = QPushButton("Wyślij")
        self.send_button.setFont(QFont("Arial", 22, QFont.Bold))
        self.send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.send_button.clicked.connect(self.send_translated_command)
        self.grid_layout.addWidget(self.send_button, 2, 4, 1, 2)

        empty_placeholder = QWidget()
        empty_placeholder.setFixedHeight(111)  # Wymuszenie wysokości na 100px
        self.grid_layout.addWidget(empty_placeholder, 3, 4, 1, 2)

        # Gotowe zwroty
        phrases = [
            "PODDAJ SIĘ", "RZUĆ BROŃ", "NIE STRZELAJ", "POMOC W DRODZE", "ZAKAZ WSTĘPU", "UWAGA!!!", "ZOSTAŃ W DOMU", "ZAGROŻENIE", "OPUŚĆ TEREN", "EWAKUACJA"
        ]
        row, col = 0, 6
        for phrase in phrases:
            phrase_button = QPushButton(phrase)
            phrase_button.setFont(QFont("Arial", 18, QFont.Bold))
            phrase_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            phrase_button.clicked.connect(lambda _, ph=phrase: self.send_translated_phrase(ph))
            self.grid_layout.addWidget(phrase_button, row, col, 1, 2)
            col += 2
            if col > 8:
                col = 6
                row += 1

        # Ustawienia stylów w zależności od trybu
        self.update_styles()

        self.setLayout(self.grid_layout)
        self.connect_tab.connection_type.currentIndexChanged.connect(self.update_button_availability)
        self.update_button_availability()

    def update_styles(self):
        """Aktualizuje style w zależności od trybu aplikacji."""
        is_dark_mode = self.parent_window.is_dark_mode if self.parent_window else True
        text_color = "white" if is_dark_mode else "black"
        background_color = "#1E1E1E" if is_dark_mode else "white"
        border_color = "#6a5f31" if is_dark_mode else "#A0A0A0"

        self.text_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {background_color};
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 10px;
            }}
        """)
        self.translation_display.setStyleSheet(f"""
            QTextEdit {{
                background-color: {background_color};
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 10px;
            }}
        """)
        self.language_selector.setStyleSheet(f"""
            QComboBox {{
                background-color: {background_color};
                height: 150px;
                color: {text_color};
                border: 2px solid {border_color};
                border-radius: 10px;
                padding: 5px;
            }}
        """)

        for button in self.findChildren(QPushButton):
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {background_color};
                    color: {text_color};
                    border: 2px solid {border_color};
                    border-radius: 10px;
                }}
                QPushButton:hover {{
                    background-color: {border_color};
                    color: white;
                }}
            """)
        if is_dark_mode:
            common_style = "background-color: #121212; color: white; border: 2px solid #6a5f31; border-radius: 10px;"
            button_style = (
                "QPushButton {"
                "    background-color: #333333; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;"
                "    height: 100px;"
                "}"
                "QPushButton:hover {"
                "    background-color: #555555;"
                "}"
                "QPushButton:pressed {"
                "    background-color: #222222;"
                "}"
            )
        else:
            common_style = "background-color: #FFFFFF; color: black; border: 2px solid #6a5f31; border-radius: 10px;"
            button_style = (
                "QPushButton {"
                "    background-color: #F0F0F0; color: black; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;"
                "    height: 100px;"
                "}"
                "QPushButton:hover {"
                "    background-color: #E0E0E0;"
                "}"
                "QPushButton:pressed {"
                "    background-color: #D0D0D0;"
                "}"
            )
            # Stosowanie stylów
        self.text_input.setStyleSheet(common_style)
        self.translation_display.setStyleSheet(common_style)
        self.record_button.setStyleSheet(button_style)
        self.recording_status_label.setStyleSheet(common_style)
        self.time_label.setStyleSheet(common_style)
        self.play_button.setStyleSheet(button_style)
        self.stop_button.setStyleSheet(button_style)
        self.delete_button.setStyleSheet(button_style)
        self.language_selector.setStyleSheet(common_style)
        self.clear_button.setStyleSheet(button_style)
        self.send_button.setStyleSheet(button_style)

    def update_time(self):
        try:
            self.current_time += 1
            minutes, seconds = divmod(self.current_time, 60)
            self.time_label.setText(f"{minutes:02}:{seconds:02}")
        except Exception as e:
            print(f"\033[32m\033[1m[DEBUG]\033[0m  Error in update_time: {e}")

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        try:
            self.recording_status_label.setText("Nagrywanie")
            self.stream = self.audio_interface.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024
            )
            self.frames = []
            self.recording = True
            self.current_time = 0
            self.time_label.setText("00:00")  # Reset czasu
            self.timer.start(1000)
            self.record_button.setIcon(self.stop_icon)

            def callback():
                try:
                    while self.recording:
                        data = self.stream.read(1024)
                        self.frames.append(data)
                except Exception as e:
                    print(f"\033[32m\033[1m[DEBUG]\033[0m  Error in recording callback: {e}")

            import threading
            threading.Thread(target=callback, daemon=True).start()
        except Exception as e:
            print(f"\033[32m\033[1m[DEBUG]\033[0m  Error in start_recording: {e}")

    def stop_recording(self):
        try:
            self.recording = False
            self.timer.stop()

            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None

            with wave.open(self.output_file, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(self.audio_interface.get_sample_size(pyaudio.paInt16))
                wf.setframerate(44100)
                wf.writeframes(b"".join(self.frames))

            self.recording_status_label.setText("Wstrzymano")
            self.record_button.setIcon(self.record_icon)
            self.play_button.setEnabled(True)
            self.delete_button.setEnabled(True)
        except Exception as e:
            print(f"\033[32m\033[1m[DEBUG]\033[0m  Error in stop_recording: {e}")

    def toggle_playback(self):
        try:
            # Jeśli odtwarzanie jest w toku, zatrzymaj ręcznie
            if self.playback_thread and self.playback_thread.isRunning():
                self.stop_playback(finished=False)  # Ręczne zatrzymanie
            else:
                # Rozpocznij nowe odtwarzanie
                self.recording_status_label.setText("Słuchanie audio")
                self.play_button.setEnabled(False)
                self.stop_button.setEnabled(True)

                # Tworzenie i uruchamianie wątku odtwarzania
                self.playback_thread = PlaybackThread(self.output_file, start_frame=self.playback_position)
                self.playback_thread.playback_finished.connect(self.on_playback_finished)
                self.playback_thread.start()
        except Exception as e:
            print(f"\033[32m\033[1m[DEBUG]\033[0m  Error in toggle_playback: {e}")

    def on_playback_finished(self):
        self.recording_status_label.setText("Odtwarzanie zakończone")
        if self.playback_thread:
            self.playback_position = self.playback_thread.current_frame  # Zachowanie pozycji
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.playback_position = 0
        self.playback_thread = None

    def stop_playback(self):
        try:
            if self.playback_thread and self.playback_thread.isRunning():
                self.playback_thread.stop()
                self.playback_thread.wait()
                self.playback_position = self.playback_thread.current_frame  # Zachowanie pozycji
                self.recording_status_label.setText("Odtwarzanie zatrzymane")
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(False)
        except Exception as e:
            print(f"\033[32m\033[1m[DEBUG]\033[0m  Error in stop_playback: {e}")

    def delete_audio(self):
        try:
            self.frames = []
            self.output_file = "recording.wav"
            self.recording_status_label.setText("Usunięto audio")
            self.time_label.setText("00:00")  # Reset czasu
            self.current_time = 0
            self.play_button.setEnabled(False)
            self.delete_button.setEnabled(False)
        except Exception as e:
            print(f"\033[32m\033[1m[DEBUG]\033[0m  Error in delete_audio: {e}")

    def clear_text(self):
        """Czyści pola tekstowe i tłumaczenia."""
        self.text_input.clear()
        self.translation_display.clear()

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
            debug_print("audio_tab", f"Tłumaczenie na {self.language_selector.currentText()}: {translation.result}")
        except Exception as e:
            QMessageBox.critical(self, debug_print("audio_tab", f"Nie udało się przetłumaczyć tekstu: {e}"))

    def is_connected(self):
        """
        Sprawdza, czy aplikacja jest połączona z serwerem.
        Wyświetla komunikat o błędzie, jeśli połączenie nie istnieje.
        """
        if not self.parent_window or not hasattr(self.parent_window, 'connect_tab'):
            QMessageBox.warning(self, "Błąd", "Brak połączenia z serwerem. Proszę się połączyć.")
            return False
        connect_tab = self.parent_window.connect_tab
        if not connect_tab.connected:
            QMessageBox.warning(self, "Błąd", "Nie jesteś połączony z serwerem. Proszę się połączyć.")
            return False
        return True

    def send_translated_phrase(self, phrase):
        """
        Tłumaczy i wysyła wybraną frazę w odpowiednim języku, jeśli połączenie jest aktywne.
        """
        if not self.is_connected():
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
            translation = self.translator.translate(phrase, target_language)
            self.send_command(translation.result)
            debug_print("audio_tab",
                        f"Wysłano przetłumaczoną frazę ({self.language_selector.currentText()}): {translation.result}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się przetłumaczyć frazy: {e}")

    def send_translated_command(self):
        """
        Wysyła przetłumaczony tekst, tekst użytkownika lub plik audio na serwer, jeśli połączenie jest aktywne.
        """
        if not self.is_connected():
            return

        translated_text = self.translation_display.toPlainText().strip()
        user_text = self.text_input.toPlainText().strip()
        connect_tab = self.parent_window.connect_tab

        try:
            if translated_text:
                self.send_command(translated_text)
            elif user_text:
                self.send_command(user_text)
            elif os.path.exists(self.output_file):
                file_name = os.path.basename(self.output_file)
                file_size = os.path.getsize(self.output_file)

                # Wysyłanie metadanych pliku BEZ tłumaczenia i szyfrowania
                au_file_command = f"AU_FILE :{file_name}:{file_size}"
                debug_print("audio_tab", f"Wysyłanie metadanych: {au_file_command}")
                if connect_tab.connection_type.currentText() == "Socket/WiFi/Ethernet":
                    connect_tab.sock.sendall(au_file_command.encode())
                elif connect_tab.connection_type.currentText() == "LoRa":
                    connect_tab.serial_conn.write(au_file_command.encode())

                # Wysyłanie pliku audio w surowych bajtach, BEZ szyfrowania
                with open(self.output_file, "rb") as audio_file:
                    for chunk in iter(lambda: audio_file.read(1024), b""):
                        if not chunk:
                            break

                        debug_print("audio_tab", f"Odczytano fragment: {chunk[:10]}...")

                        # Wysyłanie danych przez socket lub LoRę
                        if connect_tab.connection_type.currentText() == "Socket/WiFi/Ethernet":
                            connect_tab.sock.sendall(chunk)
                        elif connect_tab.connection_type.currentText() == "LoRa":
                            connect_tab.serial_conn.write(chunk)

                        debug_print("audio_tab", f"Wysłano porcję danych: {len(chunk)} bajtów")

                QMessageBox.information(self, "Sukces", "Plik audio został wysłany.")
                debug_print("audio_tab", "Wysyłanie pliku zakończone pomyślnie.")
            else:
                QMessageBox.warning(self, "Błąd", "Plik audio nie istnieje. Nagrywaj dźwięk przed wysłaniem.")
        except Exception as e:
            debug_print("audio_tab", f"Błąd podczas wysyłania: {e}")
            QMessageBox.critical(self, "Błąd", f"Nie udało się wysłać danych: {e}")

    def send_command(self, command):
        """
        Wysyła wybraną komendę do serwera, jeśli połączenie jest aktywne.
        """
        if not self.is_connected():
            return

        connect_tab = self.parent_window.connect_tab
        try:
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
            # Pobierz kod języka na podstawie wybranego tekstu
            target_language = target_language_map.get(self.language_selector.currentText(), "pl")

            # Przetłumacz komendę na wybrany język
            translation = self.translator.translate(command, target_language)
            # Dodaj do wyniku prefiks "AU " oraz kod języka
            translated_command = f"AU {target_language} " + translation.result

            # Szyfrowanie komendy (prefiks "TX" był tylko przykładowo wspomniany w komentarzu)
            encrypted_data, index1, index2, iv, tag = encrypt_data(translated_command.encode('utf-8'))
            message = (index1.to_bytes(1, 'little') +
                       index2.to_bytes(1, 'big') +
                       iv +
                       encrypted_data +
                       tag)

            # Wysyłanie danych przez socket lub LoRę
            response = None

            if connect_tab.connection_type.currentText() == "Socket/WiFi/Ethernet":
                connect_tab.sock.sendall(message)
                debug_print("audio_tab", f"Wysłano: {message}")

                # Oczekiwanie na odpowiedź
                connect_tab.sock.settimeout(5)  # Timeout na 5 sekund
                response = connect_tab.sock.recv(1024)  # Odbiór do 1024 bajtów
                self.handle_server_response(response)
            elif connect_tab.connection_type.currentText() == "LoRa":
                connect_tab.serial_conn.write(message)
                debug_print("audio_tab", f"Wysłano przez LoRa: {message}")

                # Oczekiwanie na odpowiedź (dla LoRy trzeba odpowiednio skonfigurować)
                response = connect_tab.serial_conn.read_until(
                    b'\n')  # Przykład: oczekiwanie na dane zakończone znakiem nowej linii
                self.handle_server_response(response)

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wysłać komendy: {e}")

    def handle_server_response(self, response: bytes):
        """
        Obsługuje odpowiedź z serwera, dekodując ją i wyświetlając w logach.

        Args:
            response (bytes): Odebrane dane z serwera.
        """
        try:
            # Rozpakowanie wiadomości (zakładamy format zgodny z funkcją szyfrowania)
            index1 = response[0]
            index2 = response[1]
            iv = response[2:14]  # 12 bajtów IV
            tag = response[-16:]  # Ostatnie 16 bajtów to tag
            encrypted_data = response[14:-16]  # Reszta to dane

            # Dekodowanie wiadomości
            decrypted_message = decrypt_data(encrypted_data, index1, index2, iv, tag)
            debug_print("text_tab", f"Otrzymano i odszyfrowano wiadomość: {decrypted_message}")

            # Przekazanie do logów LocalizationTab
            if hasattr(self.parent_window, 'localization_tab'):
                self.parent_window.localization_tab.update_logs(decrypted_message)
                debug_print("text_tab", "Przekazano odszyfrowaną wiadomość do LocalizationTab.")
            else:
                debug_print("text_tab", "Nie znaleziono LocalizationTab w parent_window.")
        except Exception as e:
            debug_print("text_tab", f"Błąd podczas obsługi odpowiedzi: {e}")

    def update_button_availability(self):
        """Aktualizuje stan przycisków w zależności od wybranego typu połączenia."""
        if self.connect_tab.connection_type.currentText() == "LoRa":
            # Zablokowanie przycisków, jeśli wybrano LoRa
            self.record_button.setEnabled(False)
            self.play_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.delete_button.setEnabled(False)
        else:
            # Odblokowanie przycisków dla połączenia Socket/WiFi/Ethernet
            self.record_button.setEnabled(True)
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.delete_button.setEnabled(True)
