from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class ConnectTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Kliknij, aby nawiązać połączenie."))
        self.connect_button = QPushButton("Połącz")
        layout.addWidget(self.connect_button)

        self.setLayout(layout)
