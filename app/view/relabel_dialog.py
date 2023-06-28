from PyQt5.QtWidgets import  QHBoxLayout, QFrame, QComboBox, QDialog, QVBoxLayout
from qfluentwidgets import PrimaryPushButton, ComboBox
from PyQt5.QtCore import QCoreApplication
from app.common.style_sheet import StyleSheet
from PyQt5.QtCore import Qt

class RelabelDialog(QDialog):
    def __init__(self, label_dic):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setWindowTitle('更改分类')
        self.vBoxLayout = QVBoxLayout(self)

        self._type_box = ComboBox(self)
        self._item_box = ComboBox(self)
        self._label_dic = label_dic


        self._ok_button = PrimaryPushButton(self.tr('ok!'))
        self._cancel_button = PrimaryPushButton(self.tr('cancel'))
        self._is_ok = False

        self.__initWidget()
        StyleSheet.RELABEL_DIALOG.apply(self)


        self._type_box.currentIndexChanged.connect(self.typeBoxChanged)
        self._item_box.currentIndexChanged.connect(self.itemBoxChanged)
        self._ok_button.clicked.connect(self.__okButtonClicked)
        self._cancel_button.clicked.connect(self.__cancelButtonClicked)

    def __okButtonClicked(self):
        self._is_ok = True
        self.close()


    def __cancelButtonClicked(self):
        self._is_ok = False
        self.close()

    def __initWidget(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.vBoxLayout.addWidget(self._type_box)
        self.vBoxLayout.addWidget(self._item_box)
        self.vBoxLayout.addWidget(self._ok_button)
        self.vBoxLayout.addWidget(self._cancel_button)

        self._type_box.setMinimumWidth(110)
        self._item_box.setMinimumWidth(110)

        type_temp = []
        for i, item in enumerate(self._label_dic):
            type_temp.append(item)
        if len(self._label_dic) > 0:
            self._type_box.addItems(type_temp)
            self._type_box.setCurrentIndex(0)
            self._type_name = self._type_box.currentText()
            item_temp = self._label_dic[self._type_box.currentText()]
            if len(item_temp) > 0:
                self._item_box.addItems(item_temp)
                self._item_box.setCurrentIndex(0)
                self._item_name = self._item_box.currentText()

    def typeBoxChanged(self):
        self._type_idx = self._type_box.currentIndex()
        self._type_name = self._type_box.currentText()
        self._item_box.clear()
        self._item_box.addItems(self._label_dic[self._type_name])
        self._item_box.setCurrentIndex(0)

    def itemBoxChanged(self):
        self._item_idx = self._item_box.currentIndex()
        self._item_name = self._item_box.currentText()

    @property
    def isOk(self):
        return self._is_ok

    @property
    def typeName(self):
        return '{}_{}'.format(self._type_name, self._item_name)