from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt

class ManualTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Tworzenie głównego layoutu
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Tworzenie sekcji scrollowanej
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f0f0f0;
            }
        """)

        # Widget do scrollowania
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(10)

        # Dodanie instrukcji w formie etykiet
        sections = [
            ("**Instrukcja obsługi aplikacji \"INŻYNIERKA - KOWAL&WIŚNIA\"**", True),
            ("\n---\n", False),
            ("### Wprowadzenie", True),
            ("\"INŻYNIERKA - KOWAL&WIŚNIA\" to zaawansowana aplikacja służąca do łączenia się z komputerem pokładowym za pomocą technologii LoRa, WiFi, Ethernet lub Socket. Umożliwia zarządzanie modułem panelu LED, modułem głośnika oraz obsługę GPS (w zakładce Localization). Intuicyjny interfejs aplikacji pozwala na łatwe sterowanie i komunikację z urządzeniem.", False),
            ("### Wymagania systemowe", True),
            ("#### Sprzętowe:", True),
            ("- Komputer z procesorem Intel/AMD o minimalnej częstotliwości 2 GHz.\n- Co najmniej 4 GB pamięci RAM (zalecane 8 GB).\n- Moduł LoRa kompatybilny z komputerem pokładowym.", False),
            ("#### Wymagania programowe", True),
            ("- System operacyjny: Windows 10/11, macOS 10.15 lub nowszy, Linux z obsługą środowiska Python 3.\n- Python w wersji 3.9 lub wyższej.\n- Zainstalowane biblioteki:\n  - PyQt5\n  - TranslatePy\n  - PyAudio\n  - Inne wymienione w pliku `requirements.txt`.\n- Połączenie z internetem wymagane do tłumaczeń i aktualizacji.", False),
            ("### Uruchamianie aplikacji", True),
            ("1. Uruchom aplikację z zakładki startowej Twojego systemu operacyjnego lub za pomocą pliku wykonywalnego, jeśli aplikacja została wcześniej zainstalowana.\n   - W przypadku braku instalacji: skorzystaj z przygotowanego środowiska Python.\n2. Otwórz aplikację `main.py`, korzystając z terminala, wpisując:\n   ```bash\n   python main.py\n   ```\n3. Po uruchomieniu aplikacji zobaczysz ekran powitalny z dostępem do wszystkich zakładek i funkcji. Postępuj zgodnie z wyświetlanymi instrukcjami.\n4. Aplikacja jest gotowa do użycia po skonfigurowaniu połączenia w zakładce \"POŁĄCZ\".", False),
            ("### Połączenia i konfiguracja", True),
            ("1. Przejdź do zakładki \"POŁĄCZ\".\n2. Wybierz typ połączenia:\n   - **LoRa:** Port COM, prędkość transmisji.\n   - **WiFi:** Adres IP, port.\n   - **Ethernet:** Adres IP, port.\n   - **Socket:** Adres IP, port.\n3. Wprowadź wymagane dane w zależności od wybranego typu połączenia.\n4. Kliknij przycisk \"Zatwierdź\", aby ustanowić połączenie.\n5. Po nawiązaniu połączenia możesz wysyłać komendy i dane do komputera pokładowego.", False),
            ("### Funkcjonalności aplikacji", True),
            ("#### 1. **Zakładka TEXT**", True),
            ("Zakładka umożliwia tłumaczenie tekstu i wysyłanie go jako komendy do komputera pokładowego.\n- **Pole tekstowe:** Wpisz tekst do tłumaczenia.\n- **Lista wyboru języka:** Wybierz język docelowy z listy rozwijanej.\n- **Pole tłumaczenia:** Wyświetla wynik tłumaczenia w wybranym języku.\n- **Przycisk \"WYŚLIJ\":** Wysyła przetłumaczoną komendę do komputera pokładowego.\n- **Przycisk \"Wyczyść\":** Czyści wszystkie pola tekstowe.", False),
            ("#### 2. **Zakładka AUDIO**", True),
            ("Zakładka służy do zarządzania nagraniami audio i ich wysyłania do modułu głośnika.\n- **Nagrywanie:**\n  - Przycisk mikrofonu pozwala nagrać dźwięk.\n  - Podczas nagrywania wyświetlany jest czas trwania nagrania.\n- **Odtwarzanie:**\n  - Przycisk \"Play\" pozwala odsłuchać nagranie.\n  - Przycisk \"Stop\" zatrzymuje odtwarzanie.\n- **Kasowanie:**\n  - Przycisk kosza usuwa nagrane dźwięki.\n- **Wysyłanie:**\n  - Po nagraniu możesz wysłać plik audio bezpośrednio do modułu głośnika.", False),
            ("#### 3. **Zakładka LOKALIZACJA**", True),
            ("- Wyświetla bieżące położenie urządzenia na podstawie danych GPS.\n- Informacje o współrzędnych GPS i trasie.", False),
            ("#### 4. **Zakładka INSTRUKCJA OBSŁUGI**", True),
            ("- Wyświetla aktualną instrukcję obsługi aplikacji.\n- Intuicyjny układ siatki z przyciskami umożliwiający szybkie wywołanie funkcji.", False),
            ("#### 5. **Zakładka O NAS**", True),
            ("- Informacje o zespole projektowym i podziękowania.", False),
            ("### Wskazówki użytkowania", True),
            ("- Zawsze sprawdzaj poprawność wprowadzonych danych przed zatwierdzeniem połączenia.\n- Użyj przycisku \"Rozłącz\", aby bezpiecznie zakończyć sesję.\n- Przechowuj pliki audio w bezpiecznej lokalizacji, aby unikać ich utraty.\n- Regularnie aktualizuj oprogramowanie, aby korzystać z najnowszych funkcji.", False),
            ("### Rozwiązywanie problemów", True),
            ("- **Brak połączenia:** Sprawdź poprawność portu COM, adresu IP lub prędkości transmisji w zależności od wybranego typu połączenia.\n- **Problemy z tłumaczeniem:** Upewnij się, że masz połączenie z internetem.\n- **Problemy z dźwiękiem:** Sprawdź mikrofon i głośniki urządzenia.", False),
            ("### Kontakt", True),
            ("W przypadku pytań lub problemów skontaktuj się z zespołem wsparcia technicznego:\n- E-mail: support@inzynierka.com\n- Telefon: +48 123 456 789", False)
        ]

        for text, is_header in sections:
            label = QLabel(text)
            label.setWordWrap(True)
            if is_header:
                label.setStyleSheet("font-weight: bold; font-size: 16px;")
            else:
                label.setStyleSheet("font-size: 14px;")
            scroll_layout.addWidget(label)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)

        # Dodanie sekcji do głównego layoutu
        layout.addWidget(scroll_area)
        self.setLayout(layout)
