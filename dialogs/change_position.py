from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QMessageBox

from manage_database.database import database

class PositionDialog(QDialog):
    def __init__(self, parent, position):
        super().__init__(parent)
        self.setWindowTitle("Ievadīt Vērtību")
        self.setFixedSize(400, 150)

        self.position = position

        message = f"Ievadiet {self.position}. pozīcijai gabalu skaitu:"

        layout = QVBoxLayout()

        self.label = QLabel(message)
        self.label.setObjectName("description")
        layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setObjectName("customInputField")
        self.input.setPlaceholderText("Gabalu skaits")
        layout.addWidget(self.input)

        button_layout = QHBoxLayout()

        self.confirm_button = QPushButton("Ievadīt")
        self.confirm_button.clicked.connect(lambda: self.change_position(self.position, self.parent().main_window.series_index))
        self.confirm_button.setObjectName("ok")
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setObjectName("cancel")
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def change_position(self, position, series_id):
        new_value = self.input.text()

        try:
            new_value = float(new_value.replace(',', '.'))
            if new_value < 0:
                raise ValueError("Vērtība nedrīkst būt mazāka par 0!")
        except ValueError as e:
            QMessageBox.warning(self, "Brīdinājums", str(e))
            return

        database.set_position(position, series_id, new_value)
        self.close()