class Command:
    def __init__(self, model):
        self.model = model        
        self.done = False #是否执行过

    def _check(self):
        return True
    
    #执行命令
    def Redo(self):
        if self.done:
            return False
        
        if not self._check():
            return False
        
        self.done = self.redo()

        return self.done

    #执行命令，子类具体执行
    def redo(self):
        '''
        virtual method
        '''
        return False

    #撤销命令
    def Undo(self):
        if not self.done:
            return False

        ok = self.undo()
        if ok:
            self.done = False

        return ok

    #撤销命令，子类具体执行
    def undo(self):
        '''
        virtual method
        '''
        return False
