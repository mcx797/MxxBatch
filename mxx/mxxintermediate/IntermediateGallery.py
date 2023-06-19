from mxx.mxxgallery.Gallery import Gallery


class IntermediateGallery(Gallery):
    def __init__(self, parent = None, INTs:dict = None):
        super().__init__()
        for INT in INTs:
            self.addItem(Item(INT, parent._para_gallery))


class Item:
    def __init__(self, INT, para_gallery):
        self._name = INT['name']
        self._types = INT['types']
        self.out_path = INT['out_path']
        self.paras = []
        for para in INT['paras']:
            if para_gallery.isItem(para):
                self.paras.append((para_gallery.item(para)))

    def outPath(self):
        out_paras = []
        for item in self.paras:
            out_paras.append(item.value())
        return self.out_path.format(out_paras)
