from PyQt6.QtWidgets import QTreeView

import g.gg as gg

class TreeViewNodes(QTreeView):
    def __init__(self, parent):
        super(QTreeView, self).__init__(parent)

        self.pressed.connect(self.onPressed)

    def onPressed(self, modelIndex):
        item = self.model().itemFromIndex(modelIndex)
        gg.CurrentControlNode = {'type': item.typ}

    def keyPressEvent(self, event):
        super(QTreeView, self).keyPressEvent(event)
        event.ignore()
