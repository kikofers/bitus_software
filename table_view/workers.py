from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtWidgets import QPushButton, QStyledItemDelegate, QWidget, QHBoxLayout

class WorkerTableModel(QAbstractTableModel):
    def __init__(self, workers, parent=None):
        super().__init__(parent)
        self.workers = workers  # List of dictionaries

    def rowCount(self, parent=None):
        return len(self.workers)

    def columnCount(self, parent=None):
        return 3  # "Darbinieks", "Efektivitāte", "Strādās Šajā Sērijā"

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        worker = self.workers[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == 0:
                return f"{worker['name']} {worker['surname']}"
            elif column == 1:
                return str(worker['efficiency'])

        return None  # Other roles return nothing

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

class WorkerButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent, toggle_callback):
        super().__init__(parent)
        self.toggle_callback = toggle_callback  # Function to handle button clicks

    def createEditor(self, parent, option, index):
        # Create a QWidget container with a QPushButton inside
        editor = QWidget(parent)
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton()
        layout.addWidget(button)

        # Store index row in button's property to identify the worker later
        button.clicked.connect(lambda: self.toggle_callback(index.row()))

        editor.setLayout(layout)
        return editor

    def setEditorData(self, editor, index):
        button = editor.layout().itemAt(0).widget()
        worker = self.parent().model().workers[index.row()]
        button.setText("Strādā" if worker['working'] else "Nestrādā")

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)