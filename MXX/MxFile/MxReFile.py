from MXX.MxFile.MxFile import MxFile

class MxReFile(MxFile):
    def __init__(self, path, mx_cfg):
        super().__init__(path)
        label = mx_cfg.matchRule(self.filePath)
        if label == None:
            self._is_auto_labeled = False
            self._is_labeled = False
            self._label_list = []
            self._label = 'Unknown'
        else:
            self._is_auto_labeled = True
            self._is_labeled = True
            self._label_list = []
            self._label = label
            self._label_list.append(label)

    @property
    def isLabeled(self):
        return self._is_labeled

    @property
    def label(self):
        return self._label