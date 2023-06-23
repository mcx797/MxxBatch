from app.view.mxx_interface import MxxInterface
from app.components.home_card import HomeCardView, HomeCard
class AllTypeLabeledInterface(MxxInterface):
    def __init__(self, parent=None, type_dic:dict = {}):
        super().__init__(
            title='全类型文件',
            subtitle = 'all type labeled files',
            parent=parent
        )
        self._type_dic = type_dic
        self.loadTypeDic()

    def loadTypeDic(self):
        self._type_view = {}
        for type in self._type_dic:
            self._type_view[type] = HomeCardView(
                self.tr(type), self.view)
            self.vBoxLayout.addWidget(self._type_view[type])

