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
            self.INT_gallery = IntermediateGallery(self, dic['INT'])
        else:
            self.INT_gallery = None

    def isConfig(self):
        if self._file == None:
            return False
        if self._description == None:
            return False
        if self._para_gallery == None:
            return False
        if self.INT_gallery == None:
            return False
        return True

if __name__ == '__main__':
    file_path = 'C:\\Users\\77902\\Desktop\\LeadingBatch\\config\\leading_INT.json'
    file = JsonFile(file_path)
    config = Config(file)

