import model.exporter.py.py_expoter as py_expoter

import g.gg as gg

class Factory:
    Classes = {
        'python'               : py_expoter.PyExporter,
    }

    @classmethod
    def New(cls, model, exportDirectory, type):
        c = cls.Classes.get(type, None)
        if c is None:
            return None
        return c(model, exportDirectory)
