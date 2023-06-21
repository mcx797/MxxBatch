from PyQt5.QtWidgets import  QHBoxLayout, QFrame, QComboBox, QDialog

class RelabelDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 500)
        self.hBoxLayout = QHBoxLayout(self)
        self._type_box = QComboBox(self)
        self._type_idx = 0
        #self.comboBox = QComboBox()
        self._type_items = [
            '储层参数评价',
            '表套固井水泥胶结评价',
            '技套固井水泥胶结评价',
            '油套固井水泥胶结评价',
            'ECS评价',
            '电成像评价',
            '核磁测井评价',
            '阵列声波评价'
        ]
        self._name_items = [
            [
                '储层参数评价图头信息',
                '储层分类',
                '目的层测井分层',
                '全井段测井分层',
                '可压性综合解释结论',
                '五峰-龙马溪组页岩气储层测井解释成果表',
                '五峰-龙马溪组页岩气连续一类储层测井解释成果表',
                '五峰-龙马溪组页岩气储层小层钻遇率统计表',
                '完井测井解释报告',
                '完井测井解释评价汇报',
                '完井测井解释报告'
            ]
        ]
        self.hBoxLayout.addWidget(self._type_box)
        for i, item in enumerate(self._type_items):
            self._type_box.addItem(item, i)

        self._type_box.currentIndexChanged.connect(self.typeBoxChanged)
        #self._type_box.activated.connect(self.typeBoxChanged())


    def typeBoxChanged(self):
        self._type_idx = self._type_box.currentIndex()
        print(self._type_box.currentIndex())

    def closeEvent(self, e):
        print('dialog closed!')
        print(self._type_box.currentIndex())