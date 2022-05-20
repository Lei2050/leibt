import enum
import os

APP_DATA_PATH = os.getenv("APPDATA").lstrip('/\\')
SOFTWARE_NAME = 'leibt'
SOFTWARE_TMP_DIR = APP_DATA_PATH + '/' + SOFTWARE_NAME
#使用Pyinstaller打包的话，打包后的exe，其实是每次都把虚拟环境复制到临时目录
# （比如win下的C:\Users\***\AppData\Local\Temp\_MEI********），
# ROOT就会是那个临时目录，
# 所以代码中想通过__file__做一些操作的事就要换一种方式，因为每次__file__都在变。
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')).rstrip('/\\')

#创建软件临时目录
def CreateSoftwareTmpDir():
    if not os.path.exists(SOFTWARE_TMP_DIR):
        os.mkdir(SOFTWARE_TMP_DIR)

CreateSoftwareTmpDir()

#所有icon的前缀
IconPrefix = 'resource/icon/'
# def getIconPrefix():
#     global IconPrefix
#     if IconPrefix:
#         return IconPrefix
#     # IconPrefix = os.path.dirname(os.getcwd()) + '/resouce/icon/'
#     IconPrefix = os.getcwd() + '/resource/icon/'
#     return IconPrefix

#当前拖动的控制节点
CurrentControlNode = {}

#控制节点类型
class ControlNodeType(enum.IntEnum):
    Start               = 1
    Or                  = 101
    And                 = 102
    FFalse              = 103
    TTrue               = 104
    Condition           = 105
    Wait                = 201
    Action              = 202
    Assignment          = 203
    Calculate           = 204
    Finish              = 205
    EmptyAction         = 206
    SubTree             = 207
    ProbabilisticChoice = 301
    RandomChoice        = 302
    OrderList           = 303
    RandomList          = 304
    ConditionAction     = 305
    ExecUntilFalse      = 306
    ExecUnitlTrue       = 307
    Weight              = 308

CNT = ControlNodeType

#bool类型的控件
ControlNodeTypeBools = (CNT.And, CNT.Condition, CNT.FFalse, CNT.Or, CNT.TTrue)
#动作类型的控件
ControlNodeTypeActions = (CNT.Action, CNT.Assignment, CNT.Calculate, CNT.EmptyAction, CNT.Finish, CNT.Wait, CNT.SubTree)
#组合类型的控件
ControlNodeTypeCombination = (CNT.ConditionAction, CNT.ExecUntilFalse, CNT.ExecUnitlTrue, CNT.OrderList, CNT.ProbabilisticChoice, CNT.RandomChoice, CNT.RandomList)
#动作类和组合类
ControlNodeTypeActionsAndCombination = ControlNodeTypeActions + ControlNodeTypeCombination
#子节点数目不固定类
ControlNodeTypeNonfixedChild = (CNT.And, CNT.Or, CNT.ExecUntilFalse, CNT.ExecUnitlTrue, CNT.OrderList, CNT.ProbabilisticChoice, CNT.RandomChoice, CNT.RandomList)
#子节点数目不固定类、组合类
ControlNodeTypeNonfixedChildCombination = (CNT.ExecUntilFalse, CNT.ExecUnitlTrue, CNT.OrderList, CNT.ProbabilisticChoice, CNT.RandomChoice, CNT.RandomList)
#子节点数目不固定类、bool类
ControlNodeTypeNonfixedChildBool = (CNT.And, CNT.Or)
#不可复制节点
ControlNodeTypeUncopyable = (CNT.Start, )

#控制节点默认大小
ControlNodeDefaultSize = (100, 50)
ControlNodeSize = {
    ControlNodeType.Start : (200, 100),
}
#节点之间最短间距
ControlNodeMargin = (20, 10)
#圆角半径
ControlNodeRectRound = (20, 20)

#默认笔刷相关
PainterPenWidth = 2

#错误码
class ErrorCode(enum.IntEnum):
    WorkspaceNameIllegal           = 1
    WorkspaceExisting              = 2
    WorkspaceSameInDirectory       = 3
    WorkspaceDirIllegal            = 4
    WorkspaceDirPermissionDeny     = 5
    WorkspaceExportIllegal         = 6
    WorkspaceExportDirPermissionDeny = 7
    ConditionHasNoLeftParam        = 601
    ConditionHasNoRightParam       = 602
    ConditionLeftParamIllegal      = 603
    ConditionRightParamIllegal     = 604
    ActionHasNoBehavior            = 801
    ActionBehaviorIllegal          = 802
    AssignmentHasNoLeftParam       = 901
    AssignmentHasNoRightParam      = 902
    AssignmentLeftParamIllegal     = 903
    AssignmentRightParamIllegal    = 904
    CalculateHasNoLeftParam        = 1001
    CalculateHasNoRightParam       = 1002
    CalculateLeftParamIllegal      = 1003
    CalculateRightParamIllegal     = 1004
    ConditionActionHasNoCondition  = 1701
    ConditionActionNoTrueBehavior  = 1702
    ConditionActionNoFalseBehavior = 1703
    WeightIllegalWeight            = 2001

    @classmethod
    def getErrorMsg(cls, code, **kw):
        import data.error as data_error
        return data_error.Data.get(int(code)).format(**kw)

WorkspaceFileSubfix = '.leibtws'
TreeFileSubfix = '.leibttree'
PathDelimiter = '/'

#[mu, a, b] => mu/a/b
def getKeyFromPath(path, *args):
    return PathDelimiter.join(path + list(args))

#[mu, a, b] => mu/a/b
def getPathFromList(path, *args):
    return PathDelimiter.join(path + list(args))

#mu/a/b => [mu, a, b]
def getPathFromStr(s):
    return s.split(PathDelimiter)
