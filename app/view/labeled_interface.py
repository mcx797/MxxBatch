from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, QHBoxLayout
from qfluentwidgets import (SmoothScrollArea, FlowLayout, PrimaryPushButton, FluentIcon)
from qfluentwidgets import FluentIcon as FIF

from app.components.line_edit import LineEdit
from app.common.style_sheet import StyleSheet
from app.common.open_file import open_file
from app.components.tree_frame import TreeFrame
from app.components.file_card import FileCard
from app.view.mxx_interface import MxxInterface

from MXX.MxFile.MxReFileGallery import MxReFileGallery
from MXX.MxFile.MxReFile import MxReFile
from MXX.MxConfig.MxConfig.MxConfig import MxConfig

from app.view.relabel_dialog import RelabelDialog
from app.common.signal_bus import signalBus
from app.view.post_label_dialog import PostLabelDialog


class MesPanel(QFrame):
    def __init__(self, parent, mx_cfg):
        super().__init__(parent=parent)
        self._parent = parent
        self._mx_cfg = mx_cfg
        self._file_name_label = QLabel(self.tr('文件名字.txt'))
        self._file_type_label = QLabel(self.tr('文件类型'))
        self.vBoxLayout = QVBoxLayout(self)

        self.setFixedWidth(500)
        self.height()

        self._file_name_label.setObjectName('fileNameLabel')
        self._file_type_label.setObjectName('fileTypeLabel')
        self.frame = TreeFrame(self, False)

        self._button_open_dir = PrimaryPushButton(self.tr('打开文件夹'))
        self._button_open_file = PrimaryPushButton(self.tr('打开文件'))
        self._re_label = PrimaryPushButton(self.tr('更改分类'))
        self._ok_label = PrimaryPushButton(self.tr('确认分类'))

        self._button_open_file.clicked.connect(self.openFile)
        self._button_open_dir.clicked.connect(self.openDir)
        self._re_label.clicked.connect(self.reLabel)
        self._ok_label.clicked.connect(self.okLabel)
        self.__initWidget()

    def __initWidget(self):
        self.vBoxLayout.setContentsMargins(15, 5, 5, 5)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.addWidget(self._file_name_label)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self._file_type_label)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.frame)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self._button_open_dir)
        self.vBoxLayout.addWidget(self._button_open_file)
        self.vBoxLayout.addWidget(self._re_label)
        self.vBoxLayout.addWidget(self._ok_label)
        self.vBoxLayout.addSpacing(5)

    def reLabel(self):
        if not isinstance(self._file, MxReFile):
            return
        w = PostLabelDialog(self._file, self._mx_cfg)
        w.show()
        w.exec_()
        if self._file.isLabeled:
            return
        if w.isOk:
            print(w.typeName)
            self._file.setLabel(w.typeName)
            signalBus.fileLabeledSignal.emit(self._file, self._parent._parent)
            self._file = None
            signalBus.autoLabeledSignal.emit()
        w.deleteLater()

    def okLabel(self):
        if not isinstance(self._file, MxReFile):
            return
        if self._file.isLabeled:
            return
        self._file.setLabel(self._file.autoLabel)
        signalBus.fileLabeledSignal.emit(self._file, self._parent._parent)
        self._file = None
        signalBus.autoLabeledSignal.emit()

    def openDir(self):
        if not isinstance(self._file, MxReFile):
            return
        open_file(self._file.dirPath)

    def openFile(self):
        if not isinstance(self._file, MxReFile):
            return
        open_file(self._file.filePath)

    def setMes(self, file:MxReFile):
        self._file = file
        self._file_name_label.setText(file.fileName)
        self._file_type_label.setText(file.autoLabel)
        self.frame.refresh(file)


class CardView(QWidget):
    def __init__(self, parent, mx_cfg: MxConfig):
        super().__init__(parent=parent)
        self._parent = parent
        self._mx_cfg = mx_cfg
        self._card_view_label = QLabel(self.tr('自动分类文件'), self)
        self._search_line_edit = LineEdit(self)
        self._mes_panel = MesPanel(self, mx_cfg)

        self.view = QFrame(self)
        self.scrollArea = SmoothScrollArea(self.view)
        self.scrollWidget = QWidget(self.scrollArea)

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.flowLayout = FlowLayout(self.scrollWidget, isTight=False)

        self._cards = []
        self._files = self._mx_cfg.autoLabeledFiles
        self._current_idx = -1
        self.__initWidget()

    def __initWidget(self):
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setViewportMargins(0, 5, 0, 5)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.addWidget(self._card_view_label)
        self.vBoxLayout.addWidget(self._search_line_edit)
        self.vBoxLayout.addWidget(self.view)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.scrollArea)
        self.hBoxLayout.addWidget(self._mes_panel, 0, Qt.AlignRight)

        self.flowLayout.setVerticalSpacing(8)
        self.flowLayout.setHorizontalSpacing(8)
        self.flowLayout.setContentsMargins(8, 3, 8, 8)

        self.__setQss()

        self._search_line_edit.clearSignal.connect(self.showAllFiles)
        self._search_line_edit.searchSignal.connect(self.search)
        signalBus.autoLabeledSignal.connect(self.__fileLabeled)

        for file in self._files:
            self.addCard(FIF.FOLDER, file)
        for file in self._files:
            if file.isAutoLabeled:
                self.__setSelectedFile(file)
                break

    def __setQss(self):
        self.view.setObjectName('cardView')
        self.scrollWidget.setObjectName('scrollWidget')
        self._card_view_label.setObjectName('cardViewLabel')
        StyleSheet.LABELED_INTERFACE.apply(self)

    def addCard(self, icon:FluentIcon, file:MxReFile):
        card = FileCard(icon, file, self)
        card.clicked.connect(self.__setSelectedFile)
        self._cards.append(card)
        card.show()
        self.flowLayout.addWidget(card)

    def __setSelectedFile(self, file:MxReFile):
        index = self._files.index(file)
        if self._current_idx >= 0:
            self._cards[self._current_idx].setSelected(False)
        self._current_idx = index
        self._cards[index].setSelected(True)
        self._mes_panel.setMes(file)

    def search(self, key_word: str):
        indexes = []
        for i, file in enumerate(self._files):
            if file.searchAutoLabeled(key_word):
                indexes.append(i)

        for i, card in enumerate(self._cards):
            isVisible = i in indexes
            if isVisible:
                card.show()
            else:
                card.hide()

        if len(indexes) > 0:
            self.__setSelectedFile(self._files[indexes[0]])
        self.repaint()

    def showAllFiles(self):
        indexes = []
        for i, file in enumerate(self._files):
            if not file.isAutoLabeled:
                continue
            if file.isLabeled:
                continue
            indexes.append(i)

        for i, card in enumerate(self._cards):
            isVisible = i in indexes
            if isVisible:
                card.show()
            else:
                card.hide()
        if len(indexes) > 0:
            self.__setSelectedFile(self._files[indexes[0]])

        self.repaint()

    def __fileLabeled(self):
        indexes = []
        for i, file in enumerate(self._files):
            if not file.isAutoLabeled:
                continue
            if file.isLabeled:
                continue
            indexes.append(i)

        signalBus.homeMesRefresh.emit()

        if indexes == []:
            signalBus.switchToSampleCard.emit('homeInterface')

        for i, card in enumerate(self._cards):
            isVisible = i in indexes
            if isVisible:
                card.show()
            else:
                card.hide()
        if len(indexes) > 0:
            self.__setSelectedFile(self._files[indexes[0]])

        self.repaint()


class LabeledInterface(MxxInterface):
    def __init__(self, parent, mx_cfg:MxConfig):
        super().__init__(
            parent = parent,
            title='自动分类文件',
            subtitle = 'labeled files',
            mx_cfg=mx_cfg
        )

        self._card_view = CardView(self, self._mx_cfg)
        self.vBoxLayout.addWidget(self._card_view)

