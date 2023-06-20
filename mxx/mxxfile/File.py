import os.path
from mxx.mxxfile.Path import Path

class File:
    def __init__(self, file_path):
        self._path = Path(file_path)
        if not os.path.isfile(self._path.filePath()):
            self._path = None
        if self._path == None:
            print('file path wrong!')
            return
        self._root_idx = 0

    def fileSuffix(self):
        if self._path == None:
            return None
        return self._path.fileSuffix()

    def fileContent(self):
        if self._path == None:
            return None
        ans = ''
        try:
            with open(self.filePath(), 'r', encoding='utf-8') as f:
                while True:
                    line = f.readline()
                    if line == '':
                        break
                    ans = ans + line
        except:
            print('mxxfile/File.py: no file here')
        return ans

    def filePath(self):
        return self._path.filePath()

    def fileName(self):
        return self._path.fileName()


if __name__ == '__main__':
    file_dir = 'D:\\2023\\Leading\\FileArr\\INT\\Leading_INT.json'
    file = File(file_dir)
    print(file.fileContent())
    print(file.fileName())
    print(file.fileSuffix())
    print(file.filePath())
