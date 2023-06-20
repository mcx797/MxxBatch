from PyQt5.QtCore import Qt, pyqtSignal, QEasingCurve, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, MessageBox,
                            isDarkTheme, PopUpAniStackedWidget, qrouter)
from qfluentwidgets import FluentIcon as FIF
from app.components.frameless_window import FramelessWindow
from app.components.title_bar import CustomTitleBar
from app.common import resource


from app.view.home_interface import HomeInterface
from app.view.setting_interface import SettingInterface
from app.view.mxx_interface import MxxInterface
from app.common.style_sheet import StyleSheet
from app.view.unlabeled_interface import UnlabeledInterface
from app.view.labeled_interface import LabeledInterface

from app.common.config import cfg
from mxx.mxxfile.Path import Path as MxxPath
from mxx.mxxintermediate.IntermediateConfig import Config as INTConfig
from mxx.mxxfile.JsonFile import JsonFile as MxxJsonFile
from mxx.mxxrule.RuleGallery import RuleGallery
from mxx.mxxfile.FileGallery import FileGallery
from mxx.mxxlog.LogFile import wrong_log

class StackedWidget(QFrame):
    """ Stacked widget """

    currentWidgetChanged = pyqtSignal(QWidget)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(
            lambda i: self.currentWidgetChanged.emit(self.view.widget(i)))
    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)
    def setCurrentWidget(self, widget, popOut=True):
        widget.verticalScrollBar().setValue(0)
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.InQuad)
    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class MainWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        ''' Initial Title Bar '''
        self.setTitleBar(CustomTitleBar(self))

        ''' Initial Widgets '''
        self.hBoxLayout = QHBoxLayout(self)
        self.widgetLayout = QHBoxLayout()

        self.stackWidget = StackedWidget(self)
        self.navigationInterface = NavigationInterface(self, True, True)

        INT_path = MxxPath(cfg.get(cfg.INTFile))
        self._INTConfig = INTConfig(MxxJsonFile(INT_path.filePath()))
        if self._INTConfig != None and not self._INTConfig.isConfig():
            self._INTConfig = None

        if self._INTConfig != None:
            rule_path = MxxPath(cfg.get(cfg.ruleFile))
            self._ruleGallery = RuleGallery(MxxJsonFile(rule_path.filePath()), self._INTConfig.INTGallery())
        else:
            self._ruleGallery = None

        source_path = MxxPath(cfg.get(cfg.sourceFolder))
        self._file_gallery = FileGallery(source_path, self._ruleGallery)


        self._homeInterface = HomeInterface(self)
        self._settingInterface = SettingInterface(self)
        self._unlabeledInterface = UnlabeledInterface(self, self._file_gallery)
        self._labeledInterface = LabeledInterface(self)

        ''' Initialization '''
        self.initLayout()

        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)
        self.hBoxLayout.setStretchFactor(self.widgetLayout, 1)

        self.widgetLayout.addWidget(self.stackWidget)
        self.widgetLayout.setContentsMargins(0, 48, 0, 0)

        #signalBus.switchToSampleCard.connect(self.switchToSample)

        self.navigationInterface.displayModeChanged.connect(
            self.titleBar.raise_)
        self.titleBar.raise_()

    def initNavigation(self):
        self.addSubInterface(
            self._homeInterface, 'homeInterface', FIF.HOME, self.tr('Home'), NavigationItemPosition.TOP)

        self.addSubInterface(
            self._labeledInterface, 'labeledInterface', FIF.FOLDER, self.tr('labeled'), NavigationItemPosition.TOP)

        self.addSubInterface(
            self._unlabeledInterface, 'unlabeledInterface', FIF.FOLDER, self.tr('Unlabeled'), NavigationItemPosition.TOP)

        self.addSubInterface(
            self._settingInterface, 'settingInterface', FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

        # !IMPORTANT: don't forget to set the default route key if you enable the return button
        qrouter.setDefaultRouteKey(self.stackWidget, self._homeInterface.objectName())

        self.stackWidget.currentWidgetChanged.connect(self.onCurrentWidgetChanged)
        self.navigationInterface.setCurrentItem(
            self._homeInterface.objectName())
        self.stackWidget.setCurrentIndex(0)

    def initWindow(self):
        self.resize(960, 680)
        self.setMinimumWidth(960)
        self.setMaximumWidth(1060)
        self.setMinimumHeight(680)
        self.setWindowIcon(QIcon(':/LeadingBatch/logo.png'))
        self.setWindowTitle('  LeadingBatch')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(30, 30)

        StyleSheet.MAIN_WINDOW.apply(self)

    def addSubInterface(self, interface: QWidget, objectName: str, icon, text: str, position=NavigationItemPosition.SCROLL):
        """ add sub interface """
        interface.setObjectName(objectName)
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=objectName,
            icon=icon,
            text=text,
            onClick=lambda t: self.switchTo(interface, t),
            position=position,
            tooltip=text
        )

    def onCurrentWidgetChanged(self, widget: QWidget):
        self.navigationInterface.setCurrentItem(widget.objectName())
        qrouter.push(self.stackWidget, widget.objectName())

    def resizeEvent(self, e):
        self.titleBar.move(46, 0)
        self.titleBar.resize(self.width()-46, self.titleBar.height())

    def switchTo(self, widget, triggerByUser=True):
        self.stackWidget.setCurrentWidget(widget, not triggerByUser)

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(MxxInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
