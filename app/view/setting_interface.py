from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog
from qfluentwidgets import (ScrollArea, ExpandLayout, SettingCardGroup,
                            RangeSettingCard, OptionsSettingCard, CustomColorSettingCard,
                            ComboBoxSettingCard, PushSettingCard)
from qfluentwidgets import FluentIcon as FIF
from app.common.style_sheet import StyleSheet
from app.common.config import cfg
from app.common.signal_bus import signalBus


class SettingInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("Settings"), self)

        # folder group

        self.folderGroup = SettingCardGroup(
            self.tr("配置文件夹"), self.scrollWidget)

        self.paraFolderCard = PushSettingCard(
            self.tr('Choose folder'),
            FIF.FOLDER,
            self.tr('para directory'),
            cfg.get(cfg.paraFolder),
            self.folderGroup
        )

        self.INTFolderCard = PushSettingCard(
            self.tr('Choose folder'),
            FIF.FOLDER,
            self.tr('INT directory'),
            cfg.get(cfg.INTFolder),
            self.folderGroup
        )

        self.ruleFolderCard = PushSettingCard(
            self.tr('Choose folder'),
            FIF.FOLDER,
            self.tr('rule directory'),
            cfg.get(cfg.ruleFolder),
            self.folderGroup
        )

        self.sourceFolderCard = PushSettingCard(
            self.tr('Choose folder'),
            FIF.FOLDER,
            self.tr('source directory'),
            cfg.get(cfg.sourceFolder),
            self.folderGroup
        )

        self.targetFolderCard = PushSettingCard(
            self.tr('Choose folder'),
            FIF.FOLDER,
            self.tr('target directory'),
            cfg.get(cfg.targetFolder),
            self.folderGroup
        )


        # personalization
        self.personalGroup = SettingCardGroup(
            self.tr('Personalization'), self.scrollWidget)
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("Use system setting")
            ],
            parent=self.personalGroup
        )
        self.languageCard = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('Language'),
            self.tr('Set your preferred language for UI'),
            texts=['简体中文', '繁體中文', 'English', self.tr('Use system setting')],
            parent=self.personalGroup
        )

        # material
        self.materialGroup = SettingCardGroup(
            self.tr('Material'), self.scrollWidget)
        self.blurRadiusCard = RangeSettingCard(
            cfg.blurRadius,
            FIF.ALBUM,
            self.tr('Acrylic blur radius'),
            self.tr('The greater the radius, the more blurred the image'),
            self.materialGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        self.folderGroup.addSettingCard(self.paraFolderCard)
        self.folderGroup.addSettingCard(self.INTFolderCard)
        self.folderGroup.addSettingCard(self.ruleFolderCard)
        self.folderGroup.addSettingCard(self.sourceFolderCard)
        self.folderGroup.addSettingCard(self.targetFolderCard)

        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        self.personalGroup.addSettingCard(self.languageCard)

        self.materialGroup.addSettingCard(self.blurRadiusCard)

        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.folderGroup)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.materialGroup)

    def __connectSignalToSlot(self):
        self.paraFolderCard.clicked.connect(
            lambda : self.__onFolderCardClicked('para', cfg.paraFolder, signalBus.paraFolderChangedSignal))

        self.INTFolderCard.clicked.connect(
            lambda : self.__onFolderCardClicked('INT', cfg.INTFolder, signalBus.INTFolderChangedSignal))

        self.ruleFolderCard.clicked.connect(
            lambda : self.__onFolderCardClicked('rule', cfg.ruleFolder, signalBus.ruleFolderChangedSignal))

        self.sourceFolderCard.clicked.connect(
            lambda : self.__onFolderCardClicked('source', cfg.sourceFolder, signalBus.sourceFolderChangedSignal))

        self.targetFolderCard.clicked.connect(
            lambda : self.__onFolderCardClicked('target', cfg.targetFolder, signalBus.targetFolderChangedSignal))

        signalBus.INTFolderChangedSignal.connect(self.__refreshContent)
        signalBus.ruleFolderChangedSignal.connect(self.__refreshContent)
        signalBus.paraFolderChangedSignal.connect(self.__refreshContent)
        signalBus.sourceFolderChangedSignal.connect(self.__refreshContent)
        signalBus.targetFolderChangedSignal.connect(self.__refreshContent)


    def __refreshContent(self):
        self.paraFolderCard.setContent(cfg.get(cfg.paraFolder))
        self.INTFolderCard.setContent(cfg.get(cfg.INTFolder))
        self.ruleFolderCard.setContent(cfg.get(cfg.ruleFolder))
        self.sourceFolderCard.setContent(cfg.get(cfg.sourceFolder))
        self.targetFolderCard.setContent(cfg.get(cfg.targetFolder))

    def __onFolderCardClicked(self, name, cfg_item, signal):
        folder = QFileDialog.getExistingDirectory(
            self, self.tr('Choose folder', './config/{}'.format(name)))
        if not folder or cfg.get(cfg_item) == folder:
            return
        cfg.set(cfg_item, folder)
        signal.emit()

