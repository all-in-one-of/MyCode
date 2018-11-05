import hou
def getChildren(node):
    childList = []
    for n in node.children():
        childList.append(n)
        if node.children():
            childList += getChildren(n)
    return childList

getChildren(hou.node('/'))

# hou.parm() 取值单项
# hou.parmTuple() 取值
# set() 属性设置
# setParms() 设置属性 字典
