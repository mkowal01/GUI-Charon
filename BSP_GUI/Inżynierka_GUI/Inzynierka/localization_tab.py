from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class LocalizationTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Funkcja lokalizacji będzie dostępna w przyszłości."))
        self.setLayout(layout)
