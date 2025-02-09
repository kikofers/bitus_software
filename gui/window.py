from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget
from PyQt5.QtCore import Qt

from gui.default import DefaultPage
from gui.settings import SettingsPage
from gui.print import PrintPage

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
        with open('styles/styles.qss', 'r', encoding='utf-8') as file:
            self.setStyleSheet(file.read())

    # Always displays the window as full-screen.
    def showEvent(self, event):
        self.showFullScreen()
        super().showEvent(event)

    # Exits full-screen mode.
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showNormal()