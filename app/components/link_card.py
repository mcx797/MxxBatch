import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel, QVBoxLayout, QFileDialog
from qfluentwidgets import IconWidget, TextWrap, SingleDirectionScrollArea

from app.common.style_sheet import StyleSheet
from app.common.config import cfg


class LinkCard(QFrame):
    def __init__(self, icon, title, url, signal, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(198, 220)
        self._iconWidget = IconWidget(icon, self)
        self._titleLabel = QLabel(title, self)
        self._url = url
        self._contentLabel = QLabel(TextWrap.wrap(cfg.get(self._url), 28, False)[0], self)
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
        url = ''
        if os.path.isfile(cfg.get(self._url)):
            fileLink = QFileDialog.getOpenFileName(
                self, self.tr('Choose folder'), cfg.get(self._url)
            )
            print(fileLink[0])
            url = fileLink[0]
        else:
            print('-------------------')
            fileLink = QFileDialog.getExistingDirectory(
                self, self.tr('Choose folder'), cfg.get(self._url)
            )
            print(fileLink)
            url = fileLink
        self.folderChanged(url)

    def folderChanged(self, url):
        if not url or cfg.get(self._url) == url:
            return
        cfg.set(self._url, url)
        self._signal.emit()

    def __refreshContent(self):
        print('refresh content table')
        self._contentLabel.setText(TextWrap.wrap(cfg.get(self._url), 28, False)[0])
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

    def addCard(self, icon, title, url, signal):
        card = LinkCard(icon, title, url, signal, self.view)
        self.hBoxLayout.addWidget(card, 0, Qt.AlignLeft)

