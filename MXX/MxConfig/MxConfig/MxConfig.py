import os
from MXX.MxFile.MxJsonFile import MxJsonFile

from app.common.config import Config
from app.common.config import cfg as qcfg

from MXX.MxConfig.MxPara.MxParaGallery import MxParaGallery
from MXX.MxConfig.MxIntermediate.MxINTGallery import MxINTGallery


class MxConfig:
    def __init__(self, cfg):
        if isinstance(cfg, Config):
            self.__loadConfig(cfg)


    def __loadConfig(self, cfg):
        INT_dir = cfg.get(cfg.INTFolder)
        rule_dir = cfg.get(cfg.ruleFolder)
        para_dir = cfg.get(cfg.paraFolder)
        self.__loadParas(para_dir)
        self.__loadINTs(INT_dir)

    def __loadINTs(self, INT_dir):
        self._INT_gallery = MxINTGallery(self)
        for file in os.listdir(INT_dir):
            path = INT_dir + '/' + file
            json_file = MxJsonFile(path)
            self._INT_gallery.loadJsonFile(json_file)
            print(self._INT_gallery)
            print(len(self._INT_gallery))

    def __loadParas(self, para_dir):
        self._para_gallery = MxParaGallery(self)
        for file in os.listdir(para_dir):
            path = para_dir + '/' + file
            json_file = MxJsonFile(path)
            self._para_gallery.loadJsonFile(json_file)
            print(self._para_gallery)
            print(len(self._para_gallery))



if __name__ == '__main__':
    cfg = MxConfig(qcfg)