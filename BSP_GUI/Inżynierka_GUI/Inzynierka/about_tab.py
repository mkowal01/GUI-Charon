from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Program stworzony przez inż. Macieja Kowala i inż. Jakuba Wiśniewskiego."))
        self.setLayout(layout)
