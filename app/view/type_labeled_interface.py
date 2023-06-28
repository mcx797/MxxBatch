from app.view.mxx_interface import MxxInterface
from app.components.home_card import HomeCardView, HomeCard
from MXX.MxConfig.MxConfig.MxConfig import MxConfig
from app.common.signal_bus import signalBus

from MXX.MxFile.MxReFile import MxReFile
from app.components.labeled_file_card import LabeledFileCardView, LabeledFileCard
from app.common.style_sheet import StyleSheet


class TypeLabeledInterface(MxxInterface):
    def __init__(self, parent=None, mx_cfg: MxConfig = None, type_name:str = 'wrong!', name_list:list = []):
        super().__init__(
            parent=parent,
            title='{}文件'.format(type_name),
            subtitle='{} type files'.format(type_name),
            mx_cfg = mx_cfg
        )
        self._type_name = type_name
        self._name_list = name_list
        self.loadNameList()
        self.vBoxLayout.addStretch(1)
        signalBus.fileLabeledSignal.connect(self.__addFileCard)
        signalBus.fileUnlabeledSignal.connect(self.__deleteFileCard)

    def __addFileCard(self, file:MxReFile, parent:MxxInterface):
        if self._type_name == file.labelType:
            self._name_view[file.labelItem].show()
            self._name_view[file.labelItem].addCard(file)
            if len(self._name_view[file.labelItem]) > 1:
                parent.showFileRepeat(file.unkownLabel)


    def __deleteFileCard(self, file:MxReFile):
        if self._type_name == file.labelType:
            self._name_view[file.labelItem].deleteCard(file)
            if len(self._name_view[file.labelItem]) == 0:
                self._name_view[file.labelItem].hide()

    def loadNameList(self):
        self._name_view = {}
        for name in self._name_list:
            self._name_view[name] = LabeledFileCardView(self, self.tr(name), self._mx_cfg)
            self.vBoxLayout.addWidget(self._name_view[name])
            self._name_view[name].hide()

