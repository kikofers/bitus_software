from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QLineEdit, QMessageBox
from manage_database.database import database

class EditWorkerEfficiencyDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Rediģēt darbinieka efektivitāti")
        self.setFixedSize(600, 800)

        layout = QVBoxLayout()

        self.label = QLabel("Izvēlieties darbinieku, kuram vēlaties mainīt efektivitāti:")
        layout.addWidget(self.label)

        self.worker_list = QListWidget()
        self.worker_list.setSelectionMode(QListWidget.SingleSelection)
        self.worker_list.setObjectName("edit")
        self.worker_id_map = {}
        self.populate_worker_list()
        layout.addWidget(self.worker_list)

        self.efficiency_input = QLineEdit()
        self.efficiency_input.setPlaceholderText("Jaunā efektivitāte")
        self.efficiency_input.setObjectName("customInputField")
        layout.addWidget(self.efficiency_input)

        buttons_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setObjectName("cancel")
        buttons_layout.addWidget(self.cancel_button)

        self.save_button = QPushButton("Saglabāt")
        self.save_button.clicked.connect(self.save_efficiency)
        self.save_button.setObjectName("ok")
        buttons_layout.addWidget(self.save_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def populate_worker_list(self):
        workers = database.get_series_workers(self.parent().main_window.series_index)
        for worker in workers.values():
            item_text = f"{worker['name']} {worker['surname']}"
            self.worker_list.addItem(item_text)
            self.worker_id_map[item_text] = worker['worker_id']

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
            new_efficiency = float(new_efficiency.replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, ievadiet derīgu skaitli efektivitātei.")
            return
        
        worker_id = self.worker_id_map[selected_items[0].text()]
        database.edit_worker(worker_id, new_efficiency)

        self.close()