from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QWidget
from MXX.MxFile.MxReFile import MxReFile
from PyQt5.QtCore import Qt

from qfluentwidgets import ComboBox, LineEdit, PrimaryPushButton
from app.components.tree_frame import TreeFrame
from app.common.open_file import open_file

from MXX.MxConfig.MxConfig.MxConfig import MxConfig
from MXX.MxPath.MxPath import MxPath
from MXX.MxFile.MxReFile import MxReFile

from app.common.style_sheet import StyleSheet


class PostLabelDialog(QDialog):
    def __init__(self, file:MxReFile, mx_cfg:MxConfig):
        super().__init__()

        self._file = file
        self._mx_cfg = mx_cfg

        self.setMinimumWidth(900)
        self.setMinimumHeight(500)
        self.setWindowTitle('{}后处理窗口'.format(self._file.fileName))

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.view = QFrame(self)
        self.hBoxLayout = QHBoxLayout(self)
        self._source_panel = FilePanel(self, self._mx_cfg)
        self._target_panel = FilePanel(self, self._mx_cfg)
        label = None
        if self._file.isLabeled:
            label = self._file.label
        elif self._file.isAutoLabeled:
            label = self._file.autoLabel
        self._post_process_panel = ProcessPanel(self, self._mx_cfg, label)
        target_path = self._mx_cfg.targetPath(self._post_process_panel.typeName)
        file_suffix = self._post_process_panel.suffixText
        suffix = self._file.fileSuffix
        if file_suffix == '':
            target_path = target_path + '.' + suffix
        else:
            target_path = target_path + '_' + file_suffix + '.' + suffix
        target_path = MxPath(target_path)
        self._source_panel.setMes(self._file)
        self._target_panel.setPathMes(target_path)
        self.__initWidget()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def refreshTargetPanel(self):
        target_path = self._mx_cfg.targetPath(self._post_process_panel.typeName)
        file_suffix = self._post_process_panel.suffixText
        suffix = self._file.fileSuffix
        if file_suffix == '':
            target_path = target_path + '.' + suffix
        else:
            target_path = target_path + '_' + file_suffix + '.' + suffix
        target_path = MxPath(target_path)
        self._target_panel.setPathMes(target_path)

    def closeEvent(self, e):
        super().closeEvent(e)

    def __initWidget(self):
        self.hBoxLayout.addWidget(self._source_panel)
        self.hBoxLayout.addWidget(self._target_panel)
        self.hBoxLayout.addWidget(self._post_process_panel)
        self.__setQss()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    @property
    def isOk(self):
        return self._post_process_panel.isOk

    @property
    def typeName(self):
        return self._post_process_panel.typeName

    def __setQss(self):
        self.view.setObjectName('post_dialog_view')
        StyleSheet.POST_DIALOG.apply(self)


class ProcessPanel(QFrame):
    def __init__(self, parent, mx_cfg:MxConfig, label):
        super().__init__(parent=parent)
        self._label = label
        self._mx_cfg = mx_cfg
        self._parent = parent
        self._is_ok = False
        self._label_dic = mx_cfg.labelDic
        self.vBoxLayout = QVBoxLayout(self)
        self._type_post_label = QLabel(self.tr('文件类型'))
        self._type_box = ComboBox(self)
        self._item_box = ComboBox(self)
        self._type_box.setFixedWidth(270)
        self._item_box.setFixedWidth(270)
        self._suffix_post_label = QLabel(self.tr('文件名后缀'))
        self._line_edit = LineEdit(self)
        self._line_edit.setPlaceholderText(self.tr('设置文件名后缀'))
        self._line_edit.setFixedWidth(270)
        self.setFixedWidth(350)
        if self._parent._file.fileNameSuffix != '':
            self._line_edit.setText(self._parent._file.fileNameSuffix)
        self._line_edit.textChanged.connect(self.__lineEditChannged)

        self._open_dir_button = PrimaryPushButton(self.tr('打开文件夹'))
        self._open_file_button = PrimaryPushButton(self.tr('打开文件'))
        self._ok_button = PrimaryPushButton(self.tr('ok!'))
        self._cancel_button = PrimaryPushButton(self.tr('cancel'))

        self.__initWidget()

        self._type_box.currentIndexChanged.connect(self.__typeBoxChanged)
        self._item_box.currentIndexChanged.connect(self.__itemBoxChanged)
        self._open_dir_button.clicked.connect(self.__openDir)
        self._open_file_button.clicked.connect(self.__openFile)
        self._ok_button.clicked.connect(self.__okButtonClicked)
        self._cancel_button.clicked.connect(self.__cancelButtonClicked)

    @property
    def suffixText(self):
        return self._line_edit.text()

    @property
    def isOk(self):
        return self._is_ok

    @property
    def typeName(self):
        return '{}_{}'.format(self._type_name, self._item_name)

    def __okButtonClicked(self):
        if self.suffixText != self._parent._file.fileNameSuffix:
            self._parent._file.setFileNameSuffix(self.suffixText)
        self._is_ok = True
        self._parent.close()

    def __cancelButtonClicked(self):
        self._is_ok = False
        self._parent.close()

    def __openDir(self):
        if not isinstance(self._parent._file, MxReFile):
            return
        open_file(self._parent._file.dirPath)

    def __openFile(self):
        if not isinstance(self._parent._file, MxReFile):
            return
        open_file(self._parent._file.filePath)

    def __initWidget(self):
        label = self._label
        self.vBoxLayout.addWidget(self._type_post_label)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self._type_box)
        self.vBoxLayout.addWidget(self._item_box)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self._suffix_post_label)
        self.vBoxLayout.addWidget(self._line_edit)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self._open_dir_button)
        self.vBoxLayout.addWidget(self._open_file_button)
        self.vBoxLayout.addWidget(self._ok_button)
        self.vBoxLayout.addWidget(self._cancel_button)

        type_temp = []
        for i, item in enumerate(self._label_dic):
            type_temp.append(item)
        if len(self._label_dic) > 0:
            self._type_box.addItems(type_temp)
            self._type_box.setCurrentIndex(0)
            self._type_name = self._type_box.currentText()
            item_temp = self._label_dic[self._type_box.currentText()]
            if len(item_temp) > 0:
                self._item_box.addItems(item_temp)
                self._item_box.setCurrentIndex(0)
                self._item_name = self._item_box.currentText()
        if label != None:
            if '_' in label:
                type_name = label.split('_')[0]
                item_name = label.split('_')[1]
            else:
                type_name = "Others"
                item_name = label
            for i, item in enumerate(self._label_dic):
                if item == type_name:
                    self._type_box.setCurrentIndex(i)
                    self._type_name = type_name
                    self._item_box.clear()
                    self._item_box.addItems(self._label_dic[self._type_name])
                    for i, item1 in enumerate(self._label_dic[self._type_name]):
                        if item1 == item_name:
                            self._item_box.setCurrentIndex(i)
                            self._item_name = item_name
                            break
                    break

    def __typeBoxChanged(self):
        self._type_idx = self._type_box.currentIndex()
        self._type_name = self._type_box.currentText()
        self._item_box.clear()
        self._item_box.addItems(self._label_dic[self._type_name])
        self._item_box.setCurrentIndex(0)
        self._item_name = self._item_box.currentText()
        self._parent.refreshTargetPanel()

    def __itemBoxChanged(self):
        self._item_idx = self._item_box.currentIndex()
        self._item_name = self._item_box.currentText()
        self._parent.refreshTargetPanel()

    def __lineEditChannged(self):
        self._parent.refreshTargetPanel()


class FilePanel(QFrame):
    def __init__(self, parent, mx_cfg:MxConfig):
        super().__init__(parent=parent)
        self._mx_cfg = mx_cfg
        self.vBoxLayout = QVBoxLayout(self)
        self.frame = TreeFrame(self, False)

        self.__initWidget()

    def __initWidget(self):
        self.vBoxLayout.setContentsMargins(15, 5, 5, 5)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.frame)
        self.vBoxLayout.addStretch(1)

    def setMes(self, file:MxReFile):
        self._file = file
        self.frame.refresh(file)

    def setPathMes(self, path:MxPath):
        self.frame.refreshPath(path)

