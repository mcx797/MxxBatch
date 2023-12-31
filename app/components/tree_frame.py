from PyQt5.QtWidgets import QFrame, QHBoxLayout, QTreeWidgetItem, QTreeWidgetItemIterator

from qfluentwidgets import TreeWidget

from MXX.MxFile.MxReFile import MxReFile

from PyQt5.QtCore import Qt

from MXX.MxPath.MxPath import MxPath

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
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)


        if enableCheck:
            it = QTreeWidgetItemIterator(self.tree)
            while(it.value()):
                it.value().setCheckState(0, Qt.Unchecked)
                it += 1

    def refreshPath(self, path:MxPath):
        self.tree.clear()
        if len(path) != 0:
            item_top = QTreeWidgetItem([self.tr(path[0])])
            item_temp = item_top
            for i in range(1, len(path)):
                item = QTreeWidgetItem([self.tr(path[i])])
                item_temp.addChild(item)
                item_temp = item
            self.tree.addTopLevelItem(item_top)
            self.tree.expandAll()
        self.repaint()

    def refresh(self, file:MxReFile):
        self.tree.clear()
        path_temp = MxPath(cfg.get(cfg.sourceFolder))
        path_file = MxPath(file.filePath)
        self.refreshPath(path_file - (path_temp - 1))
