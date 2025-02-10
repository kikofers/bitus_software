from PyQt5.QtWidgets import QStyledItemDelegate, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QModelIndex, QAbstractTableModel

class PriceTableModel(QAbstractTableModel):
    def __init__(self, prices, parent=None):
        super().__init__(parent)
        self.prices = prices  # List of dicts with keys: description, price, count, price_id

    def rowCount(self, parent=None):
        return len(self.prices)

    def columnCount(self, parent=None):
        return 5  # Description, Price, Count, Buttons, Total

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        price = self.prices[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == 0:
                return price["description"]
            elif column == 1:
                return str(price["price"])
            elif column == 2:
                return str(price["count"])
            elif column == 4:  # Total
                return f"{round(price['price'] * price['count'], 2):.2f}€"

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

class PriceButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent, modify_callback, set_callback):
        super().__init__(parent)
        self.modify_callback = modify_callback  # Function for +1/-1
        self.set_callback = set_callback  # Function for "Ievadīt"

    def createEditor(self, parent, option, index):
        editor = QWidget(parent)
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create buttons
        increase_button = QPushButton("+1")
        decrease_button = QPushButton("-1")
        set_button = QPushButton("Ievadīt")

        increase_button.setFixedSize(60, 35)
        decrease_button.setFixedSize(60, 35)
        set_button.setFixedSize(60, 35)

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
