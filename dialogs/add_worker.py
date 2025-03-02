from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

from manage_database.database import database

class AddWorkerDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Pievienot darbinieku")
        self.setFixedSize(520, 320)

        layout = QVBoxLayout()

        self.name_description = QLabel("Lūdzu, ievadiet jaunā darbinieka vārdu un uzvārdu:")
        self.name_description.setObjectName("description")
        layout.addWidget(self.name_description)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Vārds")
        self.name.setObjectName("customInputField")
        layout.addWidget(self.name)

        self.surname = QLineEdit()
        self.surname.setPlaceholderText("Uzvārds")
        self.surname.setObjectName("customInputField")
        layout.addWidget(self.surname)

        layout.addStretch()

        self.efficiency_description = QLabel("Lūdzu, ievadiet jaunā darbinieka efektivitāti (piemēram 1,0):")
        self.efficiency_description.setObjectName("description")
        layout.addWidget(self.efficiency_description)

        self.efficiency = QLineEdit()
        self.efficiency.setPlaceholderText("Efektivitāte")
        self.efficiency.setObjectName("customInputField")
        layout.addWidget(self.efficiency)

        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Pievienot")
        self.add_button.clicked.connect(self.add_worker)
        self.add_button.setObjectName("ok")
        buttons_layout.addWidget(self.add_button)

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setObjectName("cancel")
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.name.hasFocus():
                self.surname.setFocus()
            elif self.surname.hasFocus():
                self.efficiency.setFocus()
            elif self.efficiency.hasFocus():
                self.add_button.click()
        else:
            super().keyPressEvent(event)

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
            database.add_series_worker(self.parent().main_window.series_index, name, surname, efficiency)
            self.close()
        else:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, aizpildiet visus ievades laukus.")