from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class ConfirmationDialog(QDialog):
    def __init__(self, parent, message=""):
        super().__init__(parent)
        self.setWindowTitle("Darbības apstiprinājums")
        self.setFixedSize(400, 100)

        layout = QVBoxLayout()

        self.label = QLabel(message)
        self.label.setObjectName("description")
        layout.addWidget(self.label)

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Nē")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setObjectName("cancel")
        button_layout.addWidget(self.cancel_button)

        self.confirm_button = QPushButton("Jā")
        self.confirm_button.clicked.connect(self.accept)
        self.confirm_button.setObjectName("delete")
        button_layout.addWidget(self.confirm_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)