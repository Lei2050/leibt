import os
import re
import traceback
import uuid

def isPositionInGeometry(pos, geometry):
    deltax, deltay = pos[0] - geometry[0], pos[1] - geometry[1]
    return 0 < deltax < geometry[2] and 0 < deltay < geometry[3]

def singleton(cls):
    _instance = {}
    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

def getFormatTraceback():
    s = ''
    for line in traceback.format_stack():
        s += line.strip() + '\n'
    return s

validNamePattern = "^[A-Za-z][A-Za-z0-9_]*$"

def isValidName(name):
    return bool(re.match(validNamePattern, name))

#64位uuid生成器，根据它的算法，这样还是有概率重复的，不过对于本软件远远够用了。
def gen64Id():
    return uuid.uuid1().int >> 64

#检查目录path下是否有subfix类型的文件
def isPathHasKindFile(path, subfix):
    dirs = os.listdir(path)
    for v in dirs:
        v = v.split('.')
        if len(v) == 2 and ('.'+v[1]) == subfix:
            return True
    return False
    
#检查目录path下有多少个subfix类型的文件
def countPathHasKindFile(path, subfix):
    c = 0
    dirs = os.listdir(path)
    for v in dirs:
        v = v.split('.')
        if len(v) == 2 and ('.'+v[1]) == subfix:
            c += 1
    return c
