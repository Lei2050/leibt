from PyQt6.QtGui import QStandardItem, QFont, QColor, QIcon, QPixmap

import g.gg as gg

class StandardItemControl(QStandardItem):
    def __init__(self, txt='', icon='', typ = 0, font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)

        ic = QIcon()
        ic.addPixmap(QPixmap(gg.IconPrefix + icon), QIcon.Mode.Normal, QIcon.State.Off)
        self.setIcon(ic)

        self.typ = typ
