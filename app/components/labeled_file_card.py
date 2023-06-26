from app.components.home_card import HomeCardView, HomeCard
from MXX.MxFile.MxReFile import MxReFile
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import IconWidget
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from MXX.MxPath.MxPath import MxPath
from app.common.style_sheet import StyleSheet


class LabeledFileCardView(HomeCardView):
    def __init__(self, parent, title:str):
        super().__init__(parent=parent, title=title)
        self._cards = {}


    def addCard(self, file:MxReFile):
        card = LabeledFileCard(
            icon = FIF.DOCUMENT,
            file = file,
            parent=self
        )
        self._cards[file.filePath] = card
        self.flowLayout.addWidget(card)


class LabeledFileCard(QFrame):
    def __init__(self, icon, file:MxReFile, parent=None):
        super().__init__(parent=parent)
        self._file = file

        self._icon_widget = IconWidget(icon, self)
        self._title_label = QLabel(file.fileName, self)
        print(file.fileName)
        self._content_label = QLabel(MxPath(file.filePath).lenLimPath(46), self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.setFixedSize(360, 180)
        self._icon_widget.setFixedSize(48, 48)

        self.hBoxLayout.setSpacing(28)
        self.hBoxLayout.setContentsMargins(20, 0, 0, 0)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self._icon_widget)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self._title_label)
        self.vBoxLayout.addWidget(self._content_label)
        self.vBoxLayout.addStretch(1)

        self._title_label.setObjectName('titleLabel')
        self._content_label.setObjectName('contentLabel')