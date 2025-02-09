from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPainter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt

class PrintWidget(QWidget):
    def __init__(self, parent=None):
        super(PrintWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.graph_label = QLabel("Graph of Position Values")
        layout.addWidget(self.graph_label)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.print_button = QPushButton("Print")
        self.print_button.clicked.connect(self.print)
        layout.addWidget(self.print_button)

        self.setLayout(layout)

    def plot_graph(self, data):
        self.ax.clear()
        self.ax.plot(data)
        self.canvas.draw()

    def print(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.handle_paint_request(printer)

    def handle_paint_request(self, printer):
        painter = QPainter(printer)
        screen = self.grab()
        painter.drawPixmap(0, 0, screen)
        painter.end()