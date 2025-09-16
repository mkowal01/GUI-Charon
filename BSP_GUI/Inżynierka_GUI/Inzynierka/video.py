# import cv2
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtCore import QTimer, Qt
#
#
# class VideoWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         # Ustawienia podglądu strumienia RTMP
#         self.stream_url = "rtmp://192.168.1.8:1935/live/stream"
#         self.cap = None
#         self.setFixedSize(400, 300)  # Rozmiar widżetu
#
#         # Layout i widżet wyświetlający obraz
#         self.layout = QVBoxLayout()
#         self.video_label = QLabel()
#         self.video_label.setStyleSheet("background-color: black;")
#         self.video_label.setAlignment(Qt.AlignCenter)  # Wyśrodkowanie obrazu
#         self.layout.addWidget(self.video_label)
#         self.setLayout(self.layout)
#
#         # Timer do odświeżania obrazu
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_frame)
#         self.timer.start(30)
#
#         # Inicjalizacja strumienia
#         self.connect_to_stream()
#
#     def connect_to_stream(self):
#         """
#         Próba połączenia ze strumieniem RTMP.
#         """
#         if self.cap is not None:
#             self.cap.release()
#         self.cap = cv2.VideoCapture(self.stream_url)
#         if not self.cap.isOpened():
#             print("Nie udało się połączyć ze strumieniem, ponowna próba za 5 sekund...")
#             QTimer.singleShot(5000, self.connect_to_stream)
#
#     def update_frame(self):
#         """
#         Aktualizacja klatki wideo.
#         """
#         if self.cap.isOpened():
#             ret, frame = self.cap.read()
#             if ret:
#                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 h, w, ch = frame.shape
#                 bytes_per_line = ch * w
#                 image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
#
#                 # Skalowanie obrazu do rozmiaru QLabel z zachowaniem proporcji
#                 scaled_pixmap = QPixmap.fromImage(image).scaled(
#                     self.video_label.width(),
#                     self.video_label.height(),
#                     Qt.KeepAspectRatio  # Zachowanie proporcji
#                 )
#                 self.video_label.setPixmap(scaled_pixmap)
#             else:
#                 print("Strumień utracony, ponowne połączenie...")
#                 self.connect_to_stream()
#
#     def closeEvent(self, event):
#         """
#         Zwolnienie strumienia RTMP po zamknięciu widżetu.
#         """
#         if self.cap is not None and self.cap.isOpened():
#             self.cap.release()
#         event.accept()
import cv2
import socket
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QWheelEvent, QMouseEvent


class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Pobieranie lokalnego adresu IP
        local_ip = self.get_local_ip()

        # Ustawienia podglądu strumienia RTMP
        self.stream_url = f"rtmp://{local_ip}:1935/live/stream"
        self.cap = None
        self.zoom_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.last_mouse_pos = None

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

        # Inicjalizacja strumienia
        self.connect_to_stream()

    def connect_to_stream(self):
        """
        Próba połączenia ze strumieniem RTMP.
        """
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(self.stream_url)
        if not self.cap.isOpened():
            print("Nie udało się połączyć ze strumieniem, ponowna próba za 5 sekund...")
            QTimer.singleShot(5000, self.connect_to_stream)

    def update_frame(self):
        """
        Aktualizacja klatki wideo.
        """
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)

                # Skalowanie obrazu
                scaled_width = int(self.video_label.width() * self.zoom_factor)
                scaled_height = int(self.video_label.height() * self.zoom_factor)
                scaled_pixmap = pixmap.scaled(scaled_width, scaled_height, Qt.KeepAspectRatio)

                # Przesuwanie obrazu
                cropped_pixmap = scaled_pixmap.copy(self.offset_x, self.offset_y,
                                                    min(self.video_label.width(), scaled_pixmap.width()),
                                                    min(self.video_label.height(), scaled_pixmap.height()))

                self.video_label.setPixmap(cropped_pixmap)
            else:
                print("Strumień utracony, ponowne połączenie...")
                self.connect_to_stream()

    def wheelEvent(self, event: QWheelEvent):
        """
        Obsługa powiększania obrazu za pomocą kółka myszy.
        """
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        self.zoom_factor *= factor
        self.update_frame()

    def mousePressEvent(self, event: QMouseEvent):
        """
        Obsługa rozpoczęcia przesuwania obrazu myszą.
        """
        self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Obsługa przesuwania obrazu myszą.
        """
        if self.last_mouse_pos:
            delta = event.pos() - self.last_mouse_pos
            self.offset_x = max(0, self.offset_x - delta.x())
            self.offset_y = max(0, self.offset_y - delta.y())
            self.last_mouse_pos = event.pos()
            self.update_frame()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Reset pozycji myszy po zakończeniu przesuwania.
        """
        self.last_mouse_pos = None

    def closeEvent(self, event):
        """
        Zwolnienie strumienia RTMP po zamknięciu widżetu.
        """
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        event.accept()

    def get_local_ip(self):
        """Pobiera lokalny adres IP urządzenia."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Połączenie z Google DNS (nie wysyła ruchu, tylko sprawdza interfejs)
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception as e:
            print(f"Błąd podczas pobierania IP: {e}")
            return "127.0.0.1"  # Domyślny adres, jeśli nie można uzyskać lokalnego IP