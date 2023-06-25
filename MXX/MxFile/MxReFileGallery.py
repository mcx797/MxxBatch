import os

from MXX.MxGallery.MxGallery import MxGallery
from MXX.MxPath.MxPath import MxPath
from MXX.MxFile.MxReFile import MxReFile

class MxReFileGallery(MxGallery):
    def __init__(self, parent, source_path):
        super().__init__(parent)
        if not self.__loadSourceDir(source_path):
            self._root_path = None
            return

    def __loadSourceDir(self, source_path):
        if isinstance(source_path, str):
            self._root_path = MxPath(source_path)
        elif isinstance(source_path, MxPath):
            self._root_path = source_path
        else:
            return False

        self.__loadFiles(self._root_path)

    def __loadFiles(self, path):
        if isinstance(path, str):
            path = path
        elif isinstance(path, MxPath):
            path = path.path
        dir_or_files = os.listdir(path)
        for item in dir_or_files:
            path_temp = path + '/' + item
            if os.path.isdir(path_temp):
                self.__loadFiles(path_temp)
            elif os.path.isfile(path_temp):
                if MxPath(path_temp).fileName[0:2] == '~$':
                    continue
                self.addItem(path_temp, MxReFile(path_temp, self._parent))

    @property
    def labeledFileNum(self):
        ans = 0
        for item in self._items:
            if self._items[item].isLabeled == True:
                ans = ans + 1
        return ans

    @property
    def labeledFiles(self):
        ans = []
        for item in self._items:
            if self._items[item].isLabeled == True:
                ans.append(self._items[item])
        return ans

    @property
    def unlabeledFiles(self):
        ans = []
        for item in self._items:
            if self._items[item].isLabeled == False:
                ans.append(self._items[item])
        return ans

    @property
    def unlabeledFileNum(self):
        ans = 0
        for item in self._items:
            if self._items[item].isLabeled == False:
                ans = ans + 1
        return ans
