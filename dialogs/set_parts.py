from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QMessageBox

from manage_database.database import database

class PartDialog(QDialog):
    def __init__(self, parent, part_id, part_description):
        super().__init__(parent)
        self.setWindowTitle("Ievadīt Vērtību")
        self.setFixedSize(400, 150)

        self.part_id = part_id
        self.part_description = part_description

        message = f'Ievadiet {self.part_description} gabalu skaitu:'

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
        self.confirm_button.clicked.connect(lambda: self.change_part(self.part_id, self.parent().main_window.series_index))
        self.confirm_button.setObjectName("ok")
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setObjectName("cancel")
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def change_part(self, part, series_id):
        new_value = self.input.text()

        try:
            new_value = float(new_value.replace(',', '.'))
            if new_value < 0:
                raise ValueError("Vērtība nedrīkst būt mazāka par 0!")
        except ValueError:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, ievadiet derīgu skaitli, kas nav mazāks par 0.")
            return

        database.set_part(part, series_id, new_value)
        self.close()