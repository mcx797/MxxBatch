from mxx.mxxgallery.Gallery import Gallery


class ParaGallery(Gallery):
    def __init__(self, paras:dict):
        super().__init__()
        self._gallery = {}
        for key in paras:
            if paras[key]['type'] == 'options':
                self.addItem(key, OptionItem(paras[key]))
            elif paras[key]['type'] == 'combo':
                self.addItem(key, ComboItem(self, paras[key]))
            else:
                self.addItem(key, ParaItem(paras[key]))

    def isItem(self, name:str):
        return name in self._gallery

    def addItem(self, key, item):
        self._gallery[key] = item

    def item(self, key):
        try:
            return self._gallery[key]
        except:
            print('mxx.mxxintermediate.paraGallery no such key {}'.format(key))
            return None

    def __str__(self):
        ans = ''
        for key in self._gallery:
            ans = ans + '{{key: {0}, value:{1}}}'\
                .format(str(key), str(self.item(key).value()))
        return ans


class ParaItem():
    def __init__(self, para:dict):
        self._value = para['value']

    def value(self):
        return self._value


class OptionItem(ParaItem):
    def __init__(self, para:dict):
        super().__init__(para)
        self._options = para['options']

    def options(self):
        return self._options


class ComboItem(ParaItem):
    def __init__(self, parent, para:dict):
        super().__init__(para)
        self._paras = []
        for item in para['paras']:
            self._paras.append(parent.item(item))

    def value(self):
        para_list = []
        for item in self._paras:
            para_list.append(item.value())
        return super().value().format(para_list)

