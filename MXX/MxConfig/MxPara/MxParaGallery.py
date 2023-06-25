from MXX.MxGallery.MxGallery import MxGallery
from MXX.MxGallery.MxItem import MxItem
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
        else:
            MxLog().wrongLog('para file format wrong in file:{}'.format(json_file.filePath))


class MxParaItem(MxItem):
    def __init__(self, parent, path, name, dic):
        super().__init__(parent, path, name)
        if not isinstance(dic, dict):
            self._name = None
            MxLog().wrongLog('para format wrong in item {}, file: {}'.format(name, path))
            return

        if not self.__loadType(dic):
            self._name = None
            MxLog().wrongLog('para item key type wrong in item: {}, file: {}'.format(name, path))
            return

        if not self.__loadValue(dic):
            self._name = None
            MxLog().wrongLog('para item key value wrong in item: {}, file: {}'.format(name, path))
            return

        if self._type == MxParaType.OPTION:
            if not self.__loadOption(dic):
                self._name = None
                MxLog().wrongLog('para item key option wrong in item: {}, file: {}'.format(name, path))
                return
        elif self._type == MxParaType.COMBO:
            if not self.__loadCombo(dic):
                self._name = None
                MxLog().wrongLog('para item key combo wrong in item: {}, file: {}'.format(name, path))
                return
        return

    def __loadValue(self, dic):
        if 'value' not in dic:
            return False
        if not isinstance(dic['value'], str):
            return False
        self._value = dic['value']
        return True

    def __loadType(self, dic):
        if 'type' not in dic:
            return False
        if not isinstance(dic['type'], str):
            return False
        if dic['type'] == 'str':
            self._type = MxParaType.STR
        elif dic['type'] == 'option':
            self._type = MxParaType.OPTION
        elif dic['type'] == 'combo':
            self._type = MxParaType.COMBO
        else:
            return False
        return True

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
            if not self._parent.isKey(item):
                return False
            self._para.append(self._parent[item])
        return True

    def __str__(self):
        ans = '{{type:{}, value:{}, file:{}}}'.format(self.type, self.value, self.path)
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

    @property
    def type(self):
        return self._type


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

