import os

class MxPath:
    def __init__(self, path):
        default = 'something wrong'
        if isinstance(path, str):
            self._path = self.__loadPath(path)
            self._default = default
        elif isinstance(path, list):
            for item in path:
                if not isinstance(item, str):
                    self._path = None
                    return
            self._path = path
            self._default = default
        else:
            self._path = None
            self._default = default

    @property
    def path(self):
        if len(self._path) == 0:
            return self._default
        ans = self._path[0]
        for i in range(1, len(self)):
            ans = ans + '/' + self._path[i]
        return ans

    @property
    def filePath(self):
        ans = self.path
        if not os.path.isfile(ans):
            print('no such file')
            ans = self._default
        return ans

    @property
    def dirPath(self):
        ans = self.path
        if os.path.isdir(ans):
            return ans
        else:
            if len(self._path) < 1:
                return self._default
            ans = self._path[0]
            for i in range(1, len(self._path) - 1):
                ans = ans + '/' + self._path[i]
            return ans

    @property
    def isFile(self):
        return os.path.isfile(self.path)

    @property
    def isDir(self):
        return os.path.isdir(self.path)

    @property
    def fileName(self):
        if self.isFile:
            return self._path[len(self) - 1]

    @property
    def fileSuffix(self):
        if self.isFile:
            return self.fileName.split('.')[-1]

    def lenLimPath(self, len_max):
        ans = ''
        ans_list = []
        if len(self._path) == 0:
            return self._default
        temp = self._path[0]
        if len(self._path) == 1:
            return temp
        for i in range(1, len(self._path)):
            if self.__wordLen(temp + '/' + self._path[i]) > len_max:
                ans_list.append(temp)
                temp = '/' + self._path[i]
            else:
                temp = temp + '/' + self._path[i]
        for item in ans_list:
            ans = ans + item + '\n'
        ans = ans + temp
        return ans

    def __loadPath(self, path:str):
        ans = []
        INTs = path.split('\\')
        for INT in INTs:
            blks = INT.split(('/'))
            for blk in blks:
                ans.append(blk)
        return ans

    def __wordLen(self, word:str):
        ans = 0
        for s in word:
            if u'\u4e00' <= s <= u'\u9fff':
                ans = ans + 2
            else:
                ans = ans + 1
        return ans

    def __str__(self):
        return str(self.path())

    def __len__(self):
        return len(self._path)

    def __getitem__(self, item:int):
        return self._path[item]

    def __sub__(self, other):
        if isinstance(other, int):
            if len(self) <= abs(other):
                return MxPath('')
            if other == 0:
                return MxPath(self.path)
            if other > 0:
                ans = []
                for i in range(len(self) - other):
                    ans.append(self[i])
                return MxPath(ans)
            if other < 0:
                ans = []
                other = abs(other)
                for i in range(other, len(self)):
                    ans.append(self[i])
                return MxPath(ans)
        elif isinstance(other, MxPath):
            if len(other) > len(self):
                return MxPath('')
            else:
                for i in range(len(other)):
                    if other[i] != self[i]:
                        return MxPath('')
                    return self - -len(other)

    def __add__(self, other):
        if isinstance(other, MxPath):
            ans = []
            for i in range(len(self)):
                ans.append(self[i])
            for i in range(len(other)):
                ans.append(other[i])
            return MxPath(ans)


if __name__ == '__main__':
    path = MxPath('C:\\Users/77902\\Desktop/LeadingBatch/config/config.json')
    path1 = MxPath('C:/Users/77902')
    path = path - path1
    print(len(path))
    print(path.path)
    '''
    print(path.filePath)
    print('dirPath')
    print(path.dirPath)
    print(path[len(path) - 1])
    print(path.lenLimPath(30))
    print(path.fileName)
    print(path.fileSuffix)
    '''

