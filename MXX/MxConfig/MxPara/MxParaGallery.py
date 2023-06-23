from MXX.MxGallery.MxGallery import MxGallery, MxItem
from MXX.MxFile.MxJsonFile import MxJsonFile
from MXX.MxLog.MxLog import MxLog
from enum import Enum

class MxParaGallery(MxGallery):
    def __init__(self, parent):
        super().__init__(parent)

    def loadJsonFile(self, json_file):
        con = json_file.fileContent
        if isinstance(con, dict):
            for name in con:
                item = MxParaItem(self, json_file.filePath, name, con[name])
                if item.name != None:
                    self.addItem(name, item)


class MxParaItem(MxItem):
    def __init__(self, parent, path, name, dic):
        super().__init__(parent, path, name)
        if not isinstance(dic, dict):
            self._name = None
            MxLog().wrongLog('para format wrong in item {}, file: {}'.format(name, path))
            return
        if 'type' not in dic:
            self._name = None
            MxLog().wrongLog('para item has no key type in item: {}, file: {}'.format(name, path))
            return
        if not isinstance(dic['type'], str):
            self._name = None
            MxLog.wrongLog('para item key type wrong in item: {}, file: {}'.format(name, path))
        if 'value' not in dic:
            self._name = None
            MxLog().wrongLog('para item has no key value in item: {}, file: {}'.format(name, path))
            return
        if not isinstance(dic['value'], str):
            self._name = None
            MxLog().wrongLog('para item key str wrong in item: {}, file: {}'.format(name, path))
            return
        self._value = dic['value']
        if dic['type'] == 'str':
            self._type = MxParaType.STR
        elif dic['type'] == 'option':
            self._type = MxParaType.OPTION
            if not self.__loadOption(dic):
                self._name = None
                MxLog().wrongLog('para item key option wrong in item: {}, file: {}'.format(name, path))
                return
        elif dic['type'] == 'combo':
            if not self.__loadCombo(dic):
                self._name = None
                MxLog().wrongLog('para item key combo wrong in item: {}, file: {}'.format(name, path))
                return
            self._type = MxParaType.COMBO
        else:
            MxLog().wrongLog('para item has unknown type in item: {}, file: {}'.format(name, path))
            return

    def __loadOption(self, dic):
        if 'option' not in dic:
            return False
        if not isinstance(dic['option'], list):
            return False
        self._option = []
        for item in dic['option']:
            if not isinstance(item, str):
                return False
            self._option.append(item)
        return True

    def __loadCombo(self, dic):
        if 'para' not in dic:
            return False
        if not isinstance(dic['para'], list):
            return False
        self._para = []
        for item in dic['para']:
            if not isinstance(item, str):
                return False
            if item not in self._parent._dic:
                return False
            self._para.append(self._parent[item])
        return True

    def __str__(self):
        ans = '{{file:{}, name:{}, type:{}, value:{}}}'.format(self._path, self._name, self._type, self.value)
        return ans

    @property
    def value(self):
        if self._type == MxParaType.COMBO:
            para_list = []
            for item in self._para:
                para_list.append(item.value)
            return self._value.format(para_list)
        else:
            return self._value


class MxParaType(Enum):
    STR = 0
    OPTION = 1
    COMBO = 2


if __name__ == '__main__':
    paras = MxParaGallery(None)
    path = 'C:/Users/77902/Desktop/LeadingBatch/config/para/para.json'
    file = MxJsonFile(path)
    paras.loadJsonFile(file)
    print(paras)