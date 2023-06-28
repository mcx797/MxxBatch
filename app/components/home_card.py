from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QVBoxLayout
from qfluentwidgets import FlowLayout, IconWidget, TextWrap

from MXX.MxConfig.MxConfig.MxConfig import MxConfig
from MXX.MxConfig.MxPara.MxParaGallery import MxParaItem

from app.common.style_sheet import StyleSheet
from app.common.signal_bus import signalBus
from qfluentwidgets import FluentIcon as FIF


class HomeCard(QFrame):
    def __init__(self, icon, title, content, parent = None):
        super().__init__(parent=parent)
        self._icon_widget = IconWidget(icon, self)
        self._title_label = QLabel(title, self)
        self._content_label = QLabel(content, self)
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


class HomeFileCard(HomeCard):
    def __init__(self, icon, title, content, route_key, parent = None):
        super().__init__(icon, title, content, parent)
        self._route_key = route_key

    def refreshCardCon(self, str):
        self._content_label.setText(str)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        signalBus.switchToSampleCard.emit(self._route_key)


class HomeTypeCard(HomeCard):
    def __init__(self, icon, title, content, route_key, parent = None):
        super().__init__(icon, title, content, parent)
        self._route_key = route_key
        self._file_num = 0

    def refreshCardCon(self, str):
        self._content_label.setText(str)

    def addFile(self):
        self._file_num = self._file_num + 1
        self.refreshCardCon("文件数: {}".format(self._file_num))

    def subFile(self):
        self._file_num = self._file_num - 1
        self.refreshCardCon("文件数: {}".format(self._file_num))

    def __len__(self):
        return self._file_num

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        signalBus.switchToSampleCard.emit(self._route_key)


class HomeCardView(QWidget):
    def __init__(self, parent, title:str):
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


class HomeFileCardView(HomeCardView):
    def __init__(self, parent, title:str):
        super().__init__(parent=parent, title=title)

    def addCard(self, file_card:HomeFileCard):
        card = file_card
        self.flowLayout.addWidget(card)
        self._cards.append(card)


class HomeTypeCardView(HomeCardView):
    def __init__(self, parent, title:str):
        super().__init__(parent=parent, title=title)

    def addCard(self, type_card: HomeTypeCard):
        card = type_card
        self.flowLayout.addWidget(card)
        self._cards.append(card)



