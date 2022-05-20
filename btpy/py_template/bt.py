from os import stat
import weakref
import time
from btpy.py_template.bool.py_template_and import *
from btpy.py_template.bool.py_template_or import *
from btpy.py_template.combination.py_template_exec_until_false import *
from btpy.py_template.combination.py_template_exec_until_true import *
import btpy.py_template.const as btconst

class BT:
    def __init__(self, agent):
        #根节点
        self.root = None
        #游戏中的实体代理
        self.agent = weakref.ref(agent)
        #节点引用
        self.nodes = {}
        #等待时间（时间戳），
        self.wait = 0
        #触发等待的节点以及其父节点
        self.waitNodeId = 0
        #触发等待时，当前的执行链路
        self.execPathWait = []
        #当前的执行链路
        self.execPath = []
        #触发等待后现场是否恢复
        self._waitRecovered = True
        #上一次执行返回状态
        self.lastFinishStatus = btconst.BT_TRUE
    
    #interval - 等待时间
    #nodeId - 触发等待的节点
    #nodeParentId - 触发等待的节点的父节点
    def waitFor(self, interval):
        if interval <= 0:
            return
        self.wait = time.time() + interval
        self.execPathWait = self.execPath.copy()
        # print(interval, self.wait, self.execPathWait)
    
    def _execNormalUntilFalse(self, node, agent):
        status = node.updateImpl(self, agent)
        for subNode in node.execChildren:
            status = self.execNormal(subNode, agent)
            if status in (btconst.BT_OVER, btconst.BT_WAIT):
                return status
            if status == btconst.BT_FALSE:
                return status
        return status
    
    def _execNormalUntilTrue(self, node, agent):
        status = node.updateImpl(self, agent)
        for subNode in node.execChildren:
            status = self.execNormal(subNode, agent)
            if status in (btconst.BT_OVER, btconst.BT_WAIT):
                return status
            if status == btconst.BT_TRUE:
                return status
        return status
    
    def _execNormalOr(self, node, agent):
        return node.updateImpl(self, agent)
    
    # def _execNormalAnd(self, node, agent):
    #     status = node.updateImpl(self, agent)
    #     for subNode in node.execChildren:
    #         status = self.execNormal(subNode, agent)
    #         if status in (btconst.BT_OVER, btconst.BT_WAIT):
    #             return status
    #         if status == btconst.BT_FALSE:
    #             return btconst.BT_FALSE
    #     return btconst.BT_TRUE
    
    def _execNormalAnd(self, node, agent):
        return node.updateImpl(self, agent)
    
    def _execNormal(self, node, agent):
        status = node.updateImpl(self, agent)
        if status in (btconst.BT_OVER, btconst.BT_WAIT):
            return status
        for subNode in node.execChildren:
            status = self.execNormal(subNode, agent)
            if status in (btconst.BT_OVER, btconst.BT_WAIT):
                return status
        return status
    
    #正常执行
    def execNormal(self, node, agent):
        self.execPath.append(node.id)
        pathSize = len(self.execPath)

        status = btconst.BT_UNKNOW
        if isinstance(node, PyTemplateExecUntilFalse):
            status = self._execNormalUntilFalse(node, agent)
        elif isinstance(node, PyTemplateExecUntilTrue):
            status = self._execNormalUntilTrue(node, agent)
        elif isinstance(node, PyTemplateOr):
            status = self._execNormalOr(node, agent)
        elif isinstance(node, PyTemplateAnd):
            status = self._execNormalAnd(node, agent)
        else:
            status = self._execNormal(node, agent)
        
        self.execPath = self.execPath[:pathSize-1]

        return status
    
    def execAfterWait(self, node, agent, depth):
        if self._waitRecovered:
            return self.execNormal(node, agent)
        
        #先恢复等待时的现场
        if self.execPathWait[depth] != node.id:
            return btconst.BT_UNKNOW
        if depth+1 == len(self.execPathWait):
            #到达了上次执行等待的节点，说明现场恢复完毕
            self._waitRecovered = True
            #执行等待的节点是没有子节点的，直接返回，父节点执行后续
            return btconst.BT_TRUE
        
        self.execPath.append(node.id)
        pathSize = len(self.execPath)
        status = btconst.BT_UNKNOW
        for subNode in node.execChildren:
            if self._waitRecovered:
                status = self.execNormal(subNode, agent)
                if status in (btconst.BT_OVER, btconst.BT_WAIT):
                    return status
            else:
                status = self.execAfterWait(subNode, agent, depth+1)
                if status in (btconst.BT_OVER, btconst.BT_WAIT):
                    return status
        
        self.execPath = self.execPath[:pathSize]

        return status

    #执行行为树
    def exec(self):
        if not self.root:
            return btconst.BT_TRUE
        if self.wait > 0:
            if time.time() < self.wait:
                return btconst.BT_WAIT
            self.wait = 0
            self._waitRecovered = False
            self.execPath.clear()
            return self.execAfterWait(self.root, self.agent(), 0)
        self.execPath.clear()
        return self.execNormal(self.root, self.agent())
    
    def setLocalAttr(self, name, value):
        setattr(self, name, value)
    