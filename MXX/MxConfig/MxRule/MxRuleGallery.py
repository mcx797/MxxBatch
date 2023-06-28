from MXX.MxGallery.MxListGallery import MxListGallery
from MXX.MxLog.MxLog import MxLog
from MXX.MxGallery.MxItem import MxItem
from MXX.MxPath.MxPath import MxPath
from enum import Enum

class MxRuleGallery(MxListGallery):
    def __init__(self, parent):
        super().__init__(parent)

    def loadJsonFile(self, json_file):
        con = json_file.fileContent
        if isinstance(con, list):
            for item in con:
                item = MxRuleItem(self, json_file.filePath, item, self._parent)
                if item.name != None:
                    self.addItem(item)
        else:
            MxLog().wrongLog('rule file format wrong in file: {}'.format(json_file.filePath))

    def match(self, path:str):
        for item in self._items:
            label = item.match(path)
            if label != None:
                return label
        return None


class MxRuleItem(MxItem):
    def __init__(self, parent, path, dic, config):
        if not isinstance(dic, dict):
            self._name = None
            MxLog().wrongLog('MxRuleGallery: rule format wrong in file: {}'.format(path))
            return
        if not self.__loadName(dic, config):
            self._name = None
            MxLog().wrongLog('MxRuleGallery: rule key target wrong in file: {}'.format(path))
            return
        super().__init__(parent, path, dic['target'])
        if not self.__loadSuffix(dic):
            self._name = None
            MxLog().wrongLog('MxRuleGallery: rule key suffix format wrong in item: {}, file: {}'.format(self._name, path))
            return
        if not self.__loadRules(dic):
            self._name = None
            MxLog().wrongLog('MxRuleGallery: rule key rule format wrong in item: {}, file: {}'.format(self._name, path))
            return

    def __loadRules(self, dic):
        if 'rule' not in dic:
            return False
        if not isinstance(dic['rule'], list):
            return False
        self._var = {}
        self._rule = []
        for item in dic['rule']:
            rule = Rule(item)
            if rule.type == None:
                return False
            self._rule.append(rule)
            if 'var' in item:
                if isinstance(item['var'], str):
                    self._var[item['var']] = rule
        return True

    def __loadName(self, dic, config):
        if 'target' not in dic:
            return False
        if not isinstance(dic['target'], str):
            return False
        if not config.INTGallery.isKey(dic['target']):
            MxLog().wrongLog('INT has no item {}'.format(dic['target']))
            return False
        return True

    def __loadSuffix(self, dic):
        if 'suffix' not in dic:
            return False
        if not isinstance(dic['suffix'], list):
            return False
        self._suffix = []
        for item in dic['suffix']:
            if not isinstance(item, str):
                return False
            if not self.__isSuffix(item):
                return False
        return True

    def __isSuffix(self, value):
        for item in MxSuffixType:
            if item.value == value:
                if item not in self._suffix:
                    self._suffix.append(item)
                return True
        return False

    def __str__(self):
        ans = '{{target:{}, path: {}, suffix:{}, rule:['.format(self.name, self.path, self._suffix)
        for item in self._rule:
            ans = ans + str(item) + ', '
        ans = ans[:-2] + ']'
        if len(self._var) != 0:
            ans = ans + ', var:['
            for item in self._var:
                ans = ans + '{' + item + ' ' + str(self._var[item].con) + '}, '
        ans = ans[:-2] + ']'
        return ans

    @property
    def suffix(self):
        return self._suffix

    def match(self, path:str):
        path = MxPath(path)
        if not self.isSuffix(path.fileSuffix):
            return None
        for rule in self._rule:
            if rule.match(path, self._var) == False:
                return None
        return self.name

    def isSuffix(self, suffix):
        for item in self.suffix:
            if item.value == suffix:
                return True
        return False


class MxSuffixType(Enum):
    TXT = 'txt'
    XLS = 'xls'
    XLSX = 'xlsx'
    PPT = 'ppt'
    PPTX = 'pptx'
    BMP = 'bmp'
    PDF = 'pdf'
    PNG = 'png'
    JPG = 'jpg'
    JPE = 'jpe'
    TIF = 'tif'
    TIFF = 'tiff'
    JPEG = 'jpeg'



class MxRuleType(Enum):
    IN = 'in'


class Rule:
    def __init__(self, dic):
        if not isinstance(dic, dict):
            self._type = None
            return
        if not self.__loadType(dic):
            self._type = None
            return
        if not self.__loadCon(dic):
            self._type = None
            return
        if not self.__loadStart(dic):
            self._type = None
            return
        if not self.__loadEnd(dic):
            self._type = None
            return
        if not self.__loadVar(dic):
            self._type = None
            return

    def __loadType(self, dic):
        if 'type' not in dic:
            return False
        if dic['type'] == 'in':
            self._type = MxRuleType.IN
        else:
            return False
        return True

    def __loadCon(self, dic):
        if 'con' not in dic:
            return False
        con = dic['con']
        if not isinstance(con, list):
            return False
        self._con = []
        for item in con:
            if not isinstance(item, str):
                return False
            self._con.append(item)
        return True

    def __loadStart(self, dic):
        if 'start' not in dic:
            return False
        if not isinstance(dic['start'], str):
            return False
        self._start = dic['start']
        return True

    def __loadEnd(self, dic):
        if 'end' not in dic:
            return False
        if not isinstance(dic['end'], str):
            return False
        self._end = dic['end']
        return True

    def __loadVar(self, dic):
        if 'var' in dic:
            if not isinstance(dic['var'], str):
                return False
            self._var = dic['var']
        return True

    @property
    def var(self):
        return self._var

    @property
    def type(self):
        return self._type

    @property
    def con(self):
        return self._con

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def match(self, path:MxPath, vars:dict):
        start, end =  self.getRange(len(path))
        for i in range(start, end - 1, -1):
            if self.__match(path[i]):
                return True
        return False

    def getRange(self, len_path:int):
        start = len_path - int(self._start) - 1
        end = len_path - int(self._end) - 1
        return start, end

    def __match(self, root:str):
        if self._type == MxRuleType.IN:
            for con in self.con:
                if con in root:
                    return True
            return False
        else:
            return False

    def __str__(self):
        ans = '{{type:{}, con:{}, start:{}, end:{}}}'.format(self.type, self.con, self.start, self.end)
        return ans

