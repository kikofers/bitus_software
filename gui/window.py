from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import Qt

from gui.default import DefaultPage
from gui.settings import SettingsPage
from gui.print import PrintPage

import os
import sys

from manage_database.database import database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tētim programma")
        self.setGeometry(0, 0, 1880, 700)

        self.series_index = database.get_last_series_id()

        self.stack = QStackedWidget()

        self.default_page = DefaultPage(self)
        self.settings_page = SettingsPage(self)
        self.print_page = PrintPage(self)

        self.stack.addWidget(self.default_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.print_page)

        self.setCentralWidget(self.stack)

        self.apply_stylesheet()

    def apply_stylesheet(self):
        # Get paths
        font_dir = get_resource_path("styles/fonts")
        qss_path = get_resource_path("styles/styles.qss")

        # Load all necessary font variants
        font_files = [
            "Roboto-Regular.ttf",
            "Roboto-Italic.ttf",
            "Roboto-Bold.ttf",
            "Roboto-BoldItalic.ttf",
            "Roboto-Black.ttf"
        ]

        for font_file in font_files:
            full_font_path = os.path.join(font_dir, font_file)
            font_id = QFontDatabase.addApplicationFont(full_font_path)

        with open(qss_path, 'r') as file:
            self.setStyleSheet(file.read())

    # Always displays the window as full-screen.
    def showEvent(self, event):
        self.showFullScreen()
        super().showEvent(event)

    # Exits full-screen mode.
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showNormal()

def get_resource_path(relative_path):
    """Get the absolute path to a resource, ensuring it works in both development and PyInstaller."""
    if getattr(sys, 'frozen', False):  # Running as a PyInstaller executable
        base_path = sys._MEIPASS  # PyInstaller's extraction folder
    else:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))  # Use script's directory

    return os.path.normpath(os.path.join(base_path, relative_path))