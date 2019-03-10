# coding=utf-8
import shutil

import cv2
import json
import os
from pypinyin import lazy_pinyin
from PIL import Image, ImageChops, ImageOps, ImageFilter
import pymel.core as pm
from maya import cmds

MAYAPROJECT = cmds.workspace(fn=True)


def findSpecifiedFile(path, suffix=''):
    '''
    查找指定文件
    :param path: 根目录
    :param suffix: 格式，默认是空
    :return: 文件地址列表
    '''
    _file = []
    path = path.decode('utf-8')
    for root, dirs, fils in os.walk(path):
        for file in fils:
            if file.endswith(suffix):
                _file.append(os.path.join(root, file))
    return _file


def baseNameForPath(path, suffix=True):
    '''
    获取路径文件名
    :param path: 文件路径
    :param suffix: 是否需要后缀
    :return: 文件名
    '''
    name = os.path.basename(path)
    if suffix:
        return name

    else:
        name, b = os.path.splitext(name)
        return name


def readJson(path):
    """
    读取json
    :param path: json文件
    :return: 字典
    """
    with open(path, 'r') as f:
        _info = json.load(f)  # 导入json文件
        # b = json.dumps(info, encoding="utf-8", ensure_ascii=False)  # 转码成字符串
        # c = eval(b)  # 转回字典
    return _info  # 返回字典


def chineseSort(chinese):
    chinese.sort(key=lambda char: lazy_pinyin(char)[0][0])


def createDirectory(directory):
    '''
    创建路径，如果文件夹不存在，就创建
    :param directory (str): 创建文件夹
    :return:
    '''
    if not os.path.exists(directory):
        os.mkdir(directory)


def imageSaveAs(oPath, size, tPath=None, suffix=None):
    if tPath is None and suffix is None:
        tPath = oPath
    elif suffix is True:
        tPath = oPath.replace(oPath.split('.')[-1], suffix)
    im = Image.open(oPath)
    im = im.resize(size, Image.ANTIALIAS)
    im.save(tPath)
    return im


# **************************************************************
def importMeshFile(path):
    cmds.file(path, i=True, force=True)
    cmds.viewFit()


def newScene():
    cmds.file(f=True, new=True)


def openMeshFile(path):
    cmds.file(path, o=True, force=True)
    cmds.viewFit()


def fitView(f=1):
    cmds.viewFit(f=f)


def createPBS(name, direcotory=os.path.join(MAYAPROJECT, 'sourceimages')):
    '''
    创建pbs
    :param name: 名字
    :param direcotory: 贴图文件夹，默认项目文件夹sourceimages
    :return:
    '''
    if cmds.ls(sl=True, type='dagNode'):
        meshName = cmds.ls(sl=True, type='dagNode')[0]
    else:
        cmds.warning(u'未选择模型')
        return
    for i in os.listdir(MAYAPROJECT):
        # 使用simplygon减面
        if i.endswith('AmbientOcclusion.png'):
            im = Image.open(os.path.join(MAYAPROJECT, i))
            im = im.resize((512, 512), Image.ANTIALIAS)
            im.save(os.path.join(direcotory, 'T_%s_ao.png' % name))
            os.remove(os.path.join(MAYAPROJECT, i))
        if i.endswith('Diffuse.png'):
            im = Image.open(os.path.join(MAYAPROJECT, i))
            im = im.resize((2048, 2048), Image.ANTIALIAS)
            im.save(os.path.join(direcotory, 'T_%s_b.png' % name))

            os.remove(os.path.join(MAYAPROJECT, i))

        if i.endswith('Normals.png'):
            im = Image.open(os.path.join(MAYAPROJECT, i))
            im = im.resize((2048, 2048), Image.ANTIALIAS)
            im.save(os.path.join(direcotory, 'T_%s_n.png' % name))

            os.remove(os.path.join(MAYAPROJECT, i))

    shaderName = 'M_' + name + '_w'
    shader = cmds.shadingNode('StingrayPBS', asShader=True, name=shaderName)
    cmds.shaderfx(sfxnode=shader, initShaderAttributes=True)  # 初始化pbs

    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shaderName + 'SG')
    cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader')

    imges = os.listdir(direcotory)
    for img in imges:
        if img.endswith('%s_b.png' % name):
            baseTex = os.path.join(direcotory, img)
            imageSaveAs(baseTex, (2048, 2048))

            baseColor = cmds.shadingNode('file', at=True, name='T_' + name + '_b')
            cmds.setAttr(shader + '.use_color_map', 1)
            cmds.connectAttr(baseColor + '.outColor', shader + '.TEX_color_map')
            cmds.setAttr(baseColor + '.fileTextureName', baseTex, type='string')

        if img.endswith('%s_n.png' % name):
            noramlTex = os.path.join(direcotory, img)
            imageSaveAs(baseTex, (2048, 2048))

            normal = cmds.shadingNode('file', at=True, name='T_' + name + '_n')
            cmds.setAttr(shader + '.use_normal_map', 1)
            cmds.connectAttr(normal + '.outColor', shader + '.TEX_normal_map')
            cmds.setAttr(normal + '.fileTextureName', noramlTex, type='string')

        if img.endswith('%s_ao.png' % name):
            aoTex = os.path.join(direcotory, img)
            imageSaveAs(aoTex, (512, 512))

            ambientOcclusion = cmds.shadingNode('file', at=True, name='T_' + name + '_ao')
            cmds.setAttr(shader + '.use_ao_map', 1)
            cmds.connectAttr(ambientOcclusion + '.outColor', shader + '.TEX_ao_map')
            cmds.setAttr(ambientOcclusion + '.fileTextureName', aoTex, type='string')

        if img.endswith('%s_r.png' % name):
            roughnessTex = os.path.join(direcotory, img)
            imageSaveAs(roughnessTex, (512, 512))

            roughness = cmds.shadingNode('file', at=True, name='T_' + name + '_r')
            cmds.setAttr(shader + '.use_roughness_map', 1)
            cmds.connectAttr(roughness + '.outColor', shader + '.TEX_roughness_map')
            cmds.setAttr(roughness + '.fileTextureName', roughnessTex, type='string')

        else:
            cmds.setAttr(shader + '.roughness', 0.5)

        if img.endswith('%s_m.png' % name):
            metallicTex = os.path.join(direcotory, img)
            imageSaveAs(metallicTex, (512, 512))
            metallic = cmds.shadingNode('file', at=True, name='T_' + name + '_m')
            cmds.setAttr(shader + '.use_metallic_map', 1)
            cmds.connectAttr(metallic + '.outColor', shader + '.TEX_metallic_map')
            cmds.setAttr(metallic + '.fileTextureName', metallicTex, type='string')

        if img.endswith('%s_e.png' % name):
            emissiveTex = os.path.join(direcotory, img)
            imageSaveAs(emissiveTex, (512, 512))

            emissive = cmds.shadingNode('file', at=True, name='T_' + name + '_e')
            cmds.setAttr(shader + '.use_emissive_map', 1)
            cmds.connectAttr(emissive + '.outColor', shader + '.TEX_emissive_map')
            cmds.setAttr(emissive + '.fileTextureName', emissiveTex, type='string')

    cmds.sets(meshName, e=True, fe=shading_group)
    cmds.select(meshName)
    return meshName


def aoMapAdjust(taImage, imge=r"D:\HKW\mayacontroller\turtle\bakedTextures\baked_beauty_pPlaneShape1.png"):
    img = Image.open(imge)
    img = img.convert('L')
    pixel = []
    for i in range(512):
        pixel.append(img.getpixel((i, 0)))
        pixel.append(img.getpixel((0, i)))
        pixel.append(img.getpixel((i, 511)))
        pixel.append(img.getpixel((511, i)))

    cvimg = cv2.imread(imge)
    ret, thresh3 = cv2.threshold(cvimg, min(pixel), 255, cv2.THRESH_TRUNC)
    cv2.imwrite(imge, thresh3)
    img = Image.open(imge)
    img = img.convert('L')
    img = ImageOps.autocontrast(img)
    img = ImageChops.invert(img)
    img = img.filter(ImageFilter.GaussianBlur(2.5))
    img1 = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    img1.putalpha(img)
    # img1.show()
    img1.save(taImage)


def initializeTurtle():
    '''
    海龟烘培ao
    :return:
    '''
    # Load Turtle

    pluginStatus = cmds.pluginInfo("Turtle", q=True, l=True, n=True)
    if pluginStatus == False:
        cmds.loadPlugin("Turtle")

    # Create bake nodes
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "turtle", type="string")
    tOptions = cmds.createNode("ilrOptionsNode", name="TurtleRenderOptions")
    tBakeLayer = cmds.createNode("ilrBakeLayer", name="TurtleDefaultBakeLayer")
    tbakeLayerMgr = cmds.createNode("ilrBakeLayerManager", name="TurtleBakeLayerManager")

    # cmds.setAttr(tOptions + '.renderer', 1)
    # cmds.setAttr(tOptions + '.aaMaxSampleRate', 4)
    # cmds.setAttr(tOptions + '.aaMinSampleRate', 2)
    # cmds.setAttr(tBakeLayer + '.tbImageFormat', 9)

    cmds.connectAttr(tOptions + ".message", tBakeLayer + ".renderOptions")
    cmds.connectAttr(tBakeLayer + ".index", tbakeLayerMgr + ".bakeLayerId[0]")

    # cmds.connectAttr(mesh + ".instObjGroups[0]", tBakeLayer + ".dagSetMembers[0]")


def createShadow(name, direcotory=os.path.join(MAYAPROJECT, 'sourceimages')):
    '''
    创建阴影材质球
    :param name: 名字
    :param direcotory: 文件夹，默认项目文件夹sourceimages
    '''
    if cmds.ls(sl=True, type='dagNode'):
        meshName = cmds.ls(sl=True, type='dagNode')[0]
        if meshName != 'pPlane1':
            bbox = cmds.exactWorldBoundingBox(meshName)
            extend = 15
            shdowsX = (bbox[3] - bbox[0]) + extend
            shdowsZ = (bbox[5] - bbox[2]) + extend
            sPlane = cmds.polyPlane(w=shdowsX, h=shdowsZ, sx=1, sy=1)
            meshName = sPlane[0]

    else:
        cmds.warning(u'未选择模型')
        return

    # 如果有阴影贴图，直接贴
    if 'T_%s_s.png' % name in os.listdir(direcotory):
        shaderName = 'M_' + name + '_s'
        shader = cmds.shadingNode('lambert', asShader=True, name=shaderName)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shaderName + 'SG')
        cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader')
        shadowTex = os.path.join(direcotory, 'T_%s_s.png' % name)
        shadow = cmds.shadingNode('file', at=True, name='T_' + name + '_s')
        cmds.connectAttr(shadow + '.outColor', shader + '.color')
        cmds.connectAttr(shadow + '.outTransparency', shader + '.transparency')

        cmds.setAttr(shadow + '.fileTextureName', shadowTex, type='string')
        cmds.sets(meshName, e=True, fe=shading_group)

    else:
        initializeTurtle()
        sShader = cmds.shadingNode('ilrOccSampler', asShader=True)
        cmds.select(meshName)
        cmds.hyperShade(a=sShader, assign=True)
        cmds.setAttr('%s.maxSamples' % sShader, 512)
        cmds.setAttr('%s.minSamples' % sShader, 128)

        cmds.setAttr('%s.output' % sShader, 3)
        cmds.setAttr('%s.enableAdaptiveSampling' % sShader, 0)
        pm.mel.eval(
            'ilrTextureBakeCmd -target "pPlaneShape1" -frontRange 0 -backRange 200 -frontBias 0 -backBias -100 -transferSpace 1 -selectionMode 0 -mismatchMode 0 -envelopeMode 0 -ignoreInconsistentNormals 1 -considerTransparency 0 -transparencyThreshold 0.001000000047 -camera "persp" -normalDirection 0 -shadows 1 -alpha 1 -viewDependent 0 -orthoRefl 1 -backgroundColor 0 0 0 -frame 1 -bakeLayer TurtleDefaultBakeLayer -width 512 -height 512 -saveToRenderView 0 -saveToFile 1 -directory "D:/HKW/rdx/turtle/bakedTextures/" -fileName "baked_$p_$s.$e" -fileFormat 9 -visualize 0 -uvRange 0 -uMin 0 -uMax 1 -vMin 0 -vMax 1 -uvSet "" -tangentUvSet "" -edgeDilation 5 -bilinearFilter 1 -merge 0 -conservative 0 -windingOrder 1 -fullShading 1 -useRenderView 1 -layer defaultRenderLayer')

        cmds.select(meshName)
        aoMapAdjust(os.path.join(direcotory, 'T_%s_s.png' % name),
                    os.path.join(MAYAPROJECT, r"turtle\bakedTextures\baked_beauty_pPlaneShape1.png"))

        createShadow(name)
    return meshName


def exportFBX(path, selection=True):
    if selection is True:
        cmds.FBXExport('-file', path, '-s')
    if selection is False:
        cmds.FBXExport('-file', path)


def saveScreenshot(name, directory):
    # 图片保存路径
    cmds.displayRGBColor('backgroundTop', 1, 1, 1)
    cmds.displayRGBColor('backgroundBottom', 1, 1, 1)
    cmds.displayRGBColor('background', 1, 1, 1)
    cmds.setAttr("perspShape.focalLength", 60)
    path = os.path.join(directory, '%s.jpg' % name)
    cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
    cmds.viewFit(f=1)  # 聚焦物体
    cmds.setAttr('defaultRenderGlobals.imageFormat', 8)  # 设置默认渲染器图片格式 8位jpg
    # 使用playblast 的方式保存截图
    cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=2048, height=2048,
                   showOrnaments=False, startTime=1, endTime=1, viewer=False)
    cmds.displayRGBColor(rs=True)

    return path


def upTextures(name, directory):
    textureDir = os.path.join(MAYAPROJECT, 'sourceimages')
    try:
        shutil.copy(os.path.join(textureDir, '%s.jpg' % name), directory)
    except:
        pass
    try:
        shutil.copy(os.path.join(textureDir, 'T_%s_b.png' % name), directory)
    except:
        pass
    try:
        shutil.copy(os.path.join(textureDir, 'T_%s_n.png' % name), directory)
    except:
        pass
    try:
        shutil.copy(os.path.join(textureDir, 'T_%s_r.png' % name), directory)
    except:
        pass
    try:
        shutil.copy(os.path.join(textureDir, 'T_%s_m.png' % name), directory)
    except:
        pass
    try:
        shutil.copy(os.path.join(textureDir, 'T_%s_e.png' % name), directory)
    except:
        pass
    try:
        shutil.copy(os.path.join(textureDir, 'T_%s_ao.png' % name), directory)
    except:
        pass
    try:
        shutil.copy(os.path.join(textureDir, 'T_%s_s.png' % name), directory)
    except:
        pass


def createMetallicTex(name):
    for i in os.listdir(MAYAPROJECT):
        if i.endswith('Diffuse.png'):
            diffuseImage = os.path.join(MAYAPROJECT,i)
            break
        else:
            diffuseImage = None

    if diffuseImage is None:
        cmds.error(u'未找到diffuse')
        return

    im0 = Image.open(diffuseImage)

    im1 = im0.convert('L')
    im2 = Image.new('L', im0.size, 0)

    b = []

    for x in range(im0.size[0]):
        for y in range(im0.size[1]):
            a = im1.getpixel((x, y))
            if 200 <= a <= 255:
                b.append((x, y))

    for i in b:
        im2.putpixel(i, 255)
        im0.putpixel(i, (226, 191, 141))

    im2.save(os.path.join(MAYAPROJECT, 'sourceimages\T_%s_m.png' % name))
    im0.save(os.path.join(MAYAPROJECT, 'Diffuse.png'))
