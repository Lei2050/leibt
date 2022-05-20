from statistics import mode


class Exporter:
    def __init__(self, model, exportDirectory):
        self.model = model
        exportDirectory = exportDirectory.rstrip('/\\')
        self.exportDirectory = exportDirectory

    def export(self):
        '''
        virtual method
        '''
        pass
