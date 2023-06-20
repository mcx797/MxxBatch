from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QVBoxLayout, QApplication, QHBoxLayout, \
    QTreeWidgetItem, QTreeWidgetItemIterator

from qfluentwidgets import (SmoothScrollArea, SearchLineEdit, FluentIcon, IconWidget, Theme, isDarkTheme, FlowLayout,
                            PrimaryPushButton, TreeWidget)

from qfluentwidgets import FluentIcon as FIF

from app.view.mxx_interface import MxxInterface

from mxx.mxxfile.FileGallery import FileGallery
from mxx.mxxfile.LabeledFile import LabeledFile
from mxx.mxxfile.File import File
from app.common.style_sheet import StyleSheet
from app.common.config import cfg
from mxx.mxxfile.Path import Path



class LineEdit(SearchLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent = parent)
        self.setPlaceholderText(self.tr('Search files'))
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)


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

        self.button1 = PrimaryPushButton(self.tr('打开文件'))
        self.button2 = PrimaryPushButton(self.tr('打开文件夹'))
        self.button3 = PrimaryPushButton(self.tr('进行分类'))

        self.vBoxLayout.addWidget(self.button3)
        self.vBoxLayout.addWidget(self.button1)
        self.vBoxLayout.addWidget(self.button2)

        #self.button1.clicked.connect(self.openFile)
        #self.button2.clicked.connect(self.openDir)
        #self.button3.clicked.connect(self.Classifier)

    def setMes(self, file:LabeledFile):
        self._file = file
        self.fileNameLabel.setText(file.fileName())
        self.frame.refresh(file)


class Frame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)
        self.setObjectName('frame')

    def addWidget(self, widget):
        self._widget = widget
        self.hBoxLayout.addWidget(widget)

    def clear(self):
        self._widget.clear()
        self.hBoxLayout.removeWidget(self._widget)


class TreeFrame(Frame):
    def __init__(self, parent = None, enableCheck=False):
        super().__init__(parent)
        self.tree = TreeWidget(self)
        self.addWidget(self.tree)
        item1 = QTreeWidgetItem([self.tr('井')])
        item1.addChildren([
            QTreeWidgetItem([self.tr('测井评价资料')])
        ])
        self.tree.addTopLevelItem(item1)
        item2 = QTreeWidgetItem([self.tr('1')])
        item3 = QTreeWidgetItem([self.tr('2')])
        item4 = QTreeWidgetItem([self.tr('3')])
        item2.addChild(item3)
        item3.addChild(item4)
        self.tree.addTopLevelItem(item2)
        self.tree.expandAll()
        self.tree.setHeaderHidden(True)
        self.setFixedSize(550, 400)

        if enableCheck:
            it = QTreeWidgetItemIterator(self.tree)
            while(it.value()):
                it.value().setCheckState(0, Qt.Unchecked)
                it += 1

    def refresh(self, file:LabeledFile):
        self.tree.clear()
        path_temp = Path(cfg.get(cfg.sourceFolder))
        if len(file.path()) != 0:
            itemTop = QTreeWidgetItem([self.tr(file.path()[len(path_temp) - 1])])
            itemTemp = itemTop
            for i in range(len(path_temp), len(file.path())):
                item1 = QTreeWidgetItem([self.tr(file.path()[i])])
                itemTemp.addChild(item1)
                itemTemp = item1
            self.tree.addTopLevelItem(itemTop)
            self.tree.expandAll()


class FileCard(QFrame):
    clicked = pyqtSignal(LabeledFile)

    def __init__(self, icon: FluentIcon, file:LabeledFile, parent=None):
        super().__init__(parent=parent)
        self._icon = icon
        self._file = file
        self.isSelected = False
        self.iconWidget = IconWidget(icon, self)
        self.nameLabel = QLabel(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.setFixedSize(96, 96)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(8, 28, 8, 0)

        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.iconWidget.setFixedSize(28, 28)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignHCenter)
        self.vBoxLayout.addSpacing(14)
        self.vBoxLayout.addWidget(self.nameLabel, 0, Qt.AlignHCenter)

        text = self.nameLabel.fontMetrics().elidedText(file.fileSuffix(), Qt.ElideRight, 78)
        self.nameLabel.setText(text)

    def mouseReleaseEvent(self, e):
        if self.isSelected:
            return

        self.clicked.emit(self._file)

    def setSelected(self, isSelected:bool, force=False):
        if isSelected == self.isSelected and not force:
            return

        self.isSelected = isSelected

        if not isSelected:
            self.iconWidget.setIcon(self._icon)
        else:
            icon = self._icon.icon(Theme.LIGHT if isDarkTheme() else Theme.DARK)
            self.iconWidget.setIcon(icon)

        self.setProperty('isSelected', isSelected)
        self.setStyle(QApplication.style())


class CardView(QWidget):
    def __init__(self, parent = None, file_gallery:FileGallery = None):
        super().__init__(parent=parent)
        self.cardViewlabel = QLabel(self.tr('为自动分类文件'), self)
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

        for file in self._files:
            self.addCard(FIF.FOLDER, file)

        if len(self._files) > 0:
            self.__setSelectedFile(self._files[0])


    def addCard(self, icon:FluentIcon, file:LabeledFile):
        card = FileCard(icon, file, self)
        card.clicked.connect(self.__setSelectedFile)
        self._cards.append(card)
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

    def __setQss(self):
        self.view.setObjectName('cardView')
        self.scrollWidget.setObjectName('scrollWidget')
        self.cardViewlabel.setObjectName('cardViewLabel')
        StyleSheet.UNLABELED_INTERFACE.apply(self)


class UnlabeledInterface(MxxInterface):
    def __init__(self, parent=None, file_gallery:FileGallery = None):
        super().__init__(
            title='未分类文件',
            subtitle = 'unlabeled files',
            parent = parent
        )
        self._file_gallery = file_gallery
        self._cardView = CardView(self, file_gallery)
        self.vBoxLayout.addWidget(self._cardView)

