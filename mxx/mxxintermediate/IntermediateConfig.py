from mxx.mxxfile.JsonFile import JsonFile as JsonFile
from mxx.mxxintermediate.ParaGallery import ParaGallery
from mxx.mxxintermediate.IntermediateGallery import IntermediateGallery
from mxx.mxxlog.LogFile import wrong_log


class Config:
    def __init__(self, file:JsonFile):
        dic = file.fileContent()
        if dic == None:
            self._file = None
            return
        self._file = file
        if 'description' in dic:
            self._description = dic['description']
            if not isinstance(self._description, str):
                wrong_log.addLog('mxx.mxxintermediate.IntermeidateConfig no description in file'.format(file.filePath()))
                self._description = None
                return
        else:
            self._description = None
        if 'para' in dic:
            self._para_gallery = ParaGallery(dic['para'])
        else:
            self._para_gallery = None
        if 'INT' in dic:
            self._INT_gallery = IntermediateGallery(self, dic['INT'])
        else:
            self._INT_gallery = None

    def INTGallery(self):
        return self._INT_gallery

    def isConfig(self):
        if self._file == None:
            return False
        if self._description == None:
            return False
        if self._para_gallery == None:
            return False
        if self._INT_gallery == None:
            return False
        return True

    def __str__(self):
        ans = '{{description: {0}, para: {1}, INT: {2}}}'\
            .format(self._description, str(self._para_gallery), str(self._INT_gallery))
        return ans


if __name__ == '__main__':
    file_path = 'C:\\Users\\77902\\Desktop\\LeadingBatch\\config\\leading_INT.json'
    file = JsonFile(file_path)
    config = Config(file)

