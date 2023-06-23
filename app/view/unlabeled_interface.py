from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, QApplication, QHBoxLayout, \
    QTreeWidgetItem, QTreeWidgetItemIterator

from qfluentwidgets import (SmoothScrollArea, SearchLineEdit, FluentIcon, IconWidget, Theme, isDarkTheme, FlowLayout,
                            PrimaryPushButton, TreeWidget)

from qfluentwidgets import FluentIcon as FIF

from app.view.mxx_interface import MxxInterface

from MXX.mxxfile.FileGallery import FileGallery
from MXX.mxxfile.LabeledFile import LabeledFile

from app.components.tree_frame import TreeFrame

from app.common.style_sheet import StyleSheet
from app.common.config import cfg
from MXX.mxxfile.Path import Path
from app.common.open_file import open_file
from app.view.relabel_dialog import RelabelDialog
from app.components.line_edit import LineEdit
from app.components.file_card import FileCard


class MesPanel(QFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.fileNameLabel = QLabel(self.tr('文件名字.txt'))
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(15, 5, 5, 5)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.addWidget(self.fileNameLabel)
        self.setFixedWidth(500)
        self.fileNameLabel.setObjectName('fileNameLabel')
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
        w = RelabelDialog()
        w.show()
        w.exec_()
        print(w._type_items[w._type_idx])

    def openDir(self):
        open_file(self._file.fileDir())

    def openFile(self):
        open_file(self._file.filePath())

    def setMes(self, file:LabeledFile):
        self._file = file
        self.fileNameLabel.setText(file.fileName())
        self.frame.refresh(file)


class CardView(QWidget):
    def __init__(self, parent = None, file_gallery:FileGallery = None):
        super().__init__(parent=parent)
        self.cardViewlabel = QLabel(self.tr('未自动分类文件'), self)
        self.searchLineEdit = LineEdit(self)
        self._file_gallery = file_gallery

        self.view = QFrame(self)
        self.scrollArea = SmoothScrollArea(self.view)
        self.scrollWidget = QWidget(self.scrollArea)
        self.mesPanel = MesPanel(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.flowLayout = FlowLayout(self.scrollWidget, isTight=False)

        self._cards = []
        self._files = self._file_gallery.unlabeledFiles()
        self._current_idx = -1
        self.__initWidget()

    def addCard(self, icon:FluentIcon, file:LabeledFile):
        card = FileCard(icon, file, self)
        card.clicked.connect(self.__setSelectedFile)
        self._cards.append(card)
        card.show()
        self.flowLayout.addWidget(card)

    def __setSelectedFile(self, file:LabeledFile):
        index = self._files.index(file)
        if self._current_idx >= 0:
            self._cards[self._current_idx].setSelected(False)
        self._current_idx = index
        self._cards[index].setSelected(True)
        self.mesPanel.setMes(file)

    def __initWidget(self):
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setViewportMargins(0, 5, 0, 5)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.addWidget(self.cardViewlabel)
        self.vBoxLayout.addWidget(self.searchLineEdit)
        self.vBoxLayout.addWidget(self.view)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.scrollArea)
        self.hBoxLayout.addWidget(self.mesPanel, 0, Qt.AlignRight)

        self.flowLayout.setVerticalSpacing(8)
        self.flowLayout.setHorizontalSpacing(8)
        self.flowLayout.setContentsMargins(8, 3, 8, 8)

        self.__setQss()

        self.searchLineEdit.clearSignal.connect(self.showAllFiles)
        self.searchLineEdit.searchSignal.connect(self.search)

        for file in self._files:
            self.addCard(FIF.FOLDER, file)

        for file in self._files:
            if not file.isLabeled():
                self.__setSelectedFile(file)
                break

    def __setQss(self):
        self.view.setObjectName('cardView')
        self.scrollWidget.setObjectName('scrollWidget')
        self.cardViewlabel.setObjectName('cardViewLabel')
        StyleSheet.UNLABELED_INTERFACE.apply(self)

    def search(self, keyWord: str):
        indexes = []
        for i, file in enumerate(self._files):
            if file.searchUnlabeled(keyWord):
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
            if not file.isLabeled():
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
    def __init__(self, parent=None, file_gallery:FileGallery = None):
        super().__init__(
            title='未自动分类文件',
            subtitle = 'unlabeled files',
            parent = parent
        )
        self._file_gallery = file_gallery
        self._cardView = CardView(self, file_gallery)
        self.vBoxLayout.addWidget(self._cardView)

