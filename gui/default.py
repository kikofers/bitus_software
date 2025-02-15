from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QAbstractItemView, QSizePolicy, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from dialogs.change_price import PriceDialog
from dialogs.add_worker import AddWorkerDialog
from dialogs.change_position import PositionDialog
from dialogs.confirmation import ConfirmationDialog
from dialogs.delete_worker import DeleteWorkerDialog
from dialogs.worker_efficiency import EditWorkerEfficiencyDialog

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
        self.previous_series_button.setObjectName("blueButton")
        upper_button_layout.addWidget(self.previous_series_button)

        self.next_series_button = QPushButton("Nākamā sērija")
        self.next_series_button.clicked.connect(self.next_series)
        self.next_series_button.setObjectName("blueButton")
        upper_button_layout.addWidget(self.next_series_button)

        self.latest_series_button = QPushButton("Jaunākā sērija")
        self.latest_series_button.clicked.connect(self.latest_series)
        self.latest_series_button.setObjectName("blueButton")
        upper_button_layout.addWidget(self.latest_series_button)

        self.new_series_button = QPushButton("Jauna sērija")
        self.new_series_button.clicked.connect(self.create_new_series)
        self.new_series_button.setObjectName("greenButton")
        upper_button_layout.addWidget(self.new_series_button)

        main_layout.addLayout(upper_button_layout)



        lower_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.setObjectName("greyLayout")
        self.position_label = QLabel("Pozīciju Tabula")
        self.position_label.setObjectName("secondaryLabel")
        self.position_label.setAlignment(Qt.AlignCenter)

        self.position_table = QTableWidget()
        self.create_table(self.position_table, ["Pozīcija", "Gabali", "Mainīt Skaitu"])
        self.position_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.position_table.setColumnWidth(1, 80)
        self.position_table.setColumnWidth(2, 210)
    
        self.price_label = QLabel("Cenas Tabula")
        self.price_label.setObjectName("secondaryLabel")
        self.price_label.setAlignment(Qt.AlignCenter)

        self.price_table = QTableWidget()
        self.create_table(self.price_table, ["Iecirknis", "Cena", "Gabali", "Mainīt Skaitu", "KOPĀ"])
        self.price_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.price_table.setColumnWidth(1, 80)
        self.price_table.setColumnWidth(2, 80)
        self.price_table.setColumnWidth(3, 210)
        self.price_table.setColumnWidth(4, 100)

        left_layout.addWidget(self.position_label)
        left_layout.addWidget(self.position_table)
        left_layout.addWidget(self.price_label)
        left_layout.addWidget(self.price_table)

        lower_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        self.workers_label = QLabel("Sērijas Darbinieku Tabula")
        self.workers_label.setObjectName("secondaryLabel")
        self.workers_label.setAlignment(Qt.AlignCenter)

        self.workers_table = QTableWidget()
        self.create_table(self.workers_table, ["Darbinieks", "Efektivitāte", "Strādās Šajā Sērijā"])
        self.workers_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.workers_table.setColumnWidth(1, 100)
        self.workers_table.setColumnWidth(2, 210)

        self.results_label = QLabel("Sērijas Apkopojums")
        self.results_label.setObjectName("secondaryLabel")
        self.results_label.setAlignment(Qt.AlignCenter)

        self.results_table = QTableWidget()
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
        
        lower_layout_buttons.setAlignment(Qt.AlignTop)

        self.button_label = QLabel("Sērijas Darbības")
        self.button_label.setObjectName("secondaryLabel")
        self.button_label.setAlignment(Qt.AlignCenter)
        self.button_label.setFixedWidth(250)
        lower_layout_buttons.addWidget(self.button_label)

        self.add_worker_button = QPushButton("Pievienot Darbinieku")
        self.add_worker_button.clicked.connect(self.add_worker)
        self.add_worker_button.setObjectName("greenButton")
        lower_layout_buttons.addWidget(self.add_worker_button)

        self.modify_worker_efficiency_button = QPushButton("Mainīt Efektivitāti")
        self.modify_worker_efficiency_button.clicked.connect(self.modify_worker_efficiency)
        self.modify_worker_efficiency_button.setObjectName("orangeButton")
        lower_layout_buttons.addWidget(self.modify_worker_efficiency_button)

        self.remove_worker_button = QPushButton("Dzēst Darbinieku")
        self.remove_worker_button.clicked.connect(self.delete_worker)
        self.remove_worker_button.setObjectName("redButton")
        lower_layout_buttons.addWidget(self.remove_worker_button)
        
        lower_layout_buttons.addStretch()

        self.results_button = QPushButton("Sērijas Dati")
        self.results_button.clicked.connect(self.go_to_print)
        self.results_button.setObjectName("blueButton")
        lower_layout_buttons.addWidget(self.results_button)

        self.settings_button = QPushButton("Koeficientu Iestatījumi")
        self.settings_button.clicked.connect(self.go_to_settings)
        self.settings_button.setObjectName("blueButton")
        lower_layout_buttons.addWidget(self.settings_button)

        self.reset_positions_button = QPushButton("Notīrīt Pozīcijas")
        self.reset_positions_button.clicked.connect(self.confirm_reset_positions)
        self.reset_positions_button.setObjectName("redButton")
        lower_layout_buttons.addWidget(self.reset_positions_button)

        self.reset_prices_button = QPushButton("Notīrīt Cenas")
        self.reset_prices_button.clicked.connect(self.confirm_reset_prices)
        self.reset_prices_button.setObjectName("redButton")
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
        self.update_page()

    # Delete worker dialog.
    def delete_worker(self):
        dialog = DeleteWorkerDialog(self)
        dialog.exec_()
        self.update_page()

    # Modify worker's efficiency dialog.
    def modify_worker_efficiency(self):
        dialog = EditWorkerEfficiencyDialog(self)
        dialog.exec_()
        self.update_page()

    # Set's the value of a position to the inputed number.
    def set_position_value(self, parent, position):
        dialog = PositionDialog(parent, position)
        dialog.exec_()
        self.update_page()

    # Set's the value of a price to the inputed number.
    def set_price_count(self, price_id, description):
        dialog = PriceDialog(self, price_id, description)
        dialog.exec_()
        self.update_page()

    # Confirm the position reset.
    def confirm_reset_positions(self):
        message = "Vai tiešām iestatīt visas pozīciju vērtības uz 0?      "
        dialog = ConfirmationDialog(self, message)
        if dialog.exec_():
            database.reset_positions(self.main_window.series_index)
            self.update_page()
         
    # Confirm price reset.
    def confirm_reset_prices(self):
        message = "Vai tiešām iestatīt visas cenu gabalu vērtības uz 0?      "
        dialog = ConfirmationDialog(self, message)
        if dialog.exec_():
            database.reset_prices(self.main_window.series_index)
            self.update_page()



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

        self.position_table.setRowCount(9)

        for row, (position, count) in enumerate(positions.items()):
            position_item = QTableWidgetItem(f"Pozīcija nr. {position}")
            count_item = QTableWidgetItem(str(count))

            button_layout = QHBoxLayout()
            increase_button = QPushButton("+1")
            increase_button.setFixedSize(60, 35)
            decrease_button = QPushButton("-1")
            decrease_button.setFixedSize(60, 35)
            set_button = QPushButton("Ievadīt")
            set_button.setFixedSize(60, 35)

            increase_button.clicked.connect(lambda _, pos=position: self.modify_position_value(pos, series_id, 1))
            decrease_button.clicked.connect(lambda _, pos=position: self.modify_position_value(pos, series_id, -1))
            set_button.clicked.connect(lambda _, pos=position: self.set_position_value(self, pos))

            increase_button.setObjectName("smallButton")
            decrease_button.setObjectName("smallButton")
            set_button.setObjectName("smallButton")

            button_layout.addWidget(increase_button)
            button_layout.addWidget(decrease_button)
            button_layout.addWidget(set_button)
            button_layout.setAlignment(Qt.AlignCenter)
            button_layout.setContentsMargins(0, 0, 0, 0)

            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            self.position_table.setItem(row, 0, position_item)
            self.position_table.setItem(row, 1, count_item)
            self.position_table.setCellWidget(row, 2, button_widget)

    # Updates the workers table.
    def populate_worker_table(self):
        workers = database.get_series_workers(self.main_window.series_index)
        if workers is None:
            return

        self.workers_table.setRowCount(len(workers))

        for row, worker in enumerate(workers.values()):
            name_item = QTableWidgetItem(f"{worker['name']} {worker['surname']}")
            efficiency_item = QTableWidgetItem(str(worker['efficiency']))
            button_item = QPushButton("Strādā" if worker['working'] else "Nestrādā")
            button_item.setObjectName("workerButton")
            button_item.clicked.connect(lambda _, w=worker: self.toggle_worker_status(w['worker_id']))

            self.workers_table.setItem(row, 0, name_item)
            self.workers_table.setItem(row, 1, efficiency_item)
            self.workers_table.setCellWidget(row, 2, button_item)

    # Update price table.
    def populate_price_table(self):
        prices = database.get_prices(self.main_window.series_index)
        if prices is None:
            return

        self.price_table.setRowCount(len(prices))

        for row, price in enumerate(prices.values()):
            description_item = QTableWidgetItem(price["description"])
            price_item = QTableWidgetItem(f"{price['price']}€")
            price_item.setTextAlignment(Qt.AlignCenter)
            count_item = QTableWidgetItem(str(price["count"]))
            count_item.setTextAlignment(Qt.AlignCenter)
            total_item = QTableWidgetItem(f"{round(price['price'] * price['count'], 2):.2f}€")
            total_item.setTextAlignment(Qt.AlignCenter)

            button_layout = QHBoxLayout()
            increase_button = QPushButton("+1")
            increase_button.setFixedSize(60, 35)
            decrease_button = QPushButton("-1")
            decrease_button.setFixedSize(60, 35)
            set_button = QPushButton("Ievadīt")
            set_button.setFixedSize(60, 35)
            
            increase_button.clicked.connect(lambda _, price_id=price["price_id"]: self.modify_price_value(price_id, 1))
            decrease_button.clicked.connect(lambda _, price_id=price["price_id"]: self.modify_price_value(price_id, -1))
            set_button.clicked.connect(lambda _, price_id=price["price_id"], desc=price["description"]: self.set_price_count(price_id, desc))

            increase_button.setObjectName("smallButton")
            decrease_button.setObjectName("smallButton")
            set_button.setObjectName("smallButton")

            button_layout.addWidget(increase_button)
            button_layout.addWidget(decrease_button)
            button_layout.addWidget(set_button)
            button_layout.setAlignment(Qt.AlignCenter)
            button_layout.setContentsMargins(0, 0, 0, 0)

            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            self.price_table.setItem(row, 0, description_item)
            self.price_table.setItem(row, 1, price_item)
            self.price_table.setItem(row, 2, count_item)
            self.price_table.setCellWidget(row, 3, button_widget)
            self.price_table.setItem(row, 4, total_item)

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
            coefficient_id = position  # Assuming coefficient_id starts from 0 and matches position - 1
            if coefficient_id in coefficients:
                position_time += positions[position] * coefficients[coefficient_id]["value"]

        total_efficiency = 0.0
        for worker_id, worker in workers.items():
            if worker["working"]:
                total_efficiency += worker["efficiency"]

        if total_efficiency == 0:
            self.results_table.clearContents()
            self.results_table.setRowCount(1)
            efficiency_time_item = QTableWidgetItem("UZMANĪBU!")
            efficiency_time_count = QTableWidgetItem("Neviens darbinieks nestrādā.")
            self.results_table.setItem(0, 0, efficiency_time_item)
            self.results_table.setItem(0, 1, efficiency_time_count)
            return

        efficiency_time = position_time / total_efficiency
        series_time = efficiency_time + efficiency_time * coefficients[10]["value"] + efficiency_time * coefficients[11]["value"]
        
        self.results_table.setRowCount(6)

        bold_font = QFont()
        bold_font.setBold(True)

        position_sum_item = QTableWidgetItem("Kopējais pozīciju gabalu skaits:")
        position_sum_count = QTableWidgetItem(str(position_sum))
        price_sum_item = QTableWidgetItem("Kopējā vērtība sērijai:")
        price_sum_count = QTableWidgetItem(f"{price_sum:.2f}€")
        position_time_item = QTableWidgetItem("Kopējais darba laiks (neņemot vērā efektivitāti):")
        position_time_count = QTableWidgetItem(self.to_hours_and_minutes(position_time))
        efficiency_time_item = QTableWidgetItem("Sērijas izpildes laiks (ņemot vērā efektivitāti):")
        efficiency_time_count = QTableWidgetItem(self.to_hours_and_minutes(efficiency_time))
        series_time_item_hours = QTableWidgetItem("Reālais sērijas izpildes laiks (ņemot vērā visus koeficientus):")
        series_time_count_hours = QTableWidgetItem(self.to_hours_and_minutes(series_time))
        series_time_count_hours.setFont(bold_font)
        series_time_item_days = QTableWidgetItem("Reālais sērijas izpildes laiks (dienās):")
        series_time_count_days = QTableWidgetItem(f"{round(series_time / 8, 1)}d")
        series_time_count_days.setFont(bold_font)

        self.results_table.setItem(0, 0, position_sum_item)
        self.results_table.setItem(0, 1, position_sum_count)
        self.results_table.setItem(1, 0, price_sum_item)
        self.results_table.setItem(1, 1, price_sum_count)
        self.results_table.setItem(2, 0, position_time_item)
        self.results_table.setItem(2, 1, position_time_count)
        self.results_table.setItem(3, 0, efficiency_time_item)
        self.results_table.setItem(3, 1, efficiency_time_count)
        self.results_table.setItem(4, 0, series_time_item_hours)
        self.results_table.setItem(4, 1, series_time_count_hours)
        self.results_table.setItem(5, 0, series_time_item_days)
        self.results_table.setItem(5, 1, series_time_count_days)

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
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.NoSelection)

    # Toggles worker's status.
    def toggle_worker_status(self, worker_id):
        database.toggle_working(worker_id)
        self.update_page()  # Refresh the table

    # Controls the modified position value.
    def modify_position_value(self, position, series_id, delta):
        if delta == 1:
            database.add_one(position, series_id)
        elif delta == -1:
            database.remove_one(position, series_id)
        self.update_page()

    # Controls the modified price value.
    def modify_price_value(self, price_id, delta):
        if delta == 1:
            database.add_one_price(price_id)
        elif delta == -1:
            database.remove_one_price(price_id)
        self.update_page()
    
    # Returns the hours and minutes in a string format.
    def to_hours_and_minutes(self, hours):
        whole_hours = int(hours)
        minutes = int((hours - whole_hours) * 60)
        return f"{whole_hours}h {minutes}m"