from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

from manage_database.database import database

class AddWorkerDialog(QDialog):
    def __init__(self, series_id):
        self.setWindowTitle("Pievienot darbinieku")
        self.setFixedSize(450, 250)
        self.series_id = series_id

        layout = QVBoxLayout()

        self.description = QLabel("Lūdzu, ievadiet jaunā darbinieka datus:")
        self.description.setObjectName("description")
        layout.addWidget(self.description)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Vārds")
        self.name.setObjectName("customInputField")
        layout.addWidget(self.name)

        self.surname = QLineEdit()
        self.surname.setPlaceholderText("Uzvārds")
        self.surname.setObjectName("customInputField")
        layout.addWidget(self.surname)

        self.efficiency = QLineEdit()
        self.efficiency.setPlaceholderText("Efektivitāte")
        self.efficiency.setObjectName("customInputField")
        layout.addWidget(self.efficiency)

        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Pievienot")
        self.add_button.clicked.connect(self.add_worker)
        self.add_button.setObjectName("OK")
        buttons_layout.addWidget(self.add_button)

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setObjectName("cancel")
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def add_worker(self):
        name = self.name.text()
        surname = self.surname.text()
        efficiency = self.efficiency.text()

        try:
            efficiency = float(efficiency.replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, ievadiet derīgu skaitli efektivitātei.")
            return

        if name and surname and efficiency:
            database.add_series_worker(self.series_id, name, surname, efficiency)
            self.close()
        else:
            print("Kļūda! Lūdzu, aizpildiet visus laukus!")