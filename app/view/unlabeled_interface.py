from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, QApplication

from qfluentwidgets import (SmoothScrollArea, SearchLineEdit, FluentIcon, IconWidget, Theme, isDarkTheme)

from app.view.mxx_interface import MxxInterface

from mxx.mxxfile.File import File


class LineEdit(SearchLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent = parent)
        self.setPlaceholderText(self.tr('Search files'))
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)


class FileCard(QFrame):
    clicked = pyqtSignal(FluentIcon)

    def __init__(self, icon: FluentIcon, file:File, parent=None):
        super().__init__(parent=parent)
        self._icon = icon
        self._file = file
        self.isSelected = False
        self.iconWidget = IconWidget(icon, self)
        self.nameLabel = QLabel(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.setFixedSize(96, 96)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(8, 28, 8, 0)

        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.iconWidget.setFixedSize(28, 28)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignHCenter)
        self.vBoxLayout.addSpacing(14)
        self.vBoxLayout.addWidget(self.nameLabel, 0, Qt.AlignHCenter)

        text = self.nameLabel.fontMetrics().elidedText(file.fileSuffix(), Qt.ElideRight, 78)
        self.nameLabel.setText(text)

    def mouseReleaseEvent(self, e):
        if self.isSelected:
            return

        self.clicked.emit(self._file)

    def setSelected(self, isSelected:bool, force=False):
        if isSelected == self.isSelected and not force:
            return

        self.isSelected = isSelected

        if not isSelected:
            self.iconWidget.setIcon(self.icon)
        else:
            icon = self.icon.icon(Theme.LIGHT if isDarkTheme() else Theme.DARK)
            self.iconWidget.setIcon(icon)

        self.setProperty('isSelected', isSelected)
        self.setStyle(QApplication.style())


class CardView(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent=parent)
        self.Label = QLabel(self.tr('Unlabeled Files'), self)
        self.searchLineEdit = LineEdit(self)
        self.view = QFrame(self)
        self.scrollArea = SmoothScrollArea(self.view)
        self.scrollWidget = QWidget(self.scrollArea)


class UnlabeledInterface(MxxInterface):
    def __init__(self, parent=None):
        super().__init__(
            title='未分类文件',
            subtitle = 'unlabeled files',
            parent = parent
        )

        self._cardView = CardView(self)
        self.vBoxLayout.addWidget(self._cardView)