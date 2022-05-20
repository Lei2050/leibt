from PyQt6.QtGui import QPainterPath
from PyQt6.QtCore import QLineF, QPointF

#绘制多边形 - 填充
def painterPolygon(painter, vertices, brush):
    if len(vertices) <= 1:
        return
    path = QPainterPath()
    path.moveTo(vertices[0][0], vertices[0][1])
    for v in vertices[1:]:
        path.lineTo(v[0], v[1])
    path.lineTo(vertices[0][0], vertices[0][1])
    painter.fillPath(path, brush)

#绘制多边形 - 不填充
def painterPolygonLine(painter, vertices):
    if len(vertices) <= 1:
        return
    vertices.append(vertices[0])
    lines = [QLineF(QPointF(vertices[i][0], vertices[i][1]), QPointF(vertices[i+1][0], vertices[i+1][1])) for i in range(len(vertices) - 1)]
    painter.drawLines(lines)
        
def SetupWidgetUI(widget, ui, cls):
    try:
        path = f"ui_design.{ui}"
        name = f"{ui}"
        module = __import__(path, fromlist=[name, ])
        uiclass = getattr(module, f'Ui_{cls}', None)()
        uiclass.setupUi(widget)
        return uiclass
    except Exception as e:
        # print('SetupWidgetUI %s %s failed, err:%s' % (path, cls, e))
        pass
    return None

def FindOneWidgetInWidget(parent, cls, name):
    widget = parent.findChildren(cls, name)
    if not widget:
        return None
    return widget[0]
