from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QSizePolicy, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QUrl, QTimer, QThread, pyqtSignal
import folium
import os
import re
from Debuger import debug_print
from geopy.distance import geodesic
from datetime import datetime

class ResponseThread(QThread):
    response_received = pyqtSignal(str)

    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.running = True
        debug_print("ResponseThread", "Inicjalizacja wątku odbierania odpowiedzi")

    def run(self):
        while self.running:
            try:
                data = self.connection.recv(1024)
                if not data:
                    debug_print("ResponseThread", "Brak danych, zakończenie wątku")
                    break
                message = data.decode('utf-8').strip()
                debug_print("ResponseThread", f"Odebrano wiadomość: {message}")
                self.response_received.emit(message)
            except Exception as e:
                debug_print("ResponseThread", f"Błąd podczas odbierania danych: {e}")
                break

    def stop(self):
        debug_print("ResponseThread", "Zatrzymanie wątku odbierania odpowiedzi")
        self.running = False

class LocalizationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        debug_print("localization_tab", "Inicjalizacja LocalizationTab")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_logs_from_source)
        # Inicjalizacja zmiennych
        self.response_thread = None
        self.previous_coordinates = None
        self.previous_time = None
        self.gps_positions = []  # Dodanie brakującej listy gps_positions

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        for i in range(7):
            self.grid_layout.setRowStretch(i, 1)
        for j in range(7):
            self.grid_layout.setColumnStretch(j, 1)

        self.map_view = QWebEngineView()
        self.map_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.map_file = os.path.join(os.getcwd(), "map.html")
        debug_print("localization_tab", f"Ścieżka pliku mapy: {self.map_file}")
        self.grid_layout.addWidget(self.map_view, 0, 0, 4, 6)

        self.logs_widget = QTextEdit()
        self.logs_widget.setReadOnly(True)
        self.logs_widget.setFont(QFont("Arial", 10))
        self.logs_widget.setPlaceholderText("Logi będą wyświetlane tutaj...")
        self.logs_widget.setStyleSheet(
            "background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
        self.logs_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout.addWidget(self.logs_widget, 4, 0, 3, 6)

        button_size = QSizePolicy.Expanding
        button_style = (
            "QPushButton {"
            "    background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #6a5f31; color: black;"
            "}"
        )

        self.start_button = QPushButton("Start")
        self.start_button.setSizePolicy(button_size, button_size)
        self.start_button.setStyleSheet(button_style)
        self.start_button.clicked.connect(self.handle_start_button)
        self.grid_layout.addWidget(self.start_button, 0, 6, 1, 1)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setSizePolicy(button_size, button_size)
        self.stop_button.setStyleSheet(button_style)
        self.stop_button.clicked.connect(self.stop_response_thread)
        self.grid_layout.addWidget(self.stop_button, 1, 6, 1, 1)

        self.longitude_input = QLineEdit()
        self.longitude_input.setPlaceholderText("Długość geograficzna")
        self.longitude_input.setSizePolicy(button_size, button_size)
        self.longitude_input.setStyleSheet(
            "background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
        self.grid_layout.addWidget(self.longitude_input, 2, 6, 1, 1)

        self.latitude_input = QLineEdit()
        self.latitude_input.setPlaceholderText("Szerokość geograficzna")
        self.latitude_input.setSizePolicy(button_size, button_size)
        self.latitude_input.setStyleSheet(
            "background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
        self.grid_layout.addWidget(self.latitude_input, 3, 6, 1, 1)

        self.set_coordinates_button = QPushButton("Wyznacz koordynaty")
        self.set_coordinates_button.setSizePolicy(button_size, button_size)
        self.set_coordinates_button.setStyleSheet(button_style)
        self.set_coordinates_button.clicked.connect(self.update_map)
        self.grid_layout.addWidget(self.set_coordinates_button, 4, 6, 1, 1)

        self.speed_display = QLineEdit()
        self.speed_display.setPlaceholderText("Prędkość")
        self.speed_display.setReadOnly(True)
        self.speed_display.setSizePolicy(button_size, button_size)
        self.speed_display.setStyleSheet(
            "background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
        self.grid_layout.addWidget(self.speed_display, 5, 6, 1, 1)

        self.satellites_display = QLineEdit()
        self.satellites_display.setPlaceholderText("Satelity")
        self.satellites_display.setReadOnly(True)
        self.satellites_display.setSizePolicy(button_size, button_size)
        self.satellites_display.setStyleSheet(
            "background-color: #1E1E1E; color: white; border: 2px solid #6a5f31; border-radius: 10px; padding: 5px;")
        self.grid_layout.addWidget(self.satellites_display, 6, 6, 1, 1)

        self.setLayout(self.grid_layout)
        debug_print("localization_tab", "Zakończono inicjalizację layoutu")

        self.response_thread = None
        self.previous_coordinates = None
        self.previous_time = None

        self.create_map(52.2297, 21.0122)

    def create_map(self, latitude, longitude):
        try:
            debug_print("localization_tab", f"Tworzenie mapy dla współrzędnych: {latitude}, {longitude}")
            self.folium_map = folium.Map(location=[latitude, longitude], zoom_start=15)
            folium.Marker([latitude, longitude], tooltip="Lokalizacja").add_to(self.folium_map)
            self.folium_map.save(self.map_file)
            debug_print("localization_tab", f"Mapa zapisana w {self.map_file}")
            self.map_view.setUrl(QUrl.fromLocalFile(self.map_file))
        except Exception as e:
            debug_print("localization_tab", f"Błąd tworzenia mapy: {e}")
            QMessageBox.critical(self, "Błąd", f"Nie udało się wygenerować mapy: {e}")

    def update_map(self):
        debug_print("localization_tab", f"Rozpoczęcie aktualizacji mapy z pozycjami: {self.gps_positions}")
        try:
            if self.gps_positions:
                folium_map = folium.Map(location=self.gps_positions[-1], zoom_start=15)
                folium.PolyLine(self.gps_positions, color="blue", weight=2.5).add_to(folium_map)
                folium.Marker(self.gps_positions[-1]).add_to(folium_map)
                debug_print("localization_tab", f"Zaktualizowano mapę dla ostatniej pozycji: {self.gps_positions[-1]}")
            else:
                folium_map = folium.Map(location=[52.2297, 21.0122], zoom_start=15)
                debug_print("localization_tab", "Brak pozycji GPS, użyto domyślnych współrzędnych")
            folium_map.save(self.map_file)
            debug_print("localization_tab", f"Mapa zapisana w pliku: {self.map_file}")
            self.map_view.setUrl(QUrl.fromLocalFile(self.map_file))
        except Exception as e:
            debug_print("localization_tab", f"Błąd podczas aktualizacji mapy: {e}")
            QMessageBox.critical(self, "Błąd mapy", f"Nie udało się zaktualizować mapy: {e}")

    def is_connected(self):
        """Sprawdza, czy aplikacja jest połączona z serwerem."""
        debug_print("localization_tab", "Rozpoczęto sprawdzanie połączenia...")

        # Sprawdź, czy parent_window istnieje
        if not self.parent_window:
            debug_print("localization_tab", "Brak parent_window")
            return False

        # Sprawdź, czy parent_window zawiera connect_tab
        if not hasattr(self.parent_window, 'connect_tab'):
            debug_print("localization_tab", "Brak connect_tab w parent_window")
            return False

        connect_tab = self.parent_window.connect_tab

        # Sprawdź, czy connect_tab ma wymagane atrybuty
        if not hasattr(connect_tab, 'connected') or not hasattr(connect_tab, 'connection_type'):
            debug_print("localization_tab", "Brak atrybutów connected lub connection_type w connect_tab")
            return False

        # Sprawdź, czy połączenie jest aktywne
        if not connect_tab.connected:
            debug_print("localization_tab", "Nie jesteś połączony z serwerem")
            return False

        debug_print("localization_tab", "Połączenie z serwerem jest aktywne")
        return True

    def handle_start_button(self):
        """Wysyła polecenie LOC do serwera i nasłuchuje odpowiedzi."""
        if not self.is_connected():
            debug_print("localization_tab", "Połączenie nieaktywne, przerwano wysyłanie.")
            QMessageBox.warning(self, "Brak połączenia", "Musisz najpierw połączyć się z serwerem, aby wysłać komendę.")
            return

        command = "LOC"
        debug_print("localization_tab", f"Przygotowano komendę: {command}")

        try:
            connect_tab = self.parent_window.connect_tab
            connection_type = connect_tab.connection_type.currentText()
            debug_print("localization_tab", f"Typ połączenia: {connection_type}")

            if connection_type == "Socket/WiFi/Ethernet":
                if hasattr(connect_tab, 'sock') and connect_tab.sock:
                    debug_print("localization_tab", "Socket jest aktywny. Próba wysłania komendy...")
                    connect_tab.sock.sendall(command.encode('utf-8'))
                    debug_print("localization_tab", f"Wysłano przez socket: {command}")
                    self.start_response_thread(connect_tab.sock)
                else:
                    debug_print("localization_tab", "Socket nie istnieje lub jest zamknięty.")
                    QMessageBox.warning(self, "Błąd połączenia", "Socket nie jest aktywny.")
            elif connection_type == "LoRa":
                if hasattr(connect_tab, 'serial_conn') and connect_tab.serial_conn:
                    debug_print("localization_tab", "Połączenie LoRa aktywne. Próba wysłania komendy...")
                    connect_tab.serial_conn.write(command.encode('utf-8'))
                    debug_print("localization_tab", f"Wysłano przez LoRa: {command}")
                    self.start_response_thread(connect_tab.serial_conn)
                else:
                    debug_print("localization_tab", "LoRa nie istnieje lub jest zamknięta.")
                    QMessageBox.warning(self, "Błąd połączenia", "LoRa nie jest aktywna.")
            else:
                debug_print("localization_tab", f"Nieobsługiwany typ połączenia: {connection_type}")
                QMessageBox.warning(self, "Błąd połączenia", f"Nieobsługiwany typ połączenia: {connection_type}")
        except Exception as e:
            debug_print("localization_tab", f"Błąd podczas wysyłania: {e}")
            QMessageBox.critical(self, "Błąd wysyłania", f"Nie udało się wysłać: {e}")

    def start_response_thread(self, connection):
        if self.response_thread and self.response_thread.isRunning():
            self.response_thread.stop()
            self.response_thread.wait()

        self.response_thread = ResponseThread(connection)
        self.response_thread.response_received.connect(self.update_logs)
        self.response_thread.start()

    def stop_response_thread(self):
        if self.response_thread and self.response_thread.isRunning():
            self.response_thread.stop()
            self.response_thread.wait()
            self.response_thread = None
        """Wysyła polecenie LOC do serwera i nasłuchuje odpowiedzi."""
        if not self.is_connected():
            debug_print("localization_tab", "Połączenie nieaktywne, przerwano wysyłanie.")
            QMessageBox.warning(self, "Brak połączenia", "Musisz najpierw połączyć się z serwerem, aby wysłać komendę.")
            return

        command = "STOP"
        debug_print("localization_tab", f"Przygotowano komendę: {command}")

        try:
            connect_tab = self.parent_window.connect_tab
            connection_type = connect_tab.connection_type.currentText()
            debug_print("localization_tab", f"Typ połączenia: {connection_type}")

            if connection_type == "Socket/WiFi/Ethernet":
                if hasattr(connect_tab, 'sock') and connect_tab.sock:
                    debug_print("localization_tab", "Socket jest aktywny. Próba wysłania komendy...")
                    connect_tab.sock.sendall(command.encode('utf-8'))
                    debug_print("localization_tab", f"Wysłano przez socket: {command}")
                    self.start_response_thread(connect_tab.sock)
                else:
                    debug_print("localization_tab", "Socket nie istnieje lub jest zamknięty.")
                    QMessageBox.warning(self, "Błąd połączenia", "Socket nie jest aktywny.")
            elif connection_type == "LoRa":
                if hasattr(connect_tab, 'serial_conn') and connect_tab.serial_conn:
                    debug_print("localization_tab", "Połączenie LoRa aktywne. Próba wysłania komendy...")
                    connect_tab.serial_conn.write(command.encode('utf-8'))
                    debug_print("localization_tab", f"Wysłano przez LoRa: {command}")
                    self.start_response_thread(connect_tab.serial_conn)
                else:
                    debug_print("localization_tab", "LoRa nie istnieje lub jest zamknięta.")
                    QMessageBox.warning(self, "Błąd połączenia", "LoRa nie jest aktywna.")
            else:
                debug_print("localization_tab", f"Nieobsługiwany typ połączenia: {connection_type}")
                QMessageBox.warning(self, "Błąd połączenia", f"Nieobsługiwany typ połączenia: {connection_type}")
        except Exception as e:
            debug_print("localization_tab", f"Błąd podczas wysyłania: {e}")
            QMessageBox.critical(self, "Błąd wysyłania", f"Nie udało się wysłać: {e}")

    def update_logs_from_source(self):
        # Example log line (replace with actual data source logic):
        log_line = "Czas: 07:01:28.492 | Pozycja: Szerokość: 51.159929, Długość: 17.137955666666667 | Liczba widocznych satelitów: 02"
        debug_print("localization_tab", f"Aktualizacja logów z przykładowego źródła: {log_line}")
        self.update_logs(log_line)

    def update_logs(self, message):
        debug_print("localization_tab", f"Rozpoczęcie aktualizacji logów: {message}")
        try:
            self.logs_widget.append(message)
            parsed_data = self.parse_log(message)
            if parsed_data:
                latitude, longitude, satellites, timestamp = parsed_data
                debug_print("localization_tab",
                            f"Parsowanie zakończone: Lat: {latitude}, Lon: {longitude}, Sat: {satellites}, Time: {timestamp}")
                self.gps_positions.append((latitude, longitude))
                self.update_map()
                self.update_satellite_widget(satellites)
                self.calculate_speed(latitude, longitude, timestamp)
            else:
                debug_print("localization_tab", "Nie udało się sparsować danych z logu")
        except Exception as e:
            debug_print("localization_tab", f"Błąd podczas aktualizacji logów: {e}")
            QMessageBox.critical(self, "Błąd logów", f"Nie udało się zaktualizować logów: {e}")

    def parse_log(self, log_line):
        debug_print("localization_tab", f"Parsowanie logu: {log_line}")
        try:
            match = re.search(r"Szerokość: ([\d.]+), Długość: ([\d.]+) \| Liczba widocznych satelitów: (\d+)", log_line)
            if match:
                latitude = float(match.group(1))
                longitude = float(match.group(2))
                satellites = int(match.group(3))
                time_match = re.search(r"Czas: ([\d:.]+)", log_line)
                timestamp = time_match.group(1) if time_match else None
                debug_print("localization_tab",
                            f"Parsowanie zakończone - Latitude: {latitude}, Longitude: {longitude}, Satellites: {satellites}, Timestamp: {timestamp}")
                return latitude, longitude, satellites, timestamp
            debug_print("localization_tab", "Nie udało się sparsować logu")
            return None
        except Exception as e:
            debug_print("localization_tab", f"Błąd podczas parsowania logu: {e}")
            return None

    def update_satellite_widget(self, satellites):
        debug_print("localization_tab", f"Aktualizacja liczby satelitów: {satellites}")
        self.satellites_display.setText(str(satellites))

    def calculate_speed(self, latitude, longitude, timestamp):
        debug_print("localization_tab",
                    f"Rozpoczęcie obliczania prędkości dla punktu: {latitude}, {longitude}, czas: {timestamp}")
        try:
            if self.previous_coordinates and self.previous_time:
                current_coordinates = (latitude, longitude)
                distance = geodesic(self.previous_coordinates, current_coordinates).meters
                debug_print("localization_tab", f"Odległość między punktami: {distance} m")
                time_delta = (datetime.strptime(timestamp, "%H:%M:%S.%f") - self.previous_time).total_seconds()
                debug_print("localization_tab", f"Różnica czasu: {time_delta} s")
                if time_delta > 0:
                    speed = distance / time_delta  # m/s
                    debug_print("localization_tab", f"Prędkość obliczona: {speed:.2f} m/s")
                    self.speed_display.setText(f"{speed:.2f} m/s")
                else:
                    debug_print("localization_tab", "Różnica czasu <= 0, prędkość nie została obliczona")
            self.previous_coordinates = (latitude, longitude)
            self.previous_time = datetime.strptime(timestamp, "%H:%M:%S.%f")
        except Exception as e:
            debug_print("localization_tab", f"Błąd podczas obliczania prędkości: {e}")
            QMessageBox.critical(self, "Błąd", f"Nie udało się obliczyć prędkości: {e}")
