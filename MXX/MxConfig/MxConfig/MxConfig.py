import os
from MXX.MxFile.MxJsonFile import MxJsonFile

from app.common.config import Config
from qfluentwidgets import qconfig

from MXX.MxConfig.MxPara.MxParaGallery import MxParaGallery
from MXX.MxConfig.MxIntermediate.MxINTGallery import MxINTGallery
from MXX.MxConfig.MxRule.MxRuleGallery import MxRuleGallery
from MXX.MxFile.MxReFileGallery import MxReFileGallery
from MXX.MxPath.MxPath import MxPath
import shutil

class MxConfig:
    def __init__(self, cfg):
        if isinstance(cfg, Config):
            self.__loadConfig(cfg)

    def __loadConfig(self, cfg):
        self._app_cfg = cfg
        para_dir = cfg.get(cfg.paraFolder)
        INT_dir = cfg.get(cfg.INTFolder)
        rule_dir = cfg.get(cfg.ruleFolder)
        source_dir = cfg.get(cfg.sourceFolder)
        self.__loadParas(para_dir)
        self.__loadINTs(INT_dir)
        self.__loadRules(rule_dir)
        self.__loadFiles(source_dir)

    def reloadFiles(self):
        source_dir = self._app_cfg.get(self._app_cfg)
        self.__loadFiles(source_dir)

    def __loadParas(self, para_dir):
        self._para_gallery = MxParaGallery(self)
        if not os.path.isdir(para_dir):
            return
        for file in os.listdir(para_dir):
            path = para_dir + '/' + file
            json_file = MxJsonFile(path)
            self._para_gallery.loadJsonFile(json_file)

    def __loadINTs(self, INT_dir):
        self._INT_gallery = MxINTGallery(self)
        if not os.path.isdir(INT_dir):
            return
        for file in os.listdir(INT_dir):
            path = INT_dir + '/' + file
            json_file = MxJsonFile(path)
            self._INT_gallery.loadJsonFile(json_file)

    def __loadRules(self, rule_dir):
        self._rule_gallery = MxRuleGallery(self)
        if not os.path.isdir(rule_dir):
            return
        for file in os.listdir(rule_dir):
            path = rule_dir + '/' + file
            json_file = MxJsonFile(path)
            self._rule_gallery.loadJsonFile(json_file)

    def __loadFiles(self, source_dir):
        self._re_file_gallery = MxReFileGallery(self, source_dir)

    def targetPath(self, INT_name):
        return self._INT_gallery[INT_name].value

    def typeFileNum(self, type_name):
        return self._re_file_gallery.typeFileNum(type_name)

    def typeFileList(self, label_name):
        return self._re_file_gallery.typeFileList(label_name)

    def renameAllFiles(self):
        target_dir = self._app_cfg.get(self._app_cfg.targetFolder)
        if not os.path.isdir((target_dir)):
            return False
        target_root_path = MxPath(target_dir)
        for item in self._re_file_gallery.items:
            if self._re_file_gallery[item].isLabeled:
                file = self._re_file_gallery[item]
                target_path = self.targetPath(file.label)
                file_suffix = file.fileNameSuffix
                suffix = file.fileSuffix
                if file_suffix == '':
                    target_path = target_path + '.' + suffix
                else:
                    target_path = target_path + '_' + file_suffix + '.' + suffix
                print(target_path)
                target_path = target_root_path + MxPath(target_path)
                target_path_dir = (target_path - 1).path
                print(target_path_dir)
                if not os.path.exists(target_path_dir):
                    os.makedirs(target_path_dir)
                shutil.copy(file.filePath, target_path.path)

    @property
    def isFilesAllLabeled(self):
        return self._re_file_gallery.isFilesAllLabeled

    @property
    def autoLabeledFiles(self):
        return self._re_file_gallery.autoLabeledFiles

    @property
    def autoUnlabeledFiles(self):
        return self._re_file_gallery.autoUnlabeledFiles

    @property
    def autoLabeledFilesNum(self):
        return len(self._re_file_gallery.autoLabeledFiles)

    @property
    def autoUnlabeledFilesNum(self):
        return len(self._re_file_gallery.autoUnlabeledFiles)

    @property
    def labelDic(self):
        return self._INT_gallery.labelDic()

    @property
    def paraGallery(self):
        return self._para_gallery

    @property
    def INTGallery(self):
        return self._INT_gallery

    @property
    def ruleGallery(self):
        return self._rule_gallery

    @property
    def reFileGallery(self):
        return self._re_file_gallery

    @property
    def labeledFileNum(self):
        return self.reFileGallery.labeledFileNum

    @property
    def unlabeledFileNum(self):
        return self.reFileGallery.unlabeledFileNum

    def matchRule(self, path):
        if isinstance(path, MxPath):
            path = path.filePath
        return self._rule_gallery.match(path)


if __name__ == '__main__':
    cfg = Config()
    qconfig.load('C:/Users/77902/Desktop/LeadingBatch/config/config.json', cfg)
    cfg = MxConfig(cfg)
    print(cfg.paraGallery)
    print(cfg.INTGallery)
    print(cfg.ruleGallery)
    print(cfg.reFileGallery)

