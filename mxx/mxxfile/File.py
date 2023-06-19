import os.path

class File:
    def __init__(self, file_path):
        self._path = self.loadPath(file_path)
        if self._path == None:
            print('file path wrong!')
            return
        self._root_idx = 0

    def fileSuffix(self):
        if self._path == None:
            return None
        return self.fileName().split('.')[-1]

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
        if (self._path == None):
            return None
        ans = self._path[0]
        if ans[-1] == ':' and len(ans) == 2:
            ans = ans + '\\' + self._path[1]
        else:
            os.path.join(ans, self._path[1])
        for i in range(2, len(self._path)):
            ans = os.path.join(ans, self._path[i])
        return ans

    def filePathIdx(self, idx:int):
        if idx >= len(self._path):
            return "out out range"
        else:
            return self._path[idx]

    def fileName(self):
        if self._path == None:
            return None
        return self._path[len(self._path) - 1]

    def loadPath(self, file_path):
        if os.path.isfile(file_path):
            if '\\' in file_path:
                return file_path.split('\\')
            elif '/' in file_path:
                return file_path.split('/')
        else:
            return None

if __name__ == '__main__':
    file_dir = 'D:\\2023\\Leading\\FileArr\\INT\\Leading_INT.json'
    file = File(file_dir)
    print(file.fileContent())
    print(file.fileName())
    print(file.fileSuffix())
    print(file.filePath())
    print(file.filePathIdx(1))
