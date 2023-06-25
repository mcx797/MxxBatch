from MXX.MxLog.MxLog import MxLog
from MXX.MxGallery.MxGallery import MxGallery

class MxListGallery(MxGallery):
    def __init__(self, parent):
        super().__init__(parent)
        self._items = []

    def addItem(self, item):
        self._items.append(item)

    def __len__(self):
        super().__len__()

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._items[item]

    def __str__(self):
        ans = '[ '
        for item in self._items:
            ans = ans + str(item) + ', '
        ans = ans[:-2] + ' ]'
        return ans

