from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QAbstractItemView, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from manage_database.database import database

class Diagram(FigureCanvas):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        super().__init__(self.fig)
        self.setMaximumSize(1200, 900)

        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('black')
        self.ax.spines['left'].set_linewidth(2)
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['bottom'].set_linewidth(2)
        self.ax.tick_params(axis='x', colors='#666666')
        self.ax.tick_params(axis='y', colors='#666666')
        self.ax.yaxis.label.set_color('#666666')
        self.ax.xaxis.label.set_color('#666666')
        self.ax.title.set_color('#333333')

    def show_data(self, series_id):
        colors = ['yellow', 'red', 'green', 'green', 'red', 'red', 'yellow', 'red', 'yellow']

        data = database.get_positions(series_id)
        positions = sorted(data.keys())

        values = [data[position] for position in positions]
        labels = [f"Poz. {position}" for position in positions]

        self.ax.clear()
        self.ax.bar(labels, values, color=colors, edgecolor='black')

        self.ax.set_title(f"Pozīciju Skaits {series_id}. Sērijā", fontsize=14)

        if values:
            bars = self.ax.bar(labels, values, color=colors, edgecolor='black')
            self.ax.set_ylim(0, max(max(values) * 1.2, 1))
            for bar, value in zip(bars, values):
                self.ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01 * max(values), f'{value}', ha='center', va='bottom', fontsize=12)
        else:
            self.ax.set_ylim(0, 1)
            self.ax.text(0.5, 0.5, "No data", ha='center', va='center', fontsize=14, transform=self.ax.transAxes)

        self.ax.set_ylabel("Gabali", fontsize=12)
        self.ax.set_xticks(range(len(labels)))
        self.ax.set_xticklabels(labels, fontsize=12)

        self.ax.yaxis.get_major_locator().set_params(integer=True)
        self.ax.yaxis.set_tick_params(labelsize=12)

        self.fig.tight_layout()
        self.fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.draw()

class PrintPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        main_layout = QVBoxLayout()

        label = QLabel("Sērijas Dati")
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

        self.default_button = QPushButton("Atpakaļ uz Sērijas Pārvaldīšanu")
        self.default_button.clicked.connect(self.go_to_default)
        self.default_button.setObjectName("blueButton")
        upper_button_layout.addWidget(self.default_button)

        main_layout.addLayout(upper_button_layout)

        results_layout = QHBoxLayout()

        self.diagram = Diagram()
        self.diagram.show_data(self.main_window.series_index)
        results_layout.addWidget(self.diagram, stretch=2)

        self.results_table = QTableWidget()
        self.create_table(self.results_table, ["Kas", "Cik"])
        self.results_table.horizontalHeader().setVisible(False)
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.results_table.setColumnWidth(1, 120)
        results_layout.addWidget(self.results_table, stretch=1)
        
        main_layout.addLayout(results_layout)
        self.setLayout(main_layout)

        self.update_page()



#------ Update Functions: ------
    def update_page(self):
        self.series_label_color()
        self.navigation_button_color()
        self.populate_results_table()
        self.diagram.show_data(self.main_window.series_index)

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
        for id in positions:
            if id in coefficients:
                position_time += positions[id] * coefficients[id]["value"]

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
    # Helper function to create the table and keep the code clean.
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

    # Returns the hours and minutes in a string format.
    def to_hours_and_minutes(self, hours):
        whole_hours = int(hours)
        minutes = int((hours - whole_hours) * 60)
        return f"{whole_hours}h {minutes}m"

    # Returns to the default page.
    def go_to_default(self):
        self.main_window.default_page.update_page()
        self.main_window.stack.setCurrentWidget(self.main_window.default_page)