from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox, QAbstractItemView
from manage_database.database import database

class DeleteWorkerDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Dzēst darbinieku")
        self.setFixedSize(600, 800)

        layout = QVBoxLayout()

        self.label = QLabel("Izvēlieties darbinieku(-us), kurus vēlaties dzēst:")
        layout.addWidget(self.label)

        self.worker_list = QListWidget()
        self.worker_list.setSelectionMode(QListWidget.MultiSelection)
        self.worker_list.setObjectName("delete")
        self.worker_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.worker_list.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.worker_id_map = {}
        self.populate_worker_list()
        layout.addWidget(self.worker_list)

        buttons_layout = QHBoxLayout()

        self.delete_button = QPushButton("Dzēst")
        self.delete_button.clicked.connect(self.delete_selected_workers)
        self.delete_button.setObjectName("delete")
        buttons_layout.addWidget(self.delete_button)

        self.cancel_button = QPushButton("Atcelt")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setObjectName("cancel")
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def populate_worker_list(self):
        workers = database.get_series_workers(self.parent().main_window.series_index)
        for worker in workers.values():
            item_text = f"{worker['name']} {worker['surname']}"
            self.worker_list.addItem(item_text)
            self.worker_id_map[item_text] = worker['worker_id']

    def delete_selected_workers(self):
        selected_items = self.worker_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Brīdinājums", "Lūdzu, izvēlieties vismaz vienu darbinieku, lai dzēstu.")
            return

        for item in selected_items:
            worker_id = self.worker_id_map[item.text()]
            database.delete_worker(worker_id)

        self.close()