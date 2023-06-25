from MXX.MxGallery.MxGallery import MxGallery
from MXX.MxGallery.MxItem import MxItem
from MXX.MxLog.MxLog import MxLog

class MxINTGallery(MxGallery):
    def __init__(self, parent):
        super().__init__(parent)

    def loadJsonFile(self, json_file):
        con = json_file.fileContent
        if isinstance(con, dict):
            for name in con:
                if self.isKey(name):
                    continue
                item = MxINTItem(self, json_file.filePath, name, con[name], self._parent)
                if item.name != None:
                    self.addItem(name, item)
        else:
            MxLog().wrongLog('INT file format wrong in file: {}'.format(json_file.filePath))

    def labelDic(self):
        ans = {}
        for item in self._items:
            if '_' in item:
                item_name = item.split('_')
                type_name = item_name[0]
                item_name = item_name[1]
                if type_name in ans:
                    ans[type_name].append(item_name)
                else:
                    ans[type_name] = []
                    ans[type_name].append(item_name)
            else:
                if 'Other' in ans:
                    ans['Other'].append(item)
                else:
                    ans['Other'] = []
                    ans['Other'].append(item)
        return ans


class MxINTItem(MxItem):
    def __init__(self, parent, path, name, dic, config):
        super().__init__(parent, path, name)
        if not isinstance(dic, dict):
            self._name = None
            MxLog().wrongLog('MxINTGallery: INT format wrong in item: {}, file: {}'.format(name, path))
            return
        if not self.__loadPath(dic):
            self._name = None
            MxLog().wrongLog('INT item key path wrong in item: {}, path: {}'.format(name, path))
            return
        if not self.__loadPara(dic, config):
            self._name = None
            MxLog().wrongLog('INT item key para wrong in item: {}, file: {}'.format(name, path))
            return

    def __loadPath(self, dic):
        if 'path' not in dic:
            return False
        if not isinstance(dic['path'], str):
            return False
        self._value = dic['path']
        return True

    def __loadPara(self, dic, config):
        if 'para' not in dic:
            return False
        if not isinstance(dic['para'], list):
            return False
        self._para = []
        for item in dic['para']:
            if not isinstance(item, str):
                return False
            if not config.paraGallery.isKey(item):
                return False
            self._para.append(config.paraGallery[item])
        return True

    def __str__(self):
        ans = '{{path:{}}}'.format(self.value)
        return ans
    @property
    def value(self):
        para_list = []
        for item in self._para:
            para_list.append(item.value)
        return self._value.format(para_list)


