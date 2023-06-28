from app.components.home_card import HomeCardView, HomeCard
from MXX.MxFile.MxReFile import MxReFile
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import IconWidget
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from MXX.MxPath.MxPath import MxPath
from MXX.MxConfig.MxConfig.MxConfig import MxConfig
from app.common.style_sheet import StyleSheet
from app.view.post_label_dialog import PostLabelDialog
from app.common.signal_bus import signalBus
from app.view.mxx_interface import MxxInterface


class LabeledFileCardView(HomeCardView):
    def __init__(self, parent, title:str, mx_cfg:MxConfig):
        super().__init__(parent=parent, title=title)
        self._parent = parent
        self._cards = {}
        self._mx_cfg = mx_cfg

    def __len__(self):
        return len(self._cards)


    def addCard(self, file:MxReFile):
        card = LabeledFileCard(
            icon = FIF.DOCUMENT,
            file = file,
            mx_cfg=self._mx_cfg,
            parent=self
        )
        self._cards[file.filePath] = card
        self.flowLayout.addWidget(card)

    def deleteCard(self, file:MxReFile):
        for item in self._cards:
            if item == file.filePath:
                self._cards[item].hide()
                self.flowLayout.removeAllWidgets()
                self._cards.pop(item)
                break

        for card in self._cards:
            self.flowLayout.addWidget(self._cards[card])
        self.repaint()


class LabeledFileCard(QFrame):
    def __init__(self, icon, file:MxReFile, mx_cfg:MxConfig, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self._file = file
        self._mx_cfg = mx_cfg

        self._icon_widget = IconWidget(icon, self)
        self._title_label = QLabel(file.fileName, self)
        self._content_label = QLabel(MxPath(file.filePath).lenLimPath(46), self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.setFixedSize(360, 180)
        self._icon_widget.setFixedSize(48, 48)

        self.__initWidget()

        self._title_label.setObjectName('titleLabel')
        self._content_label.setObjectName('contentLabel')

    def __initWidget(self):
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

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        w = PostLabelDialog(self._file, self._mx_cfg)
        w.show()
        w.exec_()
        if self._file.label != w.typeName:
            signalBus.fileUnlabeledSignal.emit(self._file)
            self._file.setLabel(w.typeName)
            signalBus.fileLabeledSignal.emit(self._file, self._parent._parent)