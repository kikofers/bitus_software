from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QMessageBox

from manage_database.database import database

class PriceDialog(QDialog):
    def __init__(self, parent, price_id, description):
        super().__init__(parent)
        self.setWindowTitle("Ievadīt Vērtību")
        self.setFixedSize(650, 150)

        self.price_id = price_id
        self.description = description

        message = f'Ievadiet "{self.description}" iecirknim gabalu skaitu:'

        layout = QVBoxLayout()

        self.label = QLabel(message)
        self.label.setObjectName("description")
        layout.addWidget(self.label)

        self.input = QLineEdit()
        self.input.setObjectName("customInputField")
        self.input.setPlaceholderText("Gabalu skaits")
        layout.addWidget(self.input)

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setObjectName("cancel")
        button_layout.addWidget(self.cancel_button)

        self.confirm_button = QPushButton("Ievadīt")
        self.confirm_button.clicked.connect(lambda: self.change_price(self.price_id))
        self.confirm_button.setObjectName("ok")
        button_layout.addWidget(self.confirm_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def change_price(self, price_id):
        new_value = self.input.text()

        try:
            new_value = float(new_value.replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, ievadiet derīgu skaitli.")
            return

        database.set_price_count(new_value, price_id)
        self.close()