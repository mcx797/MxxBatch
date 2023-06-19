from app.view.mxx_interface import MxxInterface



class LabeledInterface(MxxInterface):
    def __init__(self, parent=None):
        super().__init__(
            title='已分类文件',
            subtitle = 'labeled files',
            parent = parent
        )