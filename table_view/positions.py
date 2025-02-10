from PyQt5.QtWidgets import QStyledItemDelegate, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QModelIndex, QAbstractTableModel

class PositionTableModel(QAbstractTableModel):
    def __init__(self, positions, parent=None):
        super().__init__(parent)
        self.positions = positions  # List of (position, count) tuples

    def rowCount(self, parent=None):
        return len(self.positions)

    def columnCount(self, parent=None):
        return 3  # Position, Count, Buttons

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        position, count = self.positions[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == 0:
                return str(position)
            elif column == 1:
                return str(count)

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

class PositionButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent, modify_callback, set_callback):
        super().__init__(parent)
        self.modify_callback = modify_callback  # Function for +1/-1
        self.set_callback = set_callback  # Function for "Ievadīt"

    def createEditor(self, parent, option, index):
        editor = QWidget(parent)
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create three buttons
        increase_button = QPushButton("+1")
        decrease_button = QPushButton("-1")
        set_button = QPushButton("Ievadīt")

        increase_button.setFixedSize(60, 35)
        decrease_button.setFixedSize(60, 35)
        set_button.setFixedSize(60, 35)

        # Connect button signals
        row = index.row()
        increase_button.clicked.connect(lambda: self.modify_callback(row, 1))
        decrease_button.clicked.connect(lambda: self.modify_callback(row, -1))
        set_button.clicked.connect(lambda: self.set_callback(row))

        # Add buttons to layout
        layout.addWidget(increase_button)
        layout.addWidget(decrease_button)
        layout.addWidget(set_button)
        layout.setAlignment(Qt.AlignCenter)
        
        editor.setLayout(layout)
        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
