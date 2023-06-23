from app.view.mxx_interface import MxxInterface
from app.components.home_card import HomeCardView, HomeCard

class TypeLabeledInterface(MxxInterface):
    def __init__(self, parent=None, type_name:str = 'wrong!', name_list:list = []):
        super().__init__(
            title='{}文件'.format(type_name),
            subtitle='all type labeled files',
            parent=parent
        )
        self._name_list = name_list
        self.loadNameList()

    def loadNameList(self):
        self._name_view = {}
        for name in self._name_list:
            self._name_view[name] = HomeCardView(
                self.tr(name), self.view)
            self.vBoxLayout.addWidget(self._name_view[name])
            #self._name_view[name].hide()