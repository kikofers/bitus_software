from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

from manage_database.database import database

class AddWorkerDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Pievienot darbinieku")
        self.setGeometry(0, 0, 400, 200)

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Vārds")
        layout.addWidget(self.name)

        self.surname = QLineEdit()
        self.surname.setPlaceholderText("Uzvārds")
        layout.addWidget(self.surname)

        self.efficiency = QLineEdit()
        self.efficiency.setPlaceholderText("Efektivitāte")
        layout.addWidget(self.efficiency)

        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Pievienot")
        self.add_button.clicked.connect(self.add_worker)
        buttons_layout.addWidget(self.add_button)

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def add_worker(self):
        name = self.name.text()
        surname = self.surname.text()
        efficiency = self.efficiency.text()

        if name and surname and efficiency:
            database.add_series_worker(self.parent().main_window.series_index, name, surname, efficiency)
            self.parent().update_page()
            self.close()
        else:
            print("Kļūda! Lūdzu, aizpildiet visus laukus!")