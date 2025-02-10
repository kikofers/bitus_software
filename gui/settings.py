from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QAbstractItemView, QSizePolicy, QInputDialog
from PyQt5.QtCore import Qt

from manage_database.database import database

# Displays all 11 coefficients. Each can be adjusted by the user.
class SettingsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        main_layout = QVBoxLayout()

        label = QLabel("Koeficientu Pārvaldīšana")
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

        self.default_button = QPushButton("Atpakaļ uz Sērijas Pārvaldīšanu")
        self.default_button.clicked.connect(self.go_to_default)
        self.default_button.setObjectName("defaultButton")
        upper_button_layout.addWidget(self.default_button)

        main_layout.addLayout(upper_button_layout)



        coefficient_layout = QHBoxLayout()
        coefficient_layout.setAlignment(Qt.AlignCenter)

        left_spacer = QVBoxLayout()
        left_spacer.addStretch()

        coefficient_table_layout = QVBoxLayout()
        
        self.table_label = QLabel("Sērijas Koeficientu Tabula")
        self.table_label.setObjectName("secondaryLabel")
        self.table_label.setAlignment(Qt.AlignCenter)
        coefficient_table_layout.addWidget(self.table_label, alignment=Qt.AlignTop)

        self.coefficient_table = QTableWidget()
        self.create_table(self.coefficient_table, ["Koeficients", "Vērtība", "Mainīt Vērtību"])
        coefficient_table_layout.addWidget(self.coefficient_table)

        right_spacer = QVBoxLayout()
        right_spacer.addStretch()

        coefficient_layout.addLayout(left_spacer, 1)
        coefficient_layout.addLayout(coefficient_table_layout, 3)
        coefficient_layout.addLayout(right_spacer, 1)

        main_layout.addLayout(coefficient_layout)
        self.setLayout(main_layout)

        self.update_page()



#------ Update Functions: ------
    def update_page(self):
        self.series_label_color()
        self.navigation_button_color()
        self.populate_coefficient_table()

    # Updates series label color.
    def series_label_color(self):
        colors = ["black", "blue", "green", "red"]
        selected_color = colors[(self.main_window.series_index - 1) % 4] if self.main_window.series_index else "orange"
        self.series_label.setText(f"Sērija {self.main_window.series_index if self.main_window.series_index else 'Nav'}")
        self.series_label.setStyleSheet(f"color: {selected_color};")
        self.series_label.show()

    # Updates coefficient table.
    def populate_coefficient_table(self):
        series_id = self.main_window.series_index

        coefficients = database.get_coefficients(series_id)
        if coefficients is None:
            return
        
        self.coefficient_table.setRowCount(11)
        
        for row, coefficient in enumerate(coefficients.values()):
            coefficient_item = QTableWidgetItem(coefficient["description"])
            coefficient_item.setTextAlignment(Qt.AlignCenter)
            value_item = QTableWidgetItem(str(coefficient["value"]))
            value_item.setTextAlignment(Qt.AlignCenter)


            set_button = QPushButton("Mainīt")
            set_button.setObjectName("changeButton")
            set_button.clicked.connect(lambda _, co=coefficient["coefficient_id"]: self.set_coefficient_value(co, series_id))

            self.coefficient_table.setItem(row, 0, coefficient_item)
            self.coefficient_table.setItem(row, 1, value_item)
            self.coefficient_table.setCellWidget(row, 2, set_button)



#------ Dialogs: ------
    def set_coefficient_value(self, coefficient, series_id):
        new_value, ok = QInputDialog.getDouble(self, "Mainīt vērtību", f"Iestatīt jauno koeficienta vērtību:", decimals=2, min=0)
        if ok:
            database.set_coefficient(coefficient, series_id, new_value)
            self.update_page()



#------ Navigation Buttons: ------
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
    # Helper function to create the two tables and keep the code clean.
    def create_table(self, table, headers):
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

    def go_to_default(self):
        self.main_window.default_page.update_page()
        self.main_window.stack.setCurrentWidget(self.main_window.default_page)