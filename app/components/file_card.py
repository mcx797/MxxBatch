from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QApplication

from MXX.MxFile.MxReFile import MxReFile

from qfluentwidgets import  FluentIcon, IconWidget, Theme, isDarkTheme


class FileCard(QFrame):
    clicked = pyqtSignal(MxReFile)

    def __init__(self, icon: FluentIcon, file:MxReFile, parent=None):
        super().__init__(parent=parent)
        self._icon = icon
        self._file = file
        self._content = file.fileSuffix
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

        text = self.nameLabel.fontMetrics().elidedText(self._content, Qt.ElideRight, 78)
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
            self.iconWidget.setIcon(self._icon)
        else:
            icon = self._icon.icon(Theme.LIGHT if isDarkTheme() else Theme.DARK)
            self.iconWidget.setIcon(icon)

        self.setProperty('isSelected', isSelected)
        self.setStyle(QApplication.style())
