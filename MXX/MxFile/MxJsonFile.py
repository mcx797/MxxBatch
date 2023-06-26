import json
from MXX.MxFile.MxFile import MxFile
from MXX.MxLog.MxLog import MxLog

class MxJsonFile(MxFile):
    def __init__(self, path):
        super().__init__(path)
        if not self.isFile:
            MxLog().wrongLog('MXX.MxJsonFile.MxJsonFile.py: no such file in {}'.format(path))

    @property
    def fileContent(self):
        try:
            file = open(self.filePath, 'r', encoding='utf-8')
        except:
            MxLog().wrongLog('MXX.MxJsonFile.MxJsonFile.py: no such file or file format wrong in {}'.format(self.filePath))
            return
        ans = {}
        try:
            ans = json.load(file)
        except:
            MxLog().wrongLog('MxJsonFile.MxJsonFile.py: load json file wrong')
        file.close()
        return ans


if __name__ == '__main__':
    path = 'C:\\Users\\77902\\Desktop\\LeadingBatch\\config\\rule/ECS评价.json'
    file = MxJsonFile(path)
    print(file.fileContent)