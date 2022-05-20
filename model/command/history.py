
class History:
    MaxHistory = 30
    def __init__(self):
        self.doneList = [] #历史的操作
        self.undoList = [] #撤销的操作
    
    def addDoneCmd(self, cmd):
        self.doneList.append(cmd)
        if len(self.doneList) > History.MaxHistory:
            self.doneList.pop(0)
        self.undoList.clear()
    
    def redo(self):
        if len(self.undoList) <= 0:
            return False
        cmd = self.undoList.pop()
        ret = cmd.Redo()
        if ret:
            self.doneList.append(cmd)
        return ret

    def undo(self):
        if len(self.doneList) <= 0:
            return False
        cmd = self.doneList.pop()
        ret = cmd.Undo()
        if ret:
            self.undoList.append(cmd)
        return ret
