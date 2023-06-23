from MXX.MxLog.MxLog import MxLog

class MxGallery:
    def __init__(self, parent):
        self._parent = parent
        self._dic = {}

    def addItem(self, name, item):
        if name == None or item == None:
            return
        if name in self._dic:
            return
            MxLog().wrongLog('MXX.MxGallery.MxGallery:item name {} repeat.'.format(name))
        self._dic[name] = item

    def __len__(self):
        return len(self._dic)

    def __getitem__(self, item:str):
        return self._dic[item]

    def __str__(self):
        ans = '{ '
        for name in self._dic:
            ans = ans + '{{name:{}, item:{}}}'.format(name, str(self._dic[name])) + ', '
        ans = ans[:-2] + ' }'
        return ans


class MxItem:
    def __init__(self, parent, path, name):
        self._parent = parent
        self._path = path
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def parent(self):
        return self._parent