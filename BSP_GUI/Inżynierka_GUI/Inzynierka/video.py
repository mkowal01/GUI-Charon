import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt


class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Ustawienia podglądu kamery
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Szerokość obrazu
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Wysokość obrazu
        self.setFixedSize(400, 300)  # Rozmiar widżetu

        # Layout i widżet wyświetlający obraz
        self.layout = QVBoxLayout()
        self.video_label = QLabel()
        self.video_label.setStyleSheet("background-color: black;")
        self.video_label.setAlignment(Qt.AlignCenter)  # Wyśrodkowanie obrazu
        self.layout.addWidget(self.video_label)
        self.setLayout(self.layout)

        # Timer do odświeżania obrazu
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        """
        Aktualizacja klatki wideo.
        """
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Skalowanie obrazu do rozmiaru QLabel z zachowaniem proporcji
            scaled_pixmap = QPixmap.fromImage(image).scaled(
                self.video_label.width(),
                self.video_label.height(),
                Qt.KeepAspectRatio  # Zachowanie proporcji
            )
            self.video_label.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        """
        Zwolnienie kamery po zamknięciu widżetu.
        """
        self.cap.release()
        event.accept()
