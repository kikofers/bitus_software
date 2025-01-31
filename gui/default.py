from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QAbstractItemView, QSizePolicy
from PyQt5.QtCore import Qt

from manage_db.db_operations import database

class DefaultPage(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        main_layout = QVBoxLayout()
        label = QLabel("Sērijas Pārvaldīšana")
        label.setObjectName("mainLabel")
        main_layout.addWidget(label, alignment=Qt.AlignCenter)



        upper_button_layout = QHBoxLayout()
        
        self.series_label = QLabel()
        self.series_label.setObjectName("mainLabel")
        upper_button_layout.addWidget(self.series_label)

        self.previous_series_button = QPushButton("Iepriekšējā sērija")
        #self.previous_series_button.clicked.connect(self.previous_series)
        self.previous_series_button.setObjectName("navButton")
        upper_button_layout.addWidget(self.previous_series_button)

        self.next_series_button = QPushButton("Nākamā sērija")
        #self.next_series_button.clicked.connect(self.next_series)
        self.next_series_button.setObjectName("navButton")
        upper_button_layout.addWidget(self.next_series_button)

        self.latest_series_button = QPushButton("Jaunākā sērija")
        #self.latest_series_button.clicked.connect(self.latest_series)
        self.latest_series_button.setObjectName("latestSeriesButton")
        upper_button_layout.addWidget(self.latest_series_button)

        self.new_series_button = QPushButton("Jauna sērija")
        self.new_series_button.clicked.connect(self.create_new_series)
        self.new_series_button.setObjectName("newSeriesButton")
        upper_button_layout.addWidget(self.new_series_button)

        self.settings_button = QPushButton("Iestatījumi")
        #self.settings_button.clicked.connect(self.settings)
        self.settings_button.setObjectName("settingsButton")
        upper_button_layout.addWidget(self.settings_button)

        main_layout.addLayout(upper_button_layout)



        lower_layout = QHBoxLayout()

        position_layout = QVBoxLayout()
        self.position_label = QLabel("Pozīcijas")
        self.position_label.setObjectName("secondaryLabel")
        self.position_label.setAlignment(Qt.AlignCenter)

        self.position_table = QTableWidget()
        self.create_table(self.position_table, ["Pozīcija", "Gabalu Skaits", "Mainīt Skaitu"])

        position_layout.addWidget(self.position_label)
        position_layout.addWidget(self.position_table)
        lower_layout.addLayout(position_layout)

        workers_layout = QVBoxLayout()
        self.workers_label = QLabel("Sērijas Darbinieki")
        self.workers_label.setObjectName("secondaryLabel")
        self.workers_label.setAlignment(Qt.AlignCenter)

        self.workers_table = QTableWidget()
        self.create_table(self.workers_table, ["Darbinieks", "Efektivitāte", "Strādās Šajā Sērijā"])

        workers_layout.addWidget(self.workers_label)
        workers_layout.addWidget(self.workers_table)
        lower_layout.addLayout(workers_layout)



        lower_layout_buttons = QVBoxLayout()

        self.button_label = QLabel("Sērijas Darbības")
        self.button_label.setObjectName("secondaryLabel")
        self.button_label.setAlignment(Qt.AlignCenter)
        lower_layout_buttons.addWidget(self.button_label, alignment=Qt.AlignTop)

        self.add_worker_button = QPushButton("Pievienot Darbinieku")
        #self.add_worker_button.clicked.connect(self.add_worker)
        self.add_worker_button.setObjectName("addButton")
        lower_layout_buttons.addWidget(self.add_worker_button, alignment=Qt.AlignTop)

        self.remove_worker_button = QPushButton("Noņemt Darbinieku")
        #self.remove_worker_button.clicked.connect(self.remove_worker)
        self.remove_worker_button.setObjectName("removeButton")
        lower_layout_buttons.addWidget(self.remove_worker_button, alignment=Qt.AlignTop)

        self.modify_worker_efficiency_button = QPushButton("Mainīt Darbinieka Efektivitāti")
        #self.modify_worker_efficiency_button.clicked.connect(self.modify_worker_efficiency)
        self.modify_worker_efficiency_button.setObjectName("modifyButton")
        lower_layout_buttons.addWidget(self.modify_worker_efficiency_button, alignment=Qt.AlignTop)

        # TODO: Add labels which will display some of the coefficients stored in the database.
        
        lower_layout.addLayout(lower_layout_buttons)

        main_layout.addLayout(lower_layout)

        self.setLayout(main_layout)

        self.update_page()

    def create_new_series(self):
        self.main_window.series_index = database.get_last_series_id()
        database.create_series()
        self.update_page()

    def update_page(self):
        self.series_label_color()
        self.populate_position_table()
        self.populate_worker_table()

    def populate_position_table(self):
        series_id = self.main_window.series_index

        positions = database.get_positions(series_id)
        if positions is None:
            return

        for row, (position, count) in enumerate(positions.items()):
            if position == 'series_id':
                continue

            position_item = QTableWidgetItem(position)
            count_item = QTableWidgetItem(str(count))

            button_layout = QHBoxLayout()
            increase_button = QPushButton("+")
            decrease_button = QPushButton("-")
            reset_button = QPushButton("Reset")

            button_layout.addWidget(increase_button)
            button_layout.addWidget(decrease_button)
            button_layout.addWidget(reset_button)

            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            self.position_table.setItem(row, 0, position_item)
            self.position_table.setItem(row, 1, count_item)
            self.position_table.setCellWidget(row, 2, button_widget)

    def populate_worker_table(self):
        workers = database.get_series_workers(self.main_window.series_index)
        if workers is None:
            return
        
        self.workers_table.setRowCount(len(workers))

        for row, worker in enumerate(workers):
            name_item = QTableWidgetItem(f"{worker['name']} {worker['surname']}")
            efficiency_item = QTableWidgetItem(str(worker['efficiency']))
            button_item = QPushButton("Strādā" if worker['is_working'] else "Nestrādā")

            self.workers_table.setItem(row, 0, name_item)
            self.workers_table.setItem(row, 1, efficiency_item)
            self.workers_table.setCellWidget(row, 2, button_item)

    def series_label_color(self):
        colors = ["black", "blue", "green", "red"]
        selected_color = colors[(self.main_window.series_index - 1) % 4] if self.main_window.series_index else "orange"
        self.series_label.setText(f"Sērija {self.main_window.series_index if self.main_window.series_index else 'Nav'}")
        self.series_label.setStyleSheet(f"color: {selected_color};")
        self.series_label.show()

    # Helper function to create the two tables and keep the code clean.
    def create_table(self, table, headers):
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
