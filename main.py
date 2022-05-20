import sys
import time
import traceback

from PyQt6.QtWidgets import QApplication
from view.main_window import MainWindow
#这行不能删
import shoudong_import #手动引入那些非显式import的包，用于Pyinstaller打包

import g.gg as gg

def excepthook(exc_type, exc_value, exc_tb):
    tm = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)
    with open(gg.SOFTWARE_TMP_DIR + '/error.log', "w+", encoding='utf-8') as f:
        f.write(f'\n\n{tm} error catched!:\n')
        f.write(tb)
    QApplication.quit()
    # or QtWidgets.QApplication.exit(0)

sys.excepthook = excepthook

app = QApplication(sys.argv)

mw = MainWindow()
mw.show()

sys.exit(app.exec())
