from MXX.MxLog.MxLog import MxLog
from MXX.MxGallery.MxItem import MxItem

class MxGallery:
    def __init__(self, parent):
        self._parent = parent
        self._items = {}

    def addItem(self, name, item):
        if name == None or item == None:
            return
        if name in self._items:
            MxLog().wrongLog('MXX.MxGallery.MxGallery:item name {} repeat.'.format(name))
            return
        self._items[name] = item

    @property
    def items(self):
        ans = []
        for item in self._items:
            ans.append(item)
        return ans

    def __len__(self):
        return len(self._items)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._items[item]
        elif isinstance(item, MxItem):
            return self._items[MxItem.name]

    def __str__(self):
        ans = '[ '
        for name in self._items:
            ans = ans + '{{name:{}, item:{}}}'.format(name, str(self._items[name])) + ', '
        ans = ans[:-2] + ' ]'
        return ans

    def isKey(self, name):
        return name in self._items

