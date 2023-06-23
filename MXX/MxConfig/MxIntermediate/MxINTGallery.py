from MXX.MxGallery.MxGallery import MxGallery, MxItem
from MXX.MxLog.MxLog import MxLog

class MxINTGallery(MxGallery):
    def __init__(self, parent):
        super().__init__(parent)

    def loadJsonFile(self, json_file):
        con = json_file.fileContent
        if isinstance(con, dict):
            for name in con:
                item = MxINTItem(self, json_file.filePath, name, con[name])
                if item.name != None:
                    self.addItem(item)

class MxINTItem(MxItem):
    def __init__(self, parent, path, name, dic):
        super().__init__(parent, path, name)
        if not isinstance(dic, dict):
            

