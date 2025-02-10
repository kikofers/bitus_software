class ResultsTableModel(QAbstractTableModel):
    def __init__(self, results=None, parent=None):
        super().__init__(parent)
        self.results = results if results else []

    def rowCount(self, parent=None):
        return len(self.results)

    def columnCount(self, parent=None):
        return 2  # Label + Value

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row, col = index.row(), index.column()

        if role == Qt.DisplayRole:
            return self.results[row][col]  # Label or Value

        return None

    def update_results(self, new_results):
        """Updates the model with new calculated values and refreshes the view."""
        self.results = new_results
        self.layoutChanged.emit()  # Notify view to refresh