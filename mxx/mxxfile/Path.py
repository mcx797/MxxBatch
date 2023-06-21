import os
class Path:
    def __init__(self, path_str):
        self._path = self.__loadPath(path_str)

    def __loadPath(self, path_str):
        if '\\' in path_str:
            return path_str.split('\\')
        elif '/' in path_str:
            return path_str.split('/')

    def path(self):
        if len(self._path) == 0:
            return ''
        ans = self._path[0]
        for i in range(1, len(self._path)):
            ans = ans + '\\' + self._path[i]
        return ans

    def linkCardPath(self, max_len):
        ans = ''
        ans_list = []
        temp = self._path[0]
        if len(self._path) == 1:
            return temp
        for i in range(1, len(self._path)):
            if self.__pathLen(temp + '\\' + self._path[i]) > max_len:
                ans_list.append(temp)
                temp = '\\' + self._path[i]
            else:
                temp = temp + '\\' + self._path[i]
        for item in ans_list:
            ans = ans + item + '\n'
        ans = ans + temp
        return ans

    def __pathLen(self, word:str):
        ans = 0
        for s in word:
            if u'\u4e00' <= s <= u'\u9fff':
                ans = ans + 2
            else:
                ans = ans + 1
        return ans

    def filePath(self):
        ans = self.path()
        if not os.path.isfile(ans):
            ans = 'not a file'
        return ans

    def fileDir(self):
        path = self._path
        if len(path) < 1:
            return ''
        ans = path[0]
        for i in range(1, len(path) - 1):
            ans = ans + '\\' + path[i]
        return ans

    def fileName(self):
        if not os.path.isfile(self.filePath()):
            print('mxx.mxxfile.Path: not a file path {}'.format(self.path()))
            return ''
        return self._path[-1]

    def root(self, idx):
        return self._path[idx]

    def __getitem__(self, item:int):
        return self._path[item]

    def __len__(self):
        return len(self._path)

    def fileSuffix(self):
        return self.fileName().split('.')[-1]

if __name__ == '__main__':
    path = Path('D:\\2023\\Leading\\FileArr\\INT\\Leading_INT.json')
    print(path.filePath())
    if os.path.isfile(path.filePath()):
        print('okok!')
    print(path.fileName())