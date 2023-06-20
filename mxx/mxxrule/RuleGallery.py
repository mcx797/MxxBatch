from mxx.mxxgallery.Gallery import Gallery
from mxx.mxxintermediate.IntermediateGallery import IntermediateGallery as INTGallery
from mxx.mxxfile.JsonFile import JsonFile as JsonFile
from mxx.mxxfile.Path import Path

class RuleGallery(Gallery):
    def __init__(self, file:JsonFile, INT:INTGallery):
        super().__init__()
        dic = file.fileContent()
        for item in dic:
            if INT.containTarget(target=item['target']):
                self.addItem(RuleItem(item))
        #print(INT)

    def match(self, path:str):
        for item in self._gallery:
            label = item.match(path)
            if label != None:
                return label
        return None

    def __str__(self):
        ans = '[ '
        for item in self._gallery:
            ans = ans + str(item) + ' '
        ans = ans + ' ]'
        return ans

class RuleItem:
    def __init__(self, dic_in):
        if 'target' in dic_in:
            self._target = dic_in['target']
        else:
            self._target = ''

        if 'suffix' in dic_in:
            self._suffix = dic_in['suffix']
        else:
            self._suffix = []

        if 'rules' in dic_in:
            self._rules = []
            for item in dic_in['rules']:
                self._rules.append(Rule(item))
        else:
            self._rules = []

    def match(self, path:str):
        path_temp = Path(path)
        if path_temp.fileSuffix() not in self._suffix:
            return None
        for rule in self._rules:
            if rule.match(path_temp) == False:
                return None
        return self._target

    def __str__(self):
        ans = '{{ target: {0}, suffix: {1}, rules: ['\
            .format(str(self._target), str(self._suffix))
        for item in self._rules:
            ans = ans + str(item)
        ans = ans + '] }}'
        return ans


class Rule:
    def __init__(self, dic_in):
        self._type = dic_in['type']
        self._content = dic_in['content']
        self._start = dic_in['start']
        self._end = dic_in['end']

    def match(self, path:Path):
        start, end = self.getRange(path)
        for i in range (start, end + 1):
            if self.__match(path[i]):
                return True
        return False

    def __match(self, root:str):
        if self._type == 'in':
            for content in self._content:
                if content in root:
                    return True
            return False
        return False

    def getRange(self, path):
        start = len(path) - int(self._end) - 1
        end = len(path) - int(self._start) - 1
        return start, end

    def __str__(self):
        return '{{ type: {}, content: {}, start: {}, end: {} }}' \
            .format(str(self._type), str(self._content), str(self._start), str(self._end))
