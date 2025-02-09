from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QHeaderView, QAbstractItemView, QSizePolicy
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from PIL import Image
import os

from manage_database.database import database

# Displays a diagramm of the positions in the series, also shows the same results
class Diagram(FigureCanvas):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        super().__init__(self.fig)

    def show_data(self, series_id):
        data = database.get_positions(series_id)  # Fetch data from database
        positions = sorted(data.keys())  # Ensure bars are in correct order
        values = [data[pos] for pos in positions]

        colors = ['yellow', 'red', 'green', 'green', 'red', 'red', 'yellow', 'red', 'yellow']
        labels = [f"Pos {pos}" for pos in positions]

        self.ax.clear()
        self.ax.bar(labels, values, color=colors)

        # Add values on top of bars
        for i, v in enumerate(values):
            self.ax.text(i, v + 0.2, str(v), ha='center', fontsize=10)

        self.ax.set_ylabel("Value")
        self.ax.set_title("Bar Chart Example")

        # Set the ticks and tick labels explicitly
        self.ax.set_xticks(range(len(labels)))
        self.ax.set_xticklabels(labels, rotation=45, ha="right")

        # Adjust layout to fit all elements
        self.fig.tight_layout(rect=[0, 0, 1, 0.95])
        self.draw()

    # Saves the chart as a picture in a folder.
    def save_chart(self, series_index):
        # Ensure the directory exists
        os.makedirs("pictures", exist_ok=True)
        # Save the chart as a picture in the directory
        self.fig.savefig(f"pictures\sērija_{series_index}.png", dpi=300)

# Displays a diagramm of the positions in the series, also shows the same results
# found in the default page. Allows the user to print the series data.
class PrintPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        main_layout = QVBoxLayout()

        label = QLabel("Printēt Sērijas Datus")
        label.setObjectName("mainLabel")
        main_layout.addWidget(label, alignment=Qt.AlignCenter)

        upper_button_layout = QHBoxLayout()
        
        self.series_label = QLabel()
        self.series_label.setObjectName("mainLabel")
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
        self.latest_series_button.setObjectName("latestSeriesButton")
        upper_button_layout.addWidget(self.latest_series_button)

        main_layout.addLayout(upper_button_layout)

        results_layout = QHBoxLayout()

        self.diagram = Diagram()
        self.diagram.show_data(self.main_window.series_index)

        self.results_table = QTableWidget()
        self.create_table(self.results_table, ["Kas", "Cik"])
        self.results_table.horizontalHeader().setVisible(False)
        
        self.default_button = QPushButton("Atpakaļ uz Sērijas Pārvaldīšanu")
        self.default_button.clicked.connect(self.go_to_default)
        self.default_button.setObjectName("defaultButton")

        self.export_pdf_button = QPushButton("Eksportēt PDF")
        self.export_pdf_button.clicked.connect(lambda: self.generate_pdf(self.main_window.series_index))
        self.export_pdf_button.setObjectName("exportPDFButton")
        
        results_layout.addWidget(self.diagram)
        results_layout.addWidget(self.results_table)
        results_layout.addWidget(self.default_button)
        
        main_layout.addWidget(self.export_pdf_button)
        main_layout.addLayout(results_layout)
        self.setLayout(main_layout)

        self.update_page()



#------ PDF Functions: ------
    def generate_pdf(self, series_index):
        # Save chart as image
        self.diagram.save_chart(series_index)
        chart_path = f"pictures\sērija_{series_index}.png"

        # Ensure the directory exists
        os.makedirs("pdf", exist_ok=True)
        
        # Create PDF
        pdf = canvas.Canvas(f"pdf\sērija_{series_index}.pdf", pagesize=letter)
        width, height = letter

        # Draw title
        pdf.setFont("Poppins", 16)
        pdf.drawString(200, height - 50, "Sērijas Dati")

        # Draw chart
        chart = Image.open(chart_path)
        pdf.drawInlineImage(chart_path, 50, height - 350, width=300, height=200)

        # Get table data
        data = []
        for row in range(self.results_table.rowCount()):
            row_data = []
            for col in range(self.results_table.columnCount()):
                item = self.results_table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        # Create table
        table = Table(data, colWidths=[200, 150])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Draw table
        table.wrapOn(pdf, width, height)
        table.drawOn(pdf, 50, height - 500)

        # Save PDF
        pdf.save()



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
        series_time_item_days = QTableWidgetItem("Reālais sērijas izpildes laiks (dienās):")
        series_time_count_days = QTableWidgetItem(f"{round(series_time / 8, 1)}d")

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
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

    # Returns the hours and minutes in a string format.
    def to_hours_and_minutes(self, hours):
        whole_hours = int(hours)
        minutes = int((hours - whole_hours) * 60)
        return f"{whole_hours}h {minutes}m"

    # Returns to the default page.
    def go_to_default(self):
        self.main_window.default_page.update_page()
        self.main_window.stack.setCurrentWidget(self.main_window.default_page)