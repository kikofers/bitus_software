from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QAbstractItemView, QSizePolicy, QInputDialog, QTableView
from PyQt5.QtCore import Qt

from dialogs.add_worker import AddWorkerDialog
from dialogs.confirmation import ConfirmationDialog
from dialogs.delete_worker import DeleteWorkerDialog
from dialogs.worker_efficiency import EditWorkerEfficiencyDialog

from table_view.workers import WorkerTableModel, WorkerButtonDelegate
from table_view.positions import PositionTableModel, PositionButtonDelegate
from table_view.prices import PriceTableModel, PriceButtonDelegate
from table_view.results import ResultsTableModel

from manage_database.database import database

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
        self.series_label.setObjectName("seriesLabel")
        upper_button_layout.addWidget(self.series_label)

        self.previous_series_button = QPushButton("Iepriekšējā sērija")
        self.previous_series_button.clicked.connect(self.previous_series)
        self.previous_series_button.setObjectName("navButton")
        upper_button_layout.addWidget(self.previous_series_button)

        self.next_series_button = QPushButton("Nākamā sērija")
        self.next_series_button.clicked.connect(self.next_series)
        self.next_series_button.setObjectName("navButton")
        upper_button_layout.addWidget(self.next_series_button)

        self.latest_series_button = QPushButton("Jaunākā sērija")
        self.latest_series_button.clicked.connect(self.latest_series)
        self.latest_series_button.setObjectName("navButton")
        upper_button_layout.addWidget(self.latest_series_button)

        self.new_series_button = QPushButton("Jauna sērija")
        self.new_series_button.clicked.connect(self.create_new_series)
        self.new_series_button.setObjectName("newSeriesButton")
        upper_button_layout.addWidget(self.new_series_button)

        main_layout.addLayout(upper_button_layout)



        lower_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        self.position_label = QLabel("Pozīciju Tabula")
        self.position_label.setObjectName("secondaryLabel")
        self.position_label.setAlignment(Qt.AlignCenter)

        self.position_table = QTableView()
        self.create_table(self.position_table, ["Pozīcija", "Gabali", "Mainīt Skaitu"])
<<<<<<< HEAD
        self.position_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.position_table.setColumnWidth(1, 80)
        self.position_table.setColumnWidth(2, 210)
    
=======
        self.position_table.setItemDelegateForColumn(2, PositionButtonDelegate(self))

>>>>>>> main
        self.price_label = QLabel("Cenas Tabula")
        self.price_label.setObjectName("secondaryLabel")
        self.price_label.setAlignment(Qt.AlignCenter)

        self.price_table = QTableView()
        self.create_table(self.price_table, ["Iecirknis", "Cena", "Gabali", "Mainīt Skaitu", "KOPĀ"])
<<<<<<< HEAD
        self.price_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.price_table.setColumnWidth(1, 80)
        self.price_table.setColumnWidth(2, 80)
        self.price_table.setColumnWidth(3, 210)
        self.price_table.setColumnWidth(4, 100)
=======
        self.price_table.setItemDelegateForColumn(3, PriceButtonDelegate(self))
>>>>>>> main

        left_layout.addWidget(self.position_label)
        left_layout.addWidget(self.position_table)
        left_layout.addWidget(self.price_label)
        left_layout.addWidget(self.price_table)

        lower_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        self.workers_label = QLabel("Sērijas Darbinieku Tabula")
        self.workers_label.setObjectName("secondaryLabel")
        self.workers_label.setAlignment(Qt.AlignCenter)

        self.workers_table = QTableView()
        self.create_table(self.workers_table, ["Darbinieks", "Efektivitāte", "Strādās Šajā Sērijā"])
<<<<<<< HEAD
        self.workers_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.workers_table.setColumnWidth(1, 100)
        self.workers_table.setColumnWidth(2, 210)

=======
        self.workers_table.setItemDelegateForColumn(2, WorkerButtonDelegate(self))
        
>>>>>>> main
        self.results_label = QLabel("Sērijas Apkopojums")
        self.results_label.setObjectName("secondaryLabel")
        self.results_label.setAlignment(Qt.AlignCenter)

        self.results_table = QTableView()
        self.create_table(self.results_table, ["Kas", "Cik"])
        self.results_table.horizontalHeader().setVisible(False)
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.results_table.setColumnWidth(1, 210)

        right_layout.addWidget(self.workers_label)
        right_layout.addWidget(self.workers_table)
        right_layout.addWidget(self.results_label)
        right_layout.addWidget(self.results_table)
        lower_layout.addLayout(right_layout)



        lower_layout_buttons = QVBoxLayout()

        self.button_label = QLabel("Sērijas Darbības")
        self.button_label.setObjectName("secondaryLabel")
        self.button_label.setAlignment(Qt.AlignCenter)
        lower_layout_buttons.addWidget(self.button_label, alignment=Qt.AlignTop)

        self.add_worker_button = QPushButton("Pievienot Darbinieku")
        self.add_worker_button.clicked.connect(self.add_worker)
        self.add_worker_button.setObjectName("addButton")
        lower_layout_buttons.addWidget(self.add_worker_button, alignment=Qt.AlignTop)

        self.remove_worker_button = QPushButton("Dzēst Darbinieku")
        self.remove_worker_button.clicked.connect(self.delete_worker)
        self.remove_worker_button.setObjectName("removeButton")
        lower_layout_buttons.addWidget(self.remove_worker_button, alignment=Qt.AlignTop)

        self.modify_worker_efficiency_button = QPushButton("Mainīt Efektivitāti")
        self.modify_worker_efficiency_button.clicked.connect(self.modify_worker_efficiency)
        self.modify_worker_efficiency_button.setObjectName("modifyButton")
        lower_layout_buttons.addWidget(self.modify_worker_efficiency_button, alignment=Qt.AlignTop)

        self.results_button = QPushButton("Sērijas Diagramma")
        self.results_button.clicked.connect(self.go_to_print)
        self.results_button.setObjectName("printButton")
        lower_layout_buttons.addWidget(self.results_button)

        self.settings_button = QPushButton("Koeficientu Iestatījumi")
        self.settings_button.clicked.connect(self.go_to_settings)
        self.settings_button.setObjectName("settingsButton")
        lower_layout_buttons.addWidget(self.settings_button)

        self.reset_positions_button = QPushButton("Notīrīt Pozīcijas")
        self.reset_positions_button.clicked.connect(self.confirm_reset_positions)
        self.reset_positions_button.setObjectName("restartButton")
        lower_layout_buttons.addWidget(self.reset_positions_button)

        self.reset_prices_button = QPushButton("Notīrīt Cenas")
        self.reset_prices_button.clicked.connect(self.confirm_reset_prices)
        self.reset_prices_button.setObjectName("restartButton")
        lower_layout_buttons.addWidget(self.reset_prices_button)

        lower_layout.addLayout(lower_layout_buttons)

        main_layout.addLayout(lower_layout)

        self.setLayout(main_layout)

        self.update_page()



#------ Dialog Functions: ------
    # Add worker dialog.
    def add_worker(self):
        dialog = AddWorkerDialog(self)
        dialog.exec_()

    # Delete worker dialog.
    def delete_worker(self):
        dialog = DeleteWorkerDialog(self)
        dialog.exec_()

    # Modify worker's efficiency dialog.
    def modify_worker_efficiency(self):
        dialog = EditWorkerEfficiencyDialog(self)
        dialog.exec_()

    # Set's the value of a position to the inputed number.
    def set_position_value(self, row_index):
        position, _ = self.position_model.positions[row_index]
        series_id = self.main_window.series_index

        new_value, ok = QInputDialog.getInt(self, "Set Position Value", f"Set new value for {position}:", min=0)
        if ok:
            database.set_position(position, series_id, new_value)

        self.update_position_table()

    # Set's the value of a price to the inputed number.
    def set_price_count(self, row_index):
        price_id = self.price_model.prices[row_index]["price_id"]

        new_value, ok = QInputDialog.getInt(self, "Set Price Count", "Enter new count:", min=0)
        if ok:
            database.set_price_count(price_id, new_value)

        self.update_price_table()
        self.update_page()

    # Confirm the position reset.
    def confirm_reset_positions(self):
        message = "Vai tiešām iestatīt visas pozīciju vērtības uz 0?      "
        dialog = ConfirmationDialog(self, message)
        if dialog.exec_():
            self.reset_positions()

    # Confirm price reset.
    def confirm_reset_prices(self):
        message = "Vai tiešām iestatīt visas cenu gabalu vērtības uz 0?      "
        dialog = ConfirmationDialog(self, message)
        if dialog.exec_():
            self.reset_prices()



#------ Update Functions: ------
    # The main function called when it's necessary to update all contents.
    def update_page(self):
        self.series_label_color()
        self.navigation_button_color()
        self.populate_position_table()
        self.populate_worker_table()
        self.populate_price_table()
        self.populate_results_table()

    # Updates the position table.
    def populate_position_table(self):
        series_id = self.main_window.series_index
        positions = database.get_positions(series_id)
        if positions is None:
            return

        self.position_model = PositionTableModel(list(positions.items()))  # Model needed
        self.position_table.setModel(self.position_model)

<<<<<<< HEAD
        for row, (position, count) in enumerate(positions.items()):
            position_item = QTableWidgetItem(f"Pozīcija nr. {position}")
            count_item = QTableWidgetItem(str(count))
=======
        # Assign button delegate
        self.button_delegate = PositionButtonDelegate(
            self.position_table, self.modify_position_value, self.set_position_value
        )
        self.position_table.setItemDelegateForColumn(2, self.button_delegate)
>>>>>>> main

        self.position_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_position_table(self):
        series_id = self.main_window.series_index
        positions = database.get_positions(series_id)

        if positions is None:
            return

        self.position_model.positions = list(positions.items())  # Update model data
        self.position_model.layoutChanged.emit()  # Notify the view about the update

    def populate_worker_table(self):
        workers = database.get_series_workers(self.main_window.series_index)
        if workers is None:
            return

        self.worker_model = WorkerTableModel(list(workers.values()))
        self.workers_table.setModel(self.worker_model)

<<<<<<< HEAD
        for row, worker in enumerate(workers.values()):
            name_item = QTableWidgetItem(f"{worker['name']} {worker['surname']}")
            efficiency_item = QTableWidgetItem(str(worker['efficiency']))
            button_item = QPushButton("Strādā" if worker['working'] else "Nestrādā")
            button_item.setObjectName("workerStatus")
            button_item.clicked.connect(lambda _, w=worker: self.toggle_worker_status(w['worker_id']))
=======
        # Assign the delegate to the last column (index 2)
        self.button_delegate = WorkerButtonDelegate(self.workers_table, self.toggle_worker_status)
        self.workers_table.setItemDelegateForColumn(2, self.button_delegate)
>>>>>>> main

        # Resize columns
        self.workers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_worker_table(self):
        workers = database.get_series_workers(self.main_window.series_index)

        if workers is None:
            return

        self.worker_model.workers = list(workers.values())  # Update model data
        self.worker_model.layoutChanged.emit()  # Notify the view to refresh

    # Update price table.
    def populate_price_table(self):
        prices = database.get_prices(self.main_window.series_index)
        if prices is None:
            return

        self.price_model = PriceTableModel(list(prices.values()))
        self.price_table.setModel(self.price_model)

<<<<<<< HEAD
        for row, price in enumerate(prices.values()):
            description_item = QTableWidgetItem(price["description"])
            price_item = QTableWidgetItem(f"{price['price']}€")
            count_item = QTableWidgetItem(str(price["count"]))
            total_item = QTableWidgetItem(f"{round(price['price'] * price['count'], 2):.2f}€")
=======
        # Assign delegate for buttons in column 3
        self.button_delegate = PriceButtonDelegate(
            self.price_table, self.modify_price_value, self.set_price_count
        )
        self.price_table.setItemDelegateForColumn(3, self.button_delegate)
>>>>>>> main

        self.price_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_price_table(self):
        prices = database.get_prices(self.main_window.series_index)

        if prices is None:
            return

        self.price_model.prices = list(prices.values())  # Update model data
        self.price_model.layoutChanged.emit()  # Refresh view

    # Updates the results table.
    def populate_results_table(self):
        positions = database.get_positions(self.main_window.series_index)
        coefficients = database.get_coefficients(self.main_window.series_index)
        workers = database.get_series_workers(self.main_window.series_index)

        if not workers:
            return

        position_sum = database.get_sum_positions(self.main_window.series_index)
        price_sum = database.get_sum_prices(self.main_window.series_index)
        
        position_time = 0.0
        for position in positions:
            coefficient_id = position
            if coefficient_id in coefficients:
                position_time += positions[position] * coefficients[coefficient_id]["value"]

        total_efficiency = sum(worker["efficiency"] for worker in workers.values() if worker["working"])

        if total_efficiency == 0:
            results = [
                ("UZMANĪBU!", "Neviens darbinieks nestrādā.")
            ]
        else:
            efficiency_time = position_time / total_efficiency
            series_time = efficiency_time + efficiency_time * coefficients[10]["value"] + efficiency_time * coefficients[11]["value"]

            results = [
                ("Kopējais pozīciju gabalu skaits:", str(position_sum)),
                ("Kopējā vērtība sērijai:", f"{price_sum:.2f}€"),
                ("Kopējais darba laiks (neņemot vērā efektivitāti):", self.to_hours_and_minutes(position_time)),
                ("Sērijas izpildes laiks (ņemot vērā efektivitāti):", self.to_hours_and_minutes(efficiency_time)),
                ("Reālais sērijas izpildes laiks (ņemot vērā visus koeficientus):", self.to_hours_and_minutes(series_time)),
                ("Reālais sērijas izpildes laiks (dienās):", f"{round(series_time / 8, 1)}d"),
            ]

        # If model already exists, update data
        if hasattr(self, 'results_model'):
            self.results_model.update_results(results)
        else:
            self.results_model = ResultsTableModel(results)
            self.results_table.setModel(self.results_model)

        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # Updates series label color.
    def series_label_color(self):
        colors = ["black", "blue", "green", "red"]
        selected_color = colors[(self.main_window.series_index - 1) % 4] if self.main_window.series_index else "orange"
        self.series_label.setText(f"Sērija {self.main_window.series_index if self.main_window.series_index else 'Nav'}")
        self.series_label.setStyleSheet(f"color: {selected_color};")
        self.series_label.show()



#------ Navigation Buttons: ------
    # Create a new series.
    def create_new_series(self):
        database.create_series()
        self.main_window.series_index = database.get_last_series_id()
        self.update_page()

    # Move to the previous series.
    def previous_series(self):
        if self.main_window.series_index and self.main_window.series_index > 1:
            self.main_window.series_index -= 1
            self.update_page()

    # Move to the next series.
    def next_series(self):
        if self.main_window.series_index and self.main_window.series_index < database.get_last_series_id():
            self.main_window.series_index += 1
            self.update_page()
        
    # Move to the latest series.
    def latest_series(self):
        self.main_window.series_index = database.get_last_series_id()
        self.update_page()

    # Controls when certain navigation buttons should be disabled.
    def navigation_button_color(self):
        self.previous_series_button.setEnabled(self.main_window.series_index and self.main_window.series_index > 1)
        self.next_series_button.setEnabled(self.main_window.series_index and self.main_window.series_index < database.get_last_series_id())
        self.latest_series_button.setEnabled(self.main_window.series_index and self.main_window.series_index != database.get_last_series_id())



#------ Other Functions: ------
    # Goes to the print page.
    def go_to_print(self):
        self.main_window.print_page.update_page()
        self.main_window.stack.setCurrentWidget(self.main_window.print_page)

    # Goes to the settings page.
    def go_to_settings(self):
        self.main_window.settings_page.update_page()
        self.main_window.stack.setCurrentWidget(self.main_window.settings_page)

    # Helper function to create the two tables and keep the code clean.
    def create_table(self, table, headers):
<<<<<<< HEAD
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        #table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
=======
        table.setModel(None)  # Reset model
        #table.setHorizontalHeaderLabels(headers)  # No longer needed, handled in the model
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
>>>>>>> main
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
<<<<<<< HEAD
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection)


=======
>>>>>>> main

    def toggle_worker_status(self, row_index):
        worker_id = self.worker_model.workers[row_index]["worker_id"]
        database.toggle_worker_status(worker_id)  # Toggle in DB
        self.update_worker_table()  # Refresh table
        self.update_page()

    # Resetts the values for position table.
    def reset_positions(self):
        database.reset_positions(self.main_window.series_index)
        self.update_page()

    # Resetts the values for price table.
    def reset_prices(self):
        database.reset_prices(self.main_window.series_index)
        self.update_page()

    # Controls the modified position value.
    def modify_position_value(self, row_index, delta):
        position, _ = self.position_model.positions[row_index]  # Get position name
        series_id = self.main_window.series_index

        if delta == 1:
            database.add_one(position, series_id)
        elif delta == -1:
            database.remove_one(position, series_id)

        self.update_position_table()
        self.update_page()

    # Controls the modified price value.
    def modify_price_value(self, row_index, delta):
        price_id = self.price_model.prices[row_index]["price_id"]

        if delta == 1:
            database.add_one_price(price_id)
        elif delta == -1:
            database.remove_one_price(price_id)

        self.update_price_table()
        self.update_page()
    
    # Returns the hours and minutes in a string format.
    def to_hours_and_minutes(self, hours):
        whole_hours = int(hours)
        minutes = int((hours - whole_hours) * 60)
        return f"{whole_hours}h {minutes}m"