from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget
from MXX.MxFile.MxReFile import MxReFile
from PyQt5.QtCore import Qt

from qfluentwidgets import SmoothScrollArea
from app.components.tree_frame import TreeFrame

class PostLabelDialog(QDialog):
    def __init__(self, file:MxReFile):
        super().__init__()
        self._file = file


        self.setFixedSize(800, 800)
        self.setWindowTitle('后处理')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.scrollArea = SmoothScrollArea(self.view)
        self.scrollWidget = QWidget(self.scrollArea)
        self.frame = TreeFrame(self, False)

        self.__initWidget()


    def __initWidget(self):
        self.vBoxLayout.setContentsMargins(15, 5, 5, 5)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.addWidget(self.frame)