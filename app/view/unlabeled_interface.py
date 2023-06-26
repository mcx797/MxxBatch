from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, QApplication, QHBoxLayout, \
    QTreeWidgetItem, QTreeWidgetItemIterator

from qfluentwidgets import (SmoothScrollArea, SearchLineEdit, FluentIcon, IconWidget, Theme, isDarkTheme, FlowLayout,
                            PrimaryPushButton, TreeWidget)

from qfluentwidgets import FluentIcon as FIF

from app.view.mxx_interface import MxxInterface

from MXX.MxConfig.MxConfig.MxConfig import MxConfig
from MXX.MxFile.MxReFile import MxReFile
from MXX.MxFile.MxReFileGallery import MxReFileGallery

from app.components.tree_frame import TreeFrame

from app.common.style_sheet import StyleSheet
from app.common.open_file import open_file
from app.view.relabel_dialog import RelabelDialog
from app.components.line_edit import LineEdit
from app.components.file_card import FileCard
from app.common.signal_bus import signalBus


class MesPanel(QFrame):
    def __init__(self, parent, mx_cfg):
        super().__init__(parent=parent)
        self._mx_cfg = mx_cfg
        self._file_name_label = QLabel(self.tr('文件名字.txt'))
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(15, 5, 5, 5)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.addWidget(self._file_name_label)
        self.setFixedWidth(500)
        self._file_name_label.setObjectName('fileNameLabel')
        self.frame = TreeFrame(self, False)
        self.vBoxLayout.addWidget(self.frame)

        self._button_open_file = PrimaryPushButton(self.tr('打开文件'))
        self._button_open_dir = PrimaryPushButton(self.tr('打开文件夹'))
        self._button_label = PrimaryPushButton(self.tr('进行分类'))


        self.vBoxLayout.addWidget(self._button_open_dir)
        self.vBoxLayout.addWidget(self._button_open_file)
        self.vBoxLayout.addWidget(self._button_label)

        self._button_open_file.clicked.connect(self.openFile)
        self._button_open_dir.clicked.connect(self.openDir)
        self._button_label.clicked.connect(self.reLabel)

    def reLabel(self):
        if not isinstance(self._file, MxReFile):
            return
        w = RelabelDialog(self._mx_cfg.labelDic)
        w.show()
        w.exec_()
        if self._file.isLabeled:
            return
        if w.isOk:
            self._file.setLabel(w.typeName)
            signalBus.fileLabeledSignal.emit(self._file)
            self._file = None
            signalBus.autoUnlabeledSignal.emit()
        w.deleteLater()

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
        self.frame.refresh(file)


class CardView(QWidget):
    def __init__(self, parent, mx_cfg:MxConfig):
        super().__init__(parent=parent)
        self._mx_cfg = mx_cfg
        self._card_view_label = QLabel(self.tr('未自动分类文件'), self)
        self._search_line_edit = LineEdit(self)
        self._mes_panel = MesPanel(self, mx_cfg)

        self.view = QFrame(self)
        self.scrollArea = SmoothScrollArea(self.view)
        self.scrollWidget = QWidget(self.scrollArea)


        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.flowLayout = FlowLayout(self.scrollWidget, isTight=False)

        self._cards = []
        self._files = self._mx_cfg.autoUnlabeledFiles
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
        signalBus.autoUnlabeledSignal.connect(self.__fileLabeled)

        for file in self._files:
            self.addCard(FIF.FOLDER, file)

        for file in self._files:
            if not file.isAutoLabeled:
                self.__setSelectedFile(file)
                break

    def __fileLabeled(self):
        indexes = []
        for i, file in enumerate(self._files):
            if file.isLabeled:
                continue
            if file.isAutoLabeled:
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

    def __setQss(self):
        self.view.setObjectName('cardView')
        self.scrollWidget.setObjectName('scrollWidget')
        self._card_view_label.setObjectName('cardViewLabel')
        StyleSheet.UNLABELED_INTERFACE.apply(self)

    def search(self, keyWord: str):
        indexes = []
        for i, file in enumerate(self._files):
            if file.searchAutoUnlabeled(keyWord):
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
            if file.isLabeled:
                continue
            if file.isAutoLabeled:
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


class UnlabeledInterface(MxxInterface):
    def __init__(self, parent, mx_cfg:MxConfig):
        super().__init__(
            parent=parent,
            title='未自动分类文件',
            subtitle = 'unlabeled files',
            mx_cfg=mx_cfg
        )
        self._card_view = CardView(self, self._mx_cfg)
        self.vBoxLayout.addWidget(self._card_view)

