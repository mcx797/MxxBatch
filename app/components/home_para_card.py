from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QVBoxLayout
from qfluentwidgets import FlowLayout, IconWidget, TextWrap, LineEdit, ComboBox

from MXX.MxConfig.MxConfig.MxConfig import MxConfig
from MXX.MxConfig.MxPara.MxParaGallery import MxParaItem, MxParaType

from app.common.style_sheet import StyleSheet
from app.common.signal_bus import signalBus
from app.components.home_card import HomeCardView
from qfluentwidgets import FluentIcon as FIF


class HomeParaCardView(HomeCardView):
    def __init__(self, parent):
        super().__init__(parent=parent, title='参数设置')
        self._cards = {}

    def addCard(self, para:MxParaItem):
        card = HomeParaCard(self, FIF.CODE, para)
        self.flowLayout.addWidget(card)
        self._cards[para.name] = card

    def addStrCard(self, para:MxParaItem):
        if para.type != MxParaType.STR:
            return
        card = HomeStrParaCard(self, FIF.EDIT, para)
        self.flowLayout.addWidget(card)
        self._cards[para.name] = card

    def addOptionCard(self, para:MxParaItem):
        if para.type != MxParaType.OPTION:
            return
        card = HomeOptionParaCard(self, FIF.MENU, para)
        self.flowLayout.addWidget(card)
        self._cards[para.name] = card


class HomeParaCard(QFrame):
    def __init__(self, parent, icon, para:MxParaItem):
        super().__init__(parent=parent)
        self._icon_widget = IconWidget(icon, self)
        self._title_label = QLabel(para.name, self)
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


        self._title_label.setObjectName('titleLabel')

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)


class HomeStrParaCard(HomeParaCard):
    def __init__(self, parent, icon, para:MxParaItem):
        super().__init__(parent, icon, para)
        self._line_edit = LineEdit(self)
        self._line_edit.setText(self.tr(para.value))
        self.vBoxLayout.addSpacing(10)
        self.vBoxLayout.addWidget(self._line_edit)
        self.vBoxLayout.addStretch(1)

class HomeOptionParaCard(HomeParaCard):
    def __init__(self, parent, icon, para:MxParaItem):
        super().__init__(parent, icon, para)
        self._combo_box = ComboBox()
        self._combo_box.addItems(para.option)
        self._combo_box.setCurrentIndex(0)
        self._combo_box.setMinimumWidth(110)
        self.vBoxLayout.addSpacing(10)
        self.vBoxLayout.addWidget(self._combo_box)
        self.vBoxLayout.addStretch(1)
