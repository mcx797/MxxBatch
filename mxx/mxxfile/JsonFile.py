import json

from mxx.mxxfile.File import File as File


class JsonFile(File):
    def __init__(self, file_path):
        super().__init__(file_path)
        if self.filePath() == None:
            return


    def fileContent(self):
        try:
            file = open(self.filePath(), encoding='utf-8')
        except:
            print('mxxfile/JsonFile.py no such file in {}'.format(self.filePath()))
            return None
        ans = ''
        try:
            ans = json.load(file)
        except:
            print('mxxfile/JsonFile.py json format wrong in {}'.format(self.filePath()))
            ans = None
        file.close()
        return ans



if __name__ == '__main__':
    file_path = 'C:\\Users\\77902\\Desktop\\LeadingBatch\\config\\leading_rule.json'
    file = JsonFile(file_path)
    print(file.fileName())
    print(file.fileContent())
    print(file.fileSuffix())