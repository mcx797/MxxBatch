from mxx.mxxgallery.Gallery import Gallery


class IntermediateGallery(Gallery):
    def __init__(self, parent = None, INTs:dict = None):
        super().__init__()
        for INT in INTs:
            self.addItem(Item(INT, parent._para_gallery))

    def containTarget(self, target:str):
        for item in self._gallery:
            if item.name() == target:
                return True
        return False

    def __str__(self):
        ans = '[ '
        for item in self._gallery:
            ans = ans + '{{' +  str(item) + '}}, '
        ans = ans[:-2] + ' ]'
        return ans


class Item:
    def __init__(self, INT, para_gallery):
        self._name = INT['name']
        self._types = INT['types']
        self.out_path = INT['out_path']
        self.paras = []
        for para in INT['paras']:
            if para_gallery.isItem(para):
                self.paras.append((para_gallery.item(para)))

    def name(self):
        return self._name

    def __str__(self):
        ans = 'name : {}, types : {}, out_path : {}'.format(str(self._name), str(self._types), self.outPath())
        return ans

    def outPath(self):
        out_paras = []
        for item in self.paras:
            out_paras.append(item.value())
        return self.out_path.format(out_paras)
