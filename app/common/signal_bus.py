# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal


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


signalBus = SignalBus()