# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal
from MXX.MxFile.MxReFile import MxReFile
from qfluentwidgets import ScrollArea


class SignalBus(QObject):
    """ Signal bus """

    switchToSampleCard = pyqtSignal(str)
    supportSignal = pyqtSignal()

    '''folder changed signal'''
    sourceFolderChangedSignal = pyqtSignal()
    targetFolderChangedSignal = pyqtSignal()
    paraFolderChangedSignal = pyqtSignal()
    INTFolderChangedSignal = pyqtSignal()
    ruleFolderChangedSignal = pyqtSignal()
    logFolderChangedSignal = pyqtSignal()

    autoUnlabeledSignal = pyqtSignal()
    autoLabeledSignal = pyqtSignal()

    homeMesRefresh = pyqtSignal()
    fileLabeledSignal = pyqtSignal(MxReFile, ScrollArea)
    fileUnlabeledSignal = pyqtSignal(MxReFile)


signalBus = SignalBus()