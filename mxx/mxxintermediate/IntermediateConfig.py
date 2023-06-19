from mxx.mxxfile.JsonFile import JsonFile as JsonFile
from mxx.mxxintermediate.ParaGallery import ParaGallery
from mxx.mxxintermediate.IntermediateGallery import IntermediateGallery


class Config:
    def __init__(self, file:JsonFile):
        dic = file.fileContent()
        if dic == None:
            return
        self._file = file
        self._description = dic['description']
        self._para_gallery = ParaGallery(dic['para'])
        self.INT_gallery = IntermediateGallery(self, dic['INT'])
        INT = dic['INT']


if __name__ == '__main__':
    file_path = 'C:\\Users\\77902\\Desktop\\LeadingBatch\\config\\leading_INT.json'
    file = JsonFile(file_path)
    config = Config(file)

