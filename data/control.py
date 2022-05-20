Data = [
    {'name':'条件', 'type':0, 'subs':[
        {'name':'或', 'type':101},
        {'name':'与', 'type':102},
        {'name':'叶节点', 'type':0, 'subs':[
            {'name':'假', 'type':103},
            {'name':'真', 'type':104},
            {'name':'条件', 'type':105},
        ]},
    ]},
    {'name':'动作', 'type':0, 'subs':[
        {'name':'等待', 'type':201},
        {'name':'动作', 'type':202},
        {'name':'赋值', 'type':203},
        {'name':'计算', 'type':204},
        {'name':'结束', 'type':205},
        {'name':'空操作', 'type':206},
        {'name':'子树', 'type':207},
    ]},
    {'name':'组合', 'type':0, 'subs':[
        {'name':'选择器', 'type':0, 'subs':[
            {'name':'概率选择', 'type':301},
            {'name':'随机选择', 'type':302},
        ]},
        {'name':'序列', 'type':0, 'subs':[
            {'name':'序列', 'type':303},
            {'name':'随机序列', 'type':304},
            {'name':'条件执行', 'type':305},
            {'name':'执行到假', 'type':306},
            {'name':'执行到真', 'type':307},
        ]},
    ]},
]