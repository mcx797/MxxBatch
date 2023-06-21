import os

from mxx.mxxgallery.Gallery import Gallery
from mxx.mxxfile.Path import Path
from mxx.mxxfile.LabeledFile import LabeledFile
from mxx.mxxlog.LogFile import auto_log

class FileGallery(Gallery):
    def __init__(self, root_path, rule_gallery):
        super().__init__()
        self._path = root_path
        self._rule_gallery = rule_gallery
        if self._rule_gallery == None:
            return
        self.__loadFiles(self._path)

    def __str__(self):
        ans = '['
        for item in self._gallery:
            ans = ans + str(item) + ', '
        ans = ans[:-2] + ']'
        return ans

    def __loadFiles(self, path):
        dir_or_files = os.listdir(path.path())
        for item in dir_or_files:
            path_temp = Path(path.path() + '\\' + item)
            if os.path.isdir(path_temp.path()):
                self.__loadFiles(path_temp)
            elif os.path.isfile(path_temp.path()):
                if path_temp.fileName()[0:2] == '~$':
                    continue
                self.addItem(LabeledFile(path_temp, self._rule_gallery))

    def unlabeledFiles(self):
        ans = []
        for item in self._gallery:
            if item.isLabeled() == False:
                ans.append(item)
        return ans

    def gallery(self):
        return self._gallery

    def labeledFiles(self):
        ans = []
        for item in self._gallery:
            if item.isLabeled() == True:
                ans.append(item)
        return ans