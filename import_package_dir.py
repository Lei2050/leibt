import os
import sys

def getFileNames(path, subfixs = []):
    ''' 获取指定目录下的所有指定后缀的文件名 '''
    f_list = os.listdir(path)
    ret = []
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if not subfixs or os.path.splitext(i)[1] in subfixs:
            ret.append(i)
    return ret

with open('shoudong_import.py', "w", encoding='utf-8') as f:
    f.write('#打包时，这些文件需要手动引入以下，否则Pyinstaller打不进包\n')
    f.write('#这些包都不是显式import的，比如调用__import__引入的\n')
    for dir in sys.argv[1:]:
        filenames = getFileNames(sys.argv[1], ['.py'])
        for filename in filenames:
            f.write(f'import {dir}.' + filename.split('.')[0] + '\n')
