from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QVBoxLayout
from qfluentwidgets import FlowLayout, IconWidget, TextWrap

from app.common.style_sheet import StyleSheet
from app.common.signal_bus import signalBus


class HomeCard(QFrame):
    def __init__(self, icon, title, content, parent = None):
        super().__init__(parent=parent)
        self._icon_widget = IconWidget(icon, self)
        self._title_label = QLabel(title, self)
        self._content_label = QLabel(TextWrap.wrap(content, 45, False)[0], self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.setFixedSize(360, 90)
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

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)


class FileHomeCard(HomeCard):
    def __init__(self, icon, title, content, route_key, parent = None):
        super().__init__(icon, title, content, parent)
        self._route_key = route_key

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        signalBus.switchToSampleCard.emit(self._route_key)


class HomeCardView(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent = parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()

        self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
        self.vBoxLayout.setSpacing(10)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addLayout(self.flowLayout, 1)

        self.titleLabel.setObjectName('viewTitleLabel')
        StyleSheet.HOME_CARD.apply(self)

        self._cards = []

    def addCard(self, icon, title, content):
        card = HomeCard(icon, title, content, self)
        self.flowLayout.addWidget(card)
        self._cards.append(card)

    def addFileCard(self, icon, title, content, route_key):
        card = FileHomeCard(icon, title, content, route_key, self)
        self.flowLayout.addWidget(card)
        self._cards.append(card)