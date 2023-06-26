from PyQt5.QtWidgets import  QHBoxLayout, QFrame, QComboBox, QDialog, QVBoxLayout
from qfluentwidgets import PrimaryPushButton
from PyQt5.QtCore import QCoreApplication

class RelabelDialog(QDialog):
    def __init__(self, label_dic):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setWindowTitle('更改分类')
        self.vBoxLayout = QVBoxLayout(self)

        self._type_box = QComboBox(self)
        self._item_box = QComboBox(self)
        self._type_idx = 0
        self._label_dic = label_dic
        #self.comboBox = QComboBox()
        self._ok_button = PrimaryPushButton(self.tr('ok!'))
        self._cancel_button = PrimaryPushButton(self.tr('cancel'))
        self._is_ok = False

        self.__initWidget()

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
        self.vBoxLayout.addWidget(self._type_box)
        self.vBoxLayout.addWidget(self._item_box)
        self.vBoxLayout.addWidget(self._ok_button)
        self.vBoxLayout.addWidget(self._cancel_button)

        for i, item in enumerate(self._label_dic):
            self._type_box.addItem(item, i)

        if (len(self._label_dic) > 0):
            idx = self._type_box.currentIndex()
            self._type_name = self._type_box.itemText(idx)
            for i, item in enumerate(self._label_dic[self._type_box.itemText(idx)]):
                self._item_box.addItem(item, i)
            for item in self._label_dic:
                if len(self._label_dic[item]) > 0:
                    idx = self._item_box.currentIndex()
                    self._item_name = self._item_box.itemText(idx)
                break

        if (len(self._label_dic) > 0):
            self._type_name = self._type_box.itemText(0)


    def typeBoxChanged(self):
        self._type_idx = self._type_box.currentIndex()
        self._type_name = self._type_box.itemText(self._type_idx)
        self._item_box.clear()
        for i, item in enumerate(self._label_dic[self._type_name]):
            self._item_box.addItem(item, i)

    def itemBoxChanged(self):
        self._item_idx = self._item_box.currentIndex()
        self._item_name = self._item_box.itemText(self._item_idx)

    @property
    def isOk(self):
        return self._is_ok

    @property
    def typeName(self):
        return '{}_{}'.format(self._type_name, self._item_name)