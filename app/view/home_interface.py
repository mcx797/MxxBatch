from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QColor, QBrush
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon, InfoBar

from app.common.style_sheet import StyleSheet
from app.components.link_card import LinkCardView, LinkCard
from app.common.config import cfg
from app.common.signal_bus import signalBus

from app.common import src

from app.components.home_card import HomeFileCardView, HomeFileCard, HomeTypeCard, HomeTypeCardView
from app.components.home_para_card import HomeParaCard, HomeParaCardView

from qfluentwidgets import FluentIcon as FIF
from MXX.MxFile.MxReFile import MxReFile
from MXX.MxConfig.MxPara.MxParaGallery import MxParaGallery, MxParaType


class BannerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)
        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('Config Gallery', self)
        self.banner = QPixmap(':/MXX/images/header1.png')
        self.linkCardView = LinkCardView(self)
        self.galleryLabel.setObjectName('galleryLabel')
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            FluentIcon.FOLDER,
            self.tr('源文件夹'),
            cfg.sourceFolder,
            signalBus.sourceFolderChangedSignal,
            ''
        )

        self.linkCardView.addCard(
            FluentIcon.FOLDER,
            self.tr('目标文件夹'),
            cfg.targetFolder,
            signalBus.targetFolderChangedSignal,
            ''
        )

        self.linkCardView.addCard(
            FluentIcon.CODE,
            self.tr('参数文件夹'),
            cfg.paraFolder,
            signalBus.paraFolderChangedSignal,
            '/para'
        )

        self.linkCardView.addCard(
            FluentIcon.CODE,
            self.tr('INT文件夹'),
            cfg.INTFolder,
            signalBus.INTFolderChangedSignal,
            '/INT'
        )

        self.linkCardView.addCard(
            FluentIcon.CODE,
            self.tr('规则文件夹'),
            cfg.ruleFolder,
            signalBus.ruleFolderChangedSignal,
            "/rule"
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), 200
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h-50, 50, 50))
        path.addRect(QRectF(w-50, 0, 50, 50))
        path.addRect(QRectF(w-50, h-50, 50, 50))
        path = path.simplified()

        # draw background color
        if not isDarkTheme():
            painter.fillPath(path, QColor(206, 216, 228))
        else:
            painter.fillPath(path, QColor(0, 0, 0))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation)
        path.addRect(QRectF(0, h, w, self.height() - h))
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    def __init__(self, parent = None, mx_cfg = None):
        super().__init__(parent=parent)
        self._mx_cfg = mx_cfg
        self._label_dic = self._mx_cfg.labelDic
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()

        signalBus.homeMesRefresh.connect(self.__homeMesRefresh)
        signalBus.fileLabeledSignal.connect(self.__typeCardViewRefresh)

        signalBus.ruleFolderChangedSignal.connect(self.__showRestartTooltip)
        signalBus.INTFolderChangedSignal.connect(self.__showRestartTooltip)
        signalBus.paraFolderChangedSignal.connect(self.__showRestartTooltip)

        self.loadHomeMes()

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(
            self.tr('Updated successfully'),
            self.tr('Configuration takes effect after restart'),
            duration=5500,
            parent=self
        )

    def __initWidget(self):
        self.view.setObjectName('view')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadHomeMes(self):
        self._home_cards = {}
        self.__initFileCard()
        self.__initTypeCard()
        self.__initParaCard()
        self.vBoxLayout.addStretch(1)



    def __initFileCard(self):
        self._file_label_view = HomeFileCardView(
            self.view, self.tr("文件分类情况"))
        file_card = HomeFileCard(
            icon = FIF.CHECKBOX,
            title = '已分类文件',
            content = self.tr("自动分类文件数: {}\n分类文件数: {}"
                              .format(self._mx_cfg.autoLabeledFilesNum, self._mx_cfg.labeledFileNum)),
            route_key = 'labeledInterface')
        self._file_label_view.addCard(file_card=file_card)
        self._home_cards['labeled_file_card'] = file_card
        file_card = HomeFileCard(
            icon = FIF.DATE_TIME,
            title = "未分类文件",
            content = self.tr("未自动分类文件数: {}\n未分类文件数: {}"
                              .format(self._mx_cfg.autoUnlabeledFilesNum, self._mx_cfg.unlabeledFileNum)),
            route_key = 'unlabeledInterface'
        )
        self._file_label_view.addCard(file_card=file_card)
        self._home_cards['unlabeled_file_card'] = file_card
        self.vBoxLayout.addWidget(self._file_label_view)

    def __initTypeCard(self):
        self._type_file_view = HomeTypeCardView(
            self.view, self.tr("类别文件数"))
        for item in self._label_dic:
            type_card = HomeTypeCard(
                icon = FIF.DOCUMENT,
                title = item,
                content = self.tr('文件数: 0'),
                route_key = 'type_labeled_interfaces_{}'.format(item)
            )

            type_card.hide()
            self._type_file_view.addCard(type_card)
            self._home_cards['type_card_{}'.format(item)] = type_card

        self._type_file_view.hide()
        self.vBoxLayout.addWidget(self._type_file_view)

    def __initParaCard(self):
        self._para_cards_view = HomeParaCardView(self.view)
        para_gallery = self._mx_cfg.paraGallery
        for item in para_gallery.items:
            if para_gallery[item].type == MxParaType.STR:
                self._para_cards_view.addStrCard(para_gallery[item])
            elif para_gallery[item].type == MxParaType.OPTION:
                self._para_cards_view.addOptionCard(para_gallery[item])
        self.vBoxLayout.addWidget(self._para_cards_view)


    def __typeCardViewRefresh(self, file:MxReFile):
        self._type_file_view.show()
        label = file.label
        if '_' in label:
            type_name = label.split('_')[0]
        else:
            type_name = "Others"
        card = self._home_cards['type_card_{}'.format(type_name)]
        card.addFile()
        card.show()


    def __homeMesRefresh(self):
        self._home_cards['labeled_file_card'].refreshCardCon(self.tr("自动分类文件数: {}\n分类文件数: {}"
                                .format(self._mx_cfg.autoLabeledFilesNum, self._mx_cfg.labeledFileNum)))
        self._home_cards['unlabeled_file_card'].refreshCardCon(self.tr("未自动分类文件数: {}\n未分类文件数: {}"
                                .format(self._mx_cfg.autoUnlabeledFilesNum, self._mx_cfg.unlabeledFileNum)))