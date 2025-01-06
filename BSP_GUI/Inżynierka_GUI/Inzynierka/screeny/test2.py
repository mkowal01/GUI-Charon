import sys
import wave
import pyaudio
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

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

class AudioRecorderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio Recorder")
        self.setGeometry(100, 100, 400, 150)
        self.setStyleSheet("background-color: #333; color: white;")

        # UI Layout
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)  # Zmniejsz odstępy między przyciskami

        # Icons (replace with actual paths to your icons)
        self.record_icon = QIcon("microphone.png")
        self.recorded_audio_icon = QIcon("recording_audio.png")
        self.play_icon = QIcon("play.png")
        self.stop_icon = QIcon("pause.png")
        self.delete_icon = QIcon("trash.png")

        # Buttons and Label
        self.record_button = QPushButton()
        self.record_button.setIcon(self.record_icon)
        self.record_button.setFixedSize(50, 50)
        self.record_button.clicked.connect(self.toggle_recording)
        self.layout.addWidget(self.record_button)

        # Etykieta statusu audio (z napisem zamiast ikony)
        self.audio_status_label = QLabel("Brak nagrania")
        self.audio_status_label.setFont(QFont("Arial", 14))
        self.audio_status_label.setAlignment(Qt.AlignCenter)
        self.audio_status_label.setStyleSheet(
            "color: black; background-color: #f0f0f0; padding: 10px; border-radius: 10px;")
        self.audio_layout.addWidget(self.audio_status_label)

        self.play_button = QPushButton()
        self.play_button.setIcon(self.play_icon)
        self.play_button.setFixedSize(50, 50)
        self.play_button.clicked.connect(self.toggle_playback)
        self.play_button.setEnabled(False)
        self.layout.addWidget(self.play_button)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.stop_icon)
        self.stop_button.setFixedSize(50, 50)
        self.stop_button.clicked.connect(self.stop_playback)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        self.time_label = QLabel("0:00")
        self.time_label.setStyleSheet("color: white;")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_label)

        self.delete_button = QPushButton()
        self.delete_button.setIcon(self.delete_icon)
        self.delete_button.setFixedSize(50, 50)
        self.delete_button.clicked.connect(self.delete_audio)
        self.delete_button.setEnabled(False)
        self.layout.addWidget(self.delete_button)

        # Audio variables
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

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        try:
            self.audio_status_label.setText("Nagrywanie...")  # Ustaw napis
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

            self.audio_status_label.setText("Nagranie zapisane")  # Zmień napis
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
                self.audio_status_label.setText("Odtwarzanie...")  # Zmień napis

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
        self.audio_status_label.setText("Odtwarzanie zakończone")  # Zmień napis
        self.playback_thread = None

    def stop_playback(self):
        try:
            if self.playback_thread and self.playback_thread.isRunning():
                self.playback_thread.stop()
                self.playback_thread.wait()
                self.play

    def delete_audio(self):
        try:
            self.frames = []
            self.output_file = "recording.wav"
            self.audio_status_label.setPixmap(self.recorded_audio_icon.pixmap(50, 50))  # Ustaw domyślną ikonę
            self.play_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.time_label.setText("0:00")
            self.playback_position = 0
        except Exception as e:
            print(f"Error in delete_audio: {e}")

    def update_time(self):
        try:
            self.current_time += 1
            minutes, seconds = divmod(self.current_time, 60)
            self.time_label.setText(f"{minutes}:{seconds:02}")
        except Exception as e:
            print(f"Error in update_time: {e}")

    def closeEvent(self, event):
        try:
            if self.playback_thread and self.playback_thread.isRunning():
                self.playback_thread.stop()
                self.playback_thread.wait()
            self.audio_interface.terminate()
            event.accept()
        except Exception as e:
            print(f"Error in closeEvent: {e}")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        recorder = AudioRecorderApp()
        recorder.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error in main: {e}")
