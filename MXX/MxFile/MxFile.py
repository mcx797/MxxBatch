import os
from MXX.MxPath.MxPath import MxPath
from MXX.MxLog.MxLog import MxLog

class MxFile:
    def __init__(self, path:str = ''):
        self._path = MxPath(path)
        if not self.isFile:
            MxLog().wrongLog('MxFile: not a file in {}'.format(path))

    ''' property '''
    @property
    def filePath(self):
        return self._path.filePath

    @property
    def dirPath(self):
        return self._path.dirPath

    @property
    def fileName(self):
        return self._path.fileName

    @property
    def isFile(self):
        return self._path.isFile

    @property
    def fileSuffix(self):
        return self._path.fileSuffix

    @property
    def fileContent(self):
        if not self.isFile:
            MxLog().wrongLog('MXX.MxFile.MxFile: not a file in {}'.format(self.filePath))
            return
        ans = ''
        try:
            with open(self.filePath, 'r', encoding='utf-8') as f:
                while True:
                    line = f.readline()
                    if line == '':
                        break
                    ans = ans + line
        except:
            MxLog().wrongLog('MXX.MxFile.MxFile: no such file in {}'.format(self.filePath))
        return ans


if __name__ == '__main__':
    file_path = 'C:/Users/77902/Desktop/LeadingBatch/config/INT/ECS评价.json'
    file = MxFile(file_path)
    print(file.fileContent)
    print(file.fileSuffix)
    print(file.filePath)
    print(file.fileName)
    print(file.isFile)
