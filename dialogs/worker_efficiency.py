from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
from manage_database.database import database

class EditWorkerEfficiencyDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Rediģēt darbinieka efektivitāti")
        self.setGeometry(0, 0, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Izvēlieties darbinieku, kuram vēlaties mainīt efektivitāti:")
        layout.addWidget(self.label)

        self.worker_list = QListWidget()
        self.worker_list.setSelectionMode(QListWidget.SingleSelection)
        self.populate_worker_list()
        layout.addWidget(self.worker_list)

        self.efficiency_input = QLineEdit()
        self.efficiency_input.setPlaceholderText("Jaunā efektivitāte")
        layout.addWidget(self.efficiency_input)

        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Saglabāt")
        self.save_button.clicked.connect(self.save_efficiency)
        buttons_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def populate_worker_list(self):
        workers = database.get_series_workers(self.parent().main_window.series_index)
        for worker in workers.values():
            self.worker_list.addItem(f"{worker['name']} {worker['surname']} (ID: {worker['worker_id']})")

    def save_efficiency(self):
        selected_items = self.worker_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, izvēlieties darbinieku.")
            return

        new_efficiency = self.efficiency_input.text()
        if not new_efficiency:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, ievadiet jauno efektivitāti.")
            return

        try:
            new_efficiency = float(new_efficiency)
        except ValueError:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, ievadiet derīgu skaitli efektivitātei.")
            return

        worker_id = int(selected_items[0].text().split("(ID: ")[1].split(")")[0])
        database.edit_worker(worker_id, new_efficiency)

        self.parent().update_page()
        self.close()