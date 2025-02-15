from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QMessageBox

from manage_database.database import database

class CoefficientDialog(QDialog):
    def __init__(self, parent, id, description, value):
        super().__init__(parent)
        self.setWindowTitle("Mainīt Vērtību")
        self.id = id
        self.description = description
        self.value = value

        message = f"Mainīt {description} pašreizējo {value} vērtību uz jauno:"

        layout = QVBoxLayout()

        self.label = QLabel(message)
        self.label.setObjectName("description")
        layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setObjectName("customInputField")
        self.input.setPlaceholderText("Jaunā vērtība")
        layout.addWidget(self.input)

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setObjectName("cancel")
        button_layout.addWidget(self.cancel_button)

        self.confirm_button = QPushButton("Mainīt")
        self.confirm_button.clicked.connect(lambda: self.change_coefficient(id, self.parent().main_window.series_index))
        self.confirm_button.setObjectName("ok")
        button_layout.addWidget(self.confirm_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def change_coefficient(self, id, series_id):
        new_value = self.input.text()

        try:
            new_value = float(new_value.replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, ievadiet derīgu skaitli.")
            return

        database.set_coefficient(id, series_id, new_value)
        
        self.close()