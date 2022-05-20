import json
import logging
import time

import common.utils as utils
import g.gg as gg

ConfigFileName = 'config.leibtcfg'

CONFIG_EXAMPLE = {
    'mainwindow_geometry': [0, 0, 100, 100], 
    'scene_setting': {
        "SceneBGColor": "#1c5555",
        "SceneNodeBGColor": "#009500",
        "SceneNodeFocusColor": "#00ff7f",
        "SceneNodeFont": "Courier New,12,-1,5,400,0,0,0,0,0,0,0,0,0,0,1,Regular",
        "SceneNodeFontColor": "#000000",
        "SceneNodeLineColor": "#ffffff",
        "SceneNodeOpSignColor": "#260013",
        "SceneNodeOpSignFocusColor": "#e2e2e2",
        "SceneNodePickedColor": "#ffff00",
        "TreeViewEditingColor": "#00aa00"
    },
    'open_workspaces': {
        'mu':  {'directory': 'f:/mu' },
        'mu2': {'directory': 'f:/mu2'},
    },
    'open_trees': {
        'mu/a': {
            'scale': 1.0,
            'paint_offset': [0, 0]
        },
        'mu/dir/tree': {},
        'mu2/a/t': {},
    },
    'current_editing_tree': 'mu/dir/tree', #当前正在编辑的行为树，tabWidget中的current
    'env': 'debug',
}

#软件配置
@utils.singleton
class Config(object):
    def __init__(self):
        self.data = {}
        self.load()
        self.lastSaveTime = time.time()
    
    def __getitem__(self, name):
        return self.data.get(name, None)
    
    def _getFilename(self):
        return gg.SOFTWARE_TMP_DIR + '/' + ConfigFileName
    
    def save(self, force=False):
        now = time.time()
        if not force:
            if now - self.lastSaveTime < 1:
                #避免太频繁
                return False
        self.lastSaveTime = now
        try:
            with open(self._getFilename(), "w", encoding='utf-8') as f:
                json.dump(self.data, f, sort_keys=True, indent=4)
        except Exception as e:
            logging.exception(e)
            return False
        return True
    
    def load(self):
        try:
            with open(self._getFilename(), "r", encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            logging.exception(e)
            self.data.setdefault('open_workspaces', {})
            return False
        self.data.setdefault('open_workspaces', {})
        return True
    
    def addWorkspace(self, wsName, cfg):
        self.data.setdefault('open_workspaces', {})[wsName] = cfg
        self.save(force=True)
    
    def remWorkspace(self, wsName):
        if self.data['open_workspaces'].pop(wsName, None) is not None:
            self.save(force=True)
    
    def loadOpenWorkspaces(self):
        return self.data.setdefault('open_workspaces', {}).copy()
    
    #移除所有已打开工作区的记忆
    def removeAllOpenWorkspace(self):
        self.data['open_workspaces'] = {}
        self.save(force=True)
    
    #移除所有已打开行为树的记忆
    def removeAllOpenTree(self):
        self.data['open_trees'] = {}
        self.save(force=True)
    
    def loadOpenTrees(self):
        return self.data.setdefault('open_trees', {}).copy()
            
    #保存行为树的落地配置
    def saveTreeCfg(self, tree, cfg):
        if isinstance(tree, list):
            tree = gg.getPathFromList(tree)
        self.data.setdefault('open_trees', {}).setdefault(tree, {}).update(cfg)
        self.save()
    
    #加载行为树的落地配置
    def loadTreeCfg(self, tree):
        if isinstance(tree, list):
            tree = gg.getPathFromList(tree)
        return self.data.setdefault('open_trees', {}).get(tree, {})
    
    def remTreeCfg(self, tree):
        if isinstance(tree, list):
            tree = gg.getPathFromList(tree)
        if self.data.setdefault('open_trees', {}).pop(tree, None) is not None:
            self.save()
    
    def saveMainwindowGeometry(self, g):
        self.data['mainwindow_geometry'] = (g[0], g[1], g[2], g[3])
        self.save()
    
    def loadMainwindowGeometry(self):
        return self.data.get('mainwindow_geometry', None)
    
    def saveSceneSetting(self, data):
        self.data['scene_setting'] = data
        self.save(force=True)
    
    def loadSceneSetting(self):
        return self.data.get('scene_setting', {})

    def saveCurrentEditTree(self, name: str):
        self.data['current_editing_tree'] = name
        self.save(force=True)
    
    def loadCurrentEditTree(self):
        return self.data.get('current_editing_tree', '')
    
    def isDebug(self):
        return self.data.get('env', '') == 'debug'
    
    def loadEnv(self):
        return self.data.get('env', '')
    
    def saveEnv(self, env):
        self.data['env'] = env
        self.save(force=True)

if __name__ == '__main__':
    # print(Config().open_workspaces)
    print(Config()['open_workspaces'])