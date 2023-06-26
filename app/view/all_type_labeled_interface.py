from app.view.mxx_interface import MxxInterface
from app.components.labeled_file_card import LabeledFileCard, LabeledFileCardView
from app.common.signal_bus import signalBus
from MXX.MxConfig.MxConfig.MxConfig import MxConfig
from MXX.MxFile.MxReFile import MxReFile
class AllTypeLabeledInterface(MxxInterface):
    def __init__(self, parent=None, mx_cfg:MxConfig = None, type_dic:dict = {}):
        super().__init__(
            parent=parent,
            title='全类型文件',
            subtitle = 'all type labeled files',
            mx_cfg = mx_cfg
        )
        self._type_dic = type_dic
        self.loadTypeDic()
        signalBus.fileLabeledSignal.connect(self.__addFileCard)

    def __addFileCard(self, file:MxReFile):
        self._type_view[file.labelType].show()
        self._type_view[file.labelType].addCard(file)

    def loadTypeDic(self):
        self._type_view = {}
        for type in self._type_dic:
            self._type_view[type] = LabeledFileCardView(
                 self.view, self.tr(type))
            self.vBoxLayout.addWidget(self._type_view[type])
            self._type_view[type].hide()

