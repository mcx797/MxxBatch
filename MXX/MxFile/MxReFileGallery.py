import os

from MXX.MxGallery.MxGallery import MxGallery
from MXX.MxPath.MxPath import MxPath
from MXX.MxFile.MxReFile import MxReFile

class MxReFileGallery(MxGallery):
    def __init__(self, parent, source_path):
        super().__init__(parent)
        self._type_dic = None
        self._is_all_labeled = False

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

        if not os.path.isdir(source_path):
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

    def __getitem__(self, item):
        return self._items[item]

    def __load_type_dic(self):
        ans = {}
        for item in self._items:
            label = self._items[item].label
            if '_' in label:
                label_type = label.split('_')[0]
                label_name = label.split('_')[1]
            else:
                label_type = 'Others'
                label_name = label
            if label_type not in ans:
                ans[label_type] = {}
                ans[label_type][label_name] = []
                ans[label_type][label_name].append(self._items[item])
            else:
                if label_name not in ans[label_type]:
                    ans[label_type][label_name] = []
                    ans[label_type][label_name].append(self._items[item])
                else:
                    ans[label_type][label_name].append(self._items[item])
        self._type_dic = ans
        return

    def typeFileNum(self, type_name):
        if self._type_dic == None:
            self.__load_type_dic()
        ans = 0
        if type_name not in self._type_dic:
            return 0
        for item in self._type_dic[type_name]:
            ans = ans + len(self._type_dic[type_name][item])
        return ans

    def typeFileList(self, label_name):
        if self._type_dic == None:
            self.__load_type_dic()
        if '_' in label_name:
            type_name = label_name.split('_')[0]
            item_name = label_name.split('_')[1]
        else:
            type_name = "Others"
            item_name = label_name
        if type_name not in self._type_dic:
            return []
        if item_name not in self._type_dic[type_name]:
            return []
        return self._type_dic[type_name][item_name].copy()

    @property
    def isFilesAllLabeled(self):
        if self._is_all_labeled == True:
            return True
        for item in self._items:
            if self[item].isLabeled == False:
                return False
        self._is_all_labeled = True
        return True

    @property
    def labeledFileNum(self):
        ans = 0
        for item in self._items:
            if self[item].isLabeled == True:
                ans = ans + 1
        return ans

    @property
    def labeledFiles(self):
        ans = []
        for item in self._items:
            if self[item].isLabeled == True:
                ans.append(self[item])
        return ans

    @property
    def unlabeledFiles(self):
        ans = []
        for item in self._items:
            if self[item].isLabeled == False:
                ans.append(self[item])
        return ans

    @property
    def unlabeledFileNum(self):
        ans = 0
        for item in self._items:
            if self[item].isLabeled == False:
                ans = ans + 1
        return ans

    @property
    def autoLabeledFiles(self):
        ans = []
        for item in self._items:
            if self[item].isAutoLabeled == True:
                ans.append(self[item])
        return ans

    @property
    def autoUnlabeledFiles(self):
        ans = []
        for item in self._items:
            if self[item].isAutoLabeled == False:
                ans.append(self[item])
        return ans

