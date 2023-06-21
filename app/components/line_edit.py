from qfluentwidgets import SearchLineEdit
class LineEdit(SearchLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent = parent)
        self.setPlaceholderText(self.tr('Search files'))
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)
