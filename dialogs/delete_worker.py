from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox
from manage_database.database import database

class DeleteWorkerDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Dzēst darbinieku")
        self.setGeometry(0, 0, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Izvēlieties darbinieku(-us), kurus vēlaties dzēst:")
        layout.addWidget(self.label)

        self.worker_list = QListWidget()
        self.worker_list.setSelectionMode(QListWidget.MultiSelection)
        self.populate_worker_list()
        layout.addWidget(self.worker_list)

        buttons_layout = QHBoxLayout()

        self.delete_button = QPushButton("Dzēst")
        self.delete_button.clicked.connect(self.delete_selected_workers)
        buttons_layout.addWidget(self.delete_button)

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def populate_worker_list(self):
        workers = database.get_series_workers(self.parent().main_window.series_index)
        for worker in workers.values():
            self.worker_list.addItem(f"{worker['name']} {worker['surname']} (ID: {worker['worker_id']})")

    def delete_selected_workers(self):
        selected_items = self.worker_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, izvēlieties vismaz vienu darbinieku, lai dzēstu.")
            return

        for item in selected_items:
            worker_id = int(item.text().split("(ID: ")[1].split(")")[0])
            database.delete_worker(worker_id)

        self.parent().update_page()
        self.close()