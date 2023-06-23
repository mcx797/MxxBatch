from PyQt5.QtWidgets import QFrame, QHBoxLayout, QTreeWidgetItem, QTreeWidgetItemIterator

from qfluentwidgets import TreeWidget

from MXX.mxxfile.LabeledFile import LabeledFile

from PyQt5.QtCore import Qt

from MXX.mxxfile.Path import Path

from app.common.config import cfg

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
