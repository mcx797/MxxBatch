from app.view.mxx_interface import MxxInterface



class LabeledInterface(MxxInterface):
    def __init__(self, parent=None):
        super().__init__(
            title='自动分类文件',
            subtitle = 'labeled files',
            parent = parent
        )

        #self.loadSamples()

    '''
    def loadSamples(self):
        basicInputView = SampleCardView(
            self.tr('Basic input samples')
        )
    '''


