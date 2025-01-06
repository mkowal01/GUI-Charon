from PyQt5.QtWidgets import QWidget, QGridLayout, QTextEdit, QComboBox, QSizePolicy, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from translatepy import Translate
import wave
import pyaudio

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

        print("Inicjalizacja AudioTab")

        # Inicjalizacja obiektu Translate
        self.translator = Translate()

        # Główny layout siatki
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        # Pole do wpisywania tekstu (0,0) do (1,1)
        self.text_input = QTextEdit()
        self.text_input.setFont(QFont("Arial", 16))
        self.text_input.setPlaceholderText("Pole do wpisania tekstu")
        self.text_input.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 10px;")
        self.text_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.text_input, 0, 0, 2, 2)

        # Pole do wyświetlania tłumaczenia (2,0) do (3,1)
        self.translation_display = QTextEdit()
        self.translation_display.setFont(QFont("Arial", 16))
        self.translation_display.setReadOnly(True)
        self.translation_display.setStyleSheet("background-color: white; border: 1px solid black; border-radius: 10px;")
        self.translation_display.setPlaceholderText("Tutaj pojawi się tłumaczenie...")
        self.translation_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.translation_display, 2, 0, 2, 2)

        # Nagrywanie, odtwarzanie i kasowanie nagrań (4,0) do (4,5)
        # Ikony
        self.record_icon = QIcon("microphone.png")
        self.recorded_audio_icon = QIcon("recording_audio.png")
        self.play_icon = QIcon("play.png")
        self.stop_icon = QIcon("pause.png")
        self.delete_icon = QIcon("trash.png")

        # Przycisk nagrywania (4,0)
        self.record_button = QPushButton()
        self.record_button.setIcon(self.record_icon)
        # self.record_button.setFixedSize(50, 50)
        self.record_button.clicked.connect(self.toggle_recording)
        self.grid_layout.addWidget(self.record_button, 4, 0, 1, 1)

        # Ikona statusu nagrywania (4,1)
        self.recording_status_label = QLabel()
        # self.recording_status_label.setPixmap(self.recorded_audio_icon.pixmap(50, 50))  # Domyślnie ustaw ikonę
        self.grid_layout.addWidget(self.recording_status_label, 4, 1, 1, 1)

        # Przycisk odtwarzania (4,3)
        self.play_button = QPushButton()
        self.play_button.setIcon(self.play_icon)
        # self.play_button.setFixedSize(50, 50)
        self.play_button.clicked.connect(self.toggle_playback)
        self.play_button.setEnabled(False)
        self.grid_layout.addWidget(self.play_button, 4, 3, 1, 1)

        # Przycisk zatrzymywania odtwarzania (4,4)
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.stop_icon)
        # self.stop_button.setFixedSize(50, 50)
        self.stop_button.clicked.connect(self.stop_playback)
        self.stop_button.setEnabled(False)
        self.grid_layout.addWidget(self.stop_button, 4, 4, 1, 1)

        # Przycisk kasowania (4,5)
        self.delete_button = QPushButton()
        self.delete_button.setIcon(self.delete_icon)
        # self.delete_button.setFixedSize(50, 50)
        self.delete_button.clicked.connect(self.delete_audio)
        self.delete_button.setEnabled(False)
        self.grid_layout.addWidget(self.delete_button, 4, 5, 1, 1)

        # Zmienna audio
        self.recording = False
        self.frames = []
        self.stream = None
        self.audio_interface = pyaudio.PyAudio()
        self.output_file = "recording.wav"
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.current_time = 0
        self.playback_thread = None
        self.playback_position = 0  # Pozycja w ramkach

        self.setLayout(self.grid_layout)
        # # Przycisk do nagrywania (4,0)
        # self.record_button = QPushButton("Nagrywanie")
        # self.record_button.setFont(QFont("Arial", 12))
        # self.record_button.setStyleSheet(
        #     "QPushButton {"
        #     "    background-color: lightgreen;"
        #     "    border: 1px solid black;"
        #     "    border-radius: 10px;"
        #     "}"
        #     "QPushButton:hover {"
        #     "    background-color: green;"
        #     "    color: white;"
        #     "}"
        # )
        # self.record_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.grid_layout.addWidget(self.record_button, 4, 0)

        # # Przycisk do odtwarzania (4,1)
        # self.play_button = QPushButton("Odtwarzanie nagrania")
        # self.play_button.setFont(QFont("Arial", 12))
        # self.play_button.setStyleSheet(
        #     "QPushButton {"
        #     "    background-color: lightblue;"
        #     "    border: 1px solid black;"
        #     "    border-radius: 10px;"
        #     "}"
        #     "QPushButton:hover {"
        #     "    background-color: blue;"
        #     "    color: white;"
        #     "}"
        # )
        # self.play_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.grid_layout.addWidget(self.play_button, 4, 1)

        # # Przycisk do kasowania nagrania (4,2)
        # self.delete_button = QPushButton("Kasowanie nagrania")
        # self.delete_button.setFont(QFont("Arial", 12))
        # self.delete_button.setStyleSheet(
        #     "QPushButton {"
        #     "    background-color: lightcoral;"
        #     "    border: 1px solid black;"
        #     "    border-radius: 10px;"
        #     "}"
        #     "QPushButton:hover {"
        #     "    background-color: red;"
        #     "    color: white;"
        #     "}"
        # )
        # self.delete_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.grid_layout.addWidget(self.delete_button, 4, 2)

        # Wybór języka (0,2)
        self.language_selector = QComboBox()
        self.language_selector.setFont(QFont("Arial", 12))
        self.language_selector.addItems([
            "Polski", "Angielski", "Niemiecki", "Francuski", "Hiszpański",
            "Ukraiński", "Rosyjski", "Włoski", "Szwedzki", "Norweski"
        ])
        self.language_selector.setCurrentIndex(0)  # Ustawienie domyślnej wartości na "Polski"
        self.language_selector.setStyleSheet(
            "QComboBox {"
            "    background-color: white;"
            "    border: 1px solid black;"
            "    border-radius: 15px;"
            "    padding: 5px;"
            "}"
            "QComboBox:hover {"
            "    background-color: lightgray;"
            "}"
        )
        self.language_selector.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.language_selector.currentTextChanged.connect(self.on_language_changed)
        self.grid_layout.addWidget(self.language_selector, 0, 2)

        # Przycisk "Wyczyść" (1,2)
        self.clear_button = QPushButton("Wyczyść")
        self.clear_button.setFont(QFont("Arial", 12))
        self.clear_button.setStyleSheet(
            "QPushButton {"
            "    background-color: lightgray;"
            "    border: 1px solid black;"
            "    border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: gray;"
            "    color: white;"
            "}"
        )
        self.clear_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clear_button.clicked.connect(self.clear_text)
        self.grid_layout.addWidget(self.clear_button, 1, 2)

        # Przycisk "Wyślij" (2,2)
        self.send_button = QPushButton("WYŚLIJ")
        self.send_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.send_button.setStyleSheet(
            "QPushButton {"
            "    border: 1px solid black;"
            "    background-color: orange;"
            "    border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: blue;"
            "    color: white;"
            "}"
        )
        self.send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.send_button.clicked.connect(self.send_translated_command)
        self.grid_layout.addWidget(self.send_button, 2, 2)

        # Gotowe zwroty (0,3) do (4,4)
        phrases = [
            "PODĄŻAJ ZA MNĄ", "STÓJ", "LEĆ W GÓRĘ", "LEĆ W DÓŁ",
            "OBRÓĆ W LEWO", "OBRÓĆ W PRAWO", "START", "LĄDUJ",
            "AUTOMATYCZNY", "MANUALNY"
        ]

        row, col = 0, 3
        for phrase in phrases:
            phrase_button = QPushButton(phrase)
            phrase_button.setFont(QFont("Arial", 10))
            phrase_button.setStyleSheet(
                "QPushButton {"
                "    border: 1px solid black;"
                "    background-color: lightblue;"
                "    border-radius: 10px;"
                "}"
                "QPushButton:hover {"
                "    background-color: blue;"
                "    color: white;"
                "}"
            )
            phrase_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            phrase_button.clicked.connect(lambda _, ph=phrase: self.send_translated_phrase(ph))
            self.grid_layout.addWidget(phrase_button, row, col)
            col += 1
            if col > 4:
                col = 3
                row += 1

        self.setLayout(self.grid_layout)

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        try:
            self.audio_status_label.setPixmap(self.recorded_audio_icon.pixmap(50, 50))  # Ustaw ikonę
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
            self.timer.start(1000)
            self.record_button.setIcon(self.stop_icon)

            def callback():
                try:
                    while self.recording:
                        data = self.stream.read(1024)
                        self.frames.append(data)
                except Exception as e:
                    print(f"Error in recording callback: {e}")

            import threading
            threading.Thread(target=callback, daemon=True).start()
        except Exception as e:
            print(f"Error in start_recording: {e}")

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

            self.audio_status_label.setPixmap(self.recorded_audio_icon.pixmap(50, 50))  # Ikona nagrania
            self.play_button.setEnabled(True)
            self.delete_button.setEnabled(True)
            self.record_button.setIcon(self.record_icon)
        except Exception as e:
            print(f"Error in stop_recording: {e}")

    def toggle_playback(self):
        try:
            if self.playback_thread and self.playback_thread.isRunning():
                self.stop_playback()
            else:
                self.play_button.setEnabled(False)
                self.stop_button.setEnabled(True)

                self.playback_thread = PlaybackThread(self.output_file, start_frame=self.playback_position)
                self.playback_thread.playback_finished.connect(self.on_playback_finished)
                self.playback_thread.start()
        except Exception as e:
            print(f"Error in toggle_playback: {e}")

    def on_playback_finished(self):
        if self.playback_thread:
            self.playback_position = self.playback_thread.current_frame  # Zachowanie pozycji
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.playback_thread = None

    def stop_playback(self):
        try:
            if self.playback_thread and self.playback_thread.isRunning():
                self.playback_thread.stop()
                self.playback_thread.wait()
                self.playback_position = self.playback_thread.current_frame  # Zachowanie pozycji
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(False)
        except Exception as e:
            print(f"Error in stop_playback: {e}")

    def delete_audio(self):
        try:
            self.frames = []
            self.output_file = "recording.wav"
            self.audio_status_label.setPixmap(self.recorded_audio_icon.pixmap(50, 50))  # Ustaw domyślną ikonę
            self.play_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.timer.stop()
            self.current_time = 0
        except Exception as e:
            print(f"Error in delete_audio: {e}")

    def update_time(self):
        try:
            self.current_time += 1
            minutes, seconds = divmod(self.current_time, 60)
            print(f"Czas nagrania: {minutes}:{seconds:02}")
        except Exception as e:
            print(f"Error in update_time: {e}")

    def clear_text(self):
        """Czyści pola tekstowe i tłumaczenia."""
        self.text_input.clear()
        self.translation_display.clear()

    def send_translated_command(self):
        """Wysyła przetłumaczony tekst lub tekst użytkownika na serwer."""
        translated_text = self.translation_display.toPlainText().strip()
        user_text = self.text_input.toPlainText().strip()

        if translated_text:
            self.send_command("AU " + translated_text)
        elif user_text:
            self.send_command("AU " + user_text)
        else:
            QMessageBox.warning(self, "Błąd", "Pole tekstowe i tłumaczenie są puste. Wpisz tekst, aby go wysłać.")

    def send_translated_phrase(self, phrase):
        """Tłumaczy i wysyła wybraną frazę w odpowiednim języku."""
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
            self.send_command("TX " + translation.result)
            print(f"[DEBUG] Wysłano przetłumaczoną frazę ({self.language_selector.currentText()}): {translation.result}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się przetłumaczyć frazy: {e}")

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
            print(f"[DEBUG] Tłumaczenie na {self.language_selector.currentText()}: {translation.result}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się przetłumaczyć tekstu: {e}")

    def send_command(self, command):
        parent = self.parent_window
        if hasattr(parent, 'client_socket') and parent.client_socket:
            try:
                parent.client_socket.sendall(command.encode('utf-8'))
                print(f"Wysłano: {command}")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się wysłać: {e}")
        else:
            QMessageBox.warning(self, "Brak połączenia", "Nie jesteś połączony z serwerem.")
