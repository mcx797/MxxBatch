from MXX.MxFile.MxFile import MxFile
from MXX.MxLog.MxLog import MxLog

class MxReFile(MxFile):
    def __init__(self, path, mx_cfg):
        super().__init__(path)
        label = mx_cfg.matchRule(self.filePath)
        if label == None:
            self._is_auto_labeled = False
            self._is_labeled = False
            self._auto_label = 'did not auto identified'
            self._label = None
        else:
            self._is_auto_labeled = True
            self._is_labeled = False
            self._auto_label = label
            self._label = None
        self._file_name_suffix = ''

    @property
    def fileNameSuffix(self):
        return self._file_name_suffix

    def setFileNameSuffix(self, suffix):
        self._file_name_suffix = suffix

    def setLabel(self, label):
        self._is_labeled = True
        self._label = label
        MxLog().renameLog(self.filePath, label, self.autoLabel)
        return

    def searchAutoUnlabeled(self, key_word):
        if self.isAutoLabeled:
            return False
        if self.isLabeled:
            return False
        path = self._path
        for i in range(len(path)):
            if key_word in path[i]:
                return True
        return False

    def searchAutoLabeled(self, key_word):
        if not self.isAutoLabeled:
            return False
        if self.isLabeled:
            return False
        path = self._path
        for i in range(len(path)):
            if key_word in path[i]:
                return True
        if '_' in self._auto_label:
            items = self._auto_label.split('_')
            for item in items:
                if key_word in item:
                    return True
        else:
            if key_word in self._auto_label:
                return True
        return False

    @property
    def isAutoLabeled(self):
        return self._is_auto_labeled

    @property
    def autoLabel(self):
        return self._auto_label

    @property
    def unkownLabel(self):
        if self.isLabeled:
            return self._label
        if self.isAutoLabeled:
            return self.autoLabel
        return None

    @property
    def isLabeled(self):
        return self._is_labeled

    @property
    def label(self):
        return self._label

    @property
    def labelType(self):
        if '_' in self._label:
            return self._label.split('_')[0]
        else:
            return 'Others'

    @property
    def labelItem(self):
        if '_' in self._label:
            return self._label.split('_')[1]
        else:
            return self._label
