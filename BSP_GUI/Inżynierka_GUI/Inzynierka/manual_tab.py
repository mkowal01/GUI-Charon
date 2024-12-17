from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ManualTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Instrukcja obsługi programu."))
        self.setLayout(layout)
