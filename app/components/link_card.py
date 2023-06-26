import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QVBoxLayout, QFileDialog
from qfluentwidgets import IconWidget, TextWrap, SingleDirectionScrollArea

from app.common.style_sheet import StyleSheet
from app.common.config import cfg
from MXX.MxPath.MxPath import MxPath
from app.common.signal_bus import signalBus


class LinkCard(QFrame):
    clicked = pyqtSignal()
    def __init__(self, icon, title, url, signal, name, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(198, 220)
        self._iconWidget = IconWidget(icon, self)
        self._titleLabel = QLabel(title, self)
        self._name = name
        self._url = url
        self._path = MxPath(cfg.get(self._url))
        self._contentLabel = QLabel(self._path.lenLimPath(28), self)
        self._signal = signal
        self._signal.connect(self.__refreshContent)
        self.__initWidget()

    def __initWidget(self):
        self.setCursor(Qt.PointingHandCursor)
        self._iconWidget.setFixedSize(54, 54)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(24, 24, 0, 13)
        self.vBoxLayout.addWidget(self._iconWidget)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self._titleLabel)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self._contentLabel)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self._titleLabel.setObjectName('titleLabel')
        self._contentLabel.setObjectName('contentLabel')

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        url = QFileDialog.getExistingDirectory(
            self, self.tr('Choose folder'), './config{}'.format(self._name)
        )
        self.folderChanged(url)

    def folderChanged(self, url):
        if not url or cfg.get(self._url) == url:
            return
        cfg.set(self._url, url)
        self._signal.emit()


    def __refreshContent(self):
        self._path = MxPath(cfg.get(self._url))
        self._contentLabel.setText(self._path.lenLimPath(28))
        self.repaint()


class LinkCardView(SingleDirectionScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Horizontal)
        self.view = QWidget()
        self.hBoxLayout = QHBoxLayout(self.view)

        self.hBoxLayout.setContentsMargins(36, 0, 0, 0)
        self.hBoxLayout.setSpacing(12)
        self.hBoxLayout.setAlignment(Qt.AlignLeft)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.view.setObjectName('view')
        StyleSheet.LINK_CARD.apply(self)

    def addCard(self, icon, title, url, signal, name):
        card = LinkCard(icon, title, url, signal, name, self.view)
        self.hBoxLayout.addWidget(card, 0, Qt.AlignLeft)

