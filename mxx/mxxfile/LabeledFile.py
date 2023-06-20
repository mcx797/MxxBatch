from mxx.mxxfile.File import File
from mxx.mxxrule.RuleGallery import RuleGallery
from mxx.mxxlog.LogFile import auto_log
class LabeledFile(File):
    def __init__(self, file_path, rule_gallery:RuleGallery):
        super().__init__(file_path.path())
        label = rule_gallery.match(self.filePath())
        if label == None:
            self._is_auto_labeled = False
            self._is_labeled = False
            self._labeled_list = []
            self._label = 'Unkonwn'
        else:
            self._is_auto_labeled = True
            self._is_labeled = True
            self._labeled_list = []
            self._labeled_list.append(label)
            self._label = label
        log_dic = {}
        log_dic['path'] = self.filePath()
        log_dic['label'] = self._label
        auto_log.addLog(str(log_dic))

    def isLabeled(self):
        return self._is_labeled

    def label(self):
        return self._label
