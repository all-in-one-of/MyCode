from math import sin, cos

geoNet = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
spiral = geoNet.pwd().createNode('curve')
coordsParm = spiral.parm('coords')
height = 30
lRadius = 10.0
uRadius = 0
frequence = 3

coordsStr = ''
radius = lRadius
step = (lRadius - uRadius) / (height * frequence)

for i in range(height*frequence):
    px = str(radius * sin(i))
    py = str(i / frequence)
    pz = str(radius * cos(i))

    coordsStr += px + ',' + py + ',' + pz + ' '
    radius -= step

coordsParm.set(coordsStr)