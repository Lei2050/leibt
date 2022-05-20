import enum

class ArgumentType(enum.IntEnum):
    TreeAttr = 1 #行为树局部参数，从行为树本身设置或获取
    String   = 2 #字符类型
    Int      = 3 #整型
    Float    = 4 #浮点

class Argument:
    def __init__(self, type, expr):
        self.type = type
        self.expr = expr
    
    def getValue(self, bt):
        if self.type == ArgumentType.TreeAttr:
            return getattr(bt, self.expr, None)
        elif self.type == ArgumentType.String:
            return str(self.expr)
        elif self.type == ArgumentType.Int:
            return int(self.expr)
        elif self.type == ArgumentType.Float:
            return int(self.expr)
        return None
