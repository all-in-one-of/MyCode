# coding=utf-8
import shutil
import time
import math
import cv2
import json
import os
from pypinyin import lazy_pinyin
from PIL import Image, ImageChops, ImageOps, ImageFilter
import pymel.core as pm
from maya import cmds, mel
import maya.OpenMaya as om

GoodsDir = r'F:\Share\goods'


def createDirectory(directory):
    '''
    创建路径，如果文件夹不存在，就创建
    :param directory (str): 创建文件夹
    :return:
    '''
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


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


MayaProjectDir = cmds.workspace(fn=True)
MayaJson = os.path.join(MayaProjectDir, 'Maya.json')
MayaInfo = readJson(MayaJson)

SourceImages = createDirectory(os.path.join(MayaProjectDir, 'sourceimages'))
ScenesDir = createDirectory(os.path.join(MayaProjectDir, 'scenes'))
TexturesDir = createDirectory(os.path.join(MayaProjectDir, 'Textures'))

UnityProjectDir = r'F:\Share\createAssetBundels\Assets\yingtaikeji'
UnityJson = os.path.join(UnityProjectDir, 'unity.json')

SimplyGonDirectory = r'F:\Share\simplygon'
SimplyGonJson = os.path.join(SimplyGonDirectory, 'simplygon.json')

MarmosetDir = r'F:\Share\Marmoset'
MarmosetJson = os.path.join(MarmosetDir, 'Marmoset.json')
MarmosetInfo = readJson(MarmosetJson)

#################################################
MerchantName = 'gaojumingzuo'
MerchantDir = os.path.join(GoodsDir, MerchantName)
MerchantJson = os.path.join(MerchantDir, MerchantName + '.json')
MerchantInfo = readJson(MerchantJson)
GoodsList = MerchantInfo['goodsList']


##########################################


def writeJson(jsonPath, info):
    with open(jsonPath, 'w') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)


def changeTime(allTime):
    day = 24 * 60 * 60
    hour = 60 * 60
    min = 60
    if allTime < 60:
        return "%d sec" % math.ceil(allTime)
    elif allTime > day:
        days = divmod(allTime, day)
        return "%d days, %s" % (int(days[0]), changeTime(days[1]))
    elif allTime > hour:
        hours = divmod(allTime, hour)
        return '%d hours, %s' % (int(hours[0]), changeTime(hours[1]))
    else:
        mins = divmod(allTime, min)
        return "%d mins, %d sec" % (int(mins[0]), math.ceil(mins[1]))


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


def chineseSort(chinese):
    chinese.sort(key=lambda char: lazy_pinyin(char)[0][0])


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
    cmds.file(save=True)


def newScene():
    cmds.file(f=True, new=True)


def openMeshFile(path):
    cmds.file(path, o=True, force=True)
    cmds.viewFit()


def fitView(f=1):
    cmds.viewFit(f=f)


def createPBS(name, direcotory=os.path.join(MayaProjectDir, 'sourceimages')):
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
    for i in os.listdir(MayaProjectDir):
        # 使用simplygon减面
        if i.endswith('AmbientOcclusion.png'):
            im = Image.open(os.path.join(MayaProjectDir, i))
            im = im.resize((512, 512), Image.ANTIALIAS)
            im.save(os.path.join(direcotory, 'T_%s_ao.png' % name))
            os.remove(os.path.join(MayaProjectDir, i))
        if i.endswith('Diffuse.png'):
            im = Image.open(os.path.join(MayaProjectDir, i))
            im = im.resize((2048, 2048), Image.ANTIALIAS)
            im.save(os.path.join(direcotory, 'T_%s_b.png' % name))

            os.remove(os.path.join(MayaProjectDir, i))

        if i.endswith('Normals.png'):
            im = Image.open(os.path.join(MayaProjectDir, i))
            im = im.resize((2048, 2048), Image.ANTIALIAS)
            im.save(os.path.join(direcotory, 'T_%s_n.png' % name))

            os.remove(os.path.join(MayaProjectDir, i))

    shaderName = 'M_' + name + '_w'
    if cmds.objExists(shaderName):
        cmds.delete(shaderName)
    shader = cmds.shadingNode('StingrayPBS', asShader=True, name=shaderName)
    cmds.shaderfx(sfxnode=shader, initShaderAttributes=True)  # 初始化pbs

    shading_group_name = shaderName + 'SG'
    if cmds.objExists(shading_group_name):
        cmds.delete(shading_group_name)
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shading_group_name)
    cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader')

    imges = os.listdir(direcotory)
    for img in imges:
        if img.endswith('%s_b.png' % name):
            baseTex = os.path.join(direcotory, img)
            imageSaveAs(baseTex, (2048, 2048))
            tb = 'T_' + name + '_b'
            if cmds.objExists(tb):
                cmds.delete(tb)
            baseColor = cmds.shadingNode('file', at=True, name=tb)
            cmds.setAttr(shader + '.use_color_map', 1)
            cmds.connectAttr(baseColor + '.outColor', shader + '.TEX_color_map')
            cmds.setAttr(baseColor + '.fileTextureName', baseTex, type='string')

        if img.endswith('%s_n.png' % name):
            noramlTex = os.path.join(direcotory, img)
            imageSaveAs(noramlTex, (2048, 2048))

            tn = 'T_' + name + '_n'
            if cmds.objExists(tn):
                cmds.delete(tn)
            normal = cmds.shadingNode('file', at=True, name=tn)
            cmds.setAttr(shader + '.use_normal_map', 1)
            cmds.connectAttr(normal + '.outColor', shader + '.TEX_normal_map')
            cmds.setAttr(normal + '.fileTextureName', noramlTex, type='string')

        if img.endswith('%s_ao.png' % name):
            aoTex = os.path.join(direcotory, img)
            imageSaveAs(aoTex, (512, 512))

            tao = 'T_' + name + '_ao'
            if cmds.objExists(tao):
                cmds.delete(tao)
            ambientOcclusion = cmds.shadingNode('file', at=True, name=tao)
            cmds.setAttr(shader + '.use_ao_map', 1)
            cmds.connectAttr(ambientOcclusion + '.outColor', shader + '.TEX_ao_map')
            cmds.setAttr(ambientOcclusion + '.fileTextureName', aoTex, type='string')

        if img.endswith('%s_r.png' % name):
            roughnessTex = os.path.join(direcotory, img)
            imageSaveAs(roughnessTex, (512, 512))

            tr = 'T_' + name + '_r'
            if cmds.objExists(tr):
                cmds.delete(tr)
            roughness = cmds.shadingNode('file', at=True, name=tr)
            cmds.setAttr(shader + '.use_roughness_map', 1)
            cmds.connectAttr(roughness + '.outColor', shader + '.TEX_roughness_map')
            cmds.setAttr(roughness + '.fileTextureName', roughnessTex, type='string')

        else:
            cmds.setAttr(shader + '.roughness', 0.5)

        if img.endswith('%s_m.png' % name):
            metallicTex = os.path.join(direcotory, img)
            imageSaveAs(metallicTex, (512, 512))

            tm = 'T_' + name + '_m'
            if cmds.objExists(tm):
                cmds.delete(tm)
            metallic = cmds.shadingNode('file', at=True, name=tm)
            cmds.setAttr(shader + '.use_metallic_map', 1)
            cmds.connectAttr(metallic + '.outColor', shader + '.TEX_metallic_map')
            cmds.setAttr(metallic + '.fileTextureName', metallicTex, type='string')

        if img.endswith('%s_e.png' % name):
            emissiveTex = os.path.join(direcotory, img)
            imageSaveAs(emissiveTex, (512, 512))

            te = 'T_' + name + '_e'
            if cmds.objExists(te):
                cmds.delete(te)
            emissive = cmds.shadingNode('file', at=True, name=te)
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


def createShadow(name, direcotory=os.path.join(MayaProjectDir, 'sourceimages')):
    '''
    创建阴影材质球
    :param name: 名字
    :param direcotory: 文件夹，默认项目文件夹sourceimages
    '''

    if cmds.ls(sl=True, type='dagNode'):
        meshName = cmds.ls(sl=True, type='dagNode')[0]
        bbox = cmds.exactWorldBoundingBox(meshName)
        if abs(bbox[1] - bbox[4]) != 0:

            extend = 15
            shdowsX = (bbox[3] - bbox[0]) + extend
            shdowsZ = (bbox[5] - bbox[2]) + extend
            panleName = 'shadow'

            if cmds.objExists(panleName):
                cmds.delete(panleName)

            sPlane = cmds.polyPlane(w=shdowsX, h=shdowsZ, sx=1, sy=1, n=panleName)
            meshName = sPlane[0]

    else:
        cmds.warning(u'未选择模型')
        return

    # 如果有阴影贴图，直接贴
    if 'T_%s_s.png' % name in os.listdir(direcotory):
        shaderName = 'M_' + name + '_s'
        if cmds.objExists(shaderName):
            cmds.delete(shaderName)
        shader = cmds.shadingNode('lambert', asShader=True, name=shaderName)

        shading_group_name = shaderName + 'SG'
        if cmds.objExists(shading_group_name):
            cmds.delete(shading_group_name)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shading_group_name)
        cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader')
        shadowTex = os.path.join(direcotory, 'T_%s_s.png' % name)
        shadowName = 'T_' + name + '_s'

        if cmds.objExists(shadowName):
            cmds.delete(shadowName)
        shadow = cmds.shadingNode('file', at=True, name=shadowName)
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
        shapes = cmds.listRelatives(meshName, s=True)[0]
        bakeAO = 'ilrTextureBakeCmd -target "%s" -frontRange 0 -backRange 200 -frontBias 0 -backBias -100 -transferSpace 1 -selectionMode 0 -mismatchMode 0 -envelopeMode 0 -ignoreInconsistentNormals 1 -considerTransparency 0 -transparencyThreshold 0.001000000047 -camera "persp" -normalDirection 0 -shadows 1 -alpha 1 -viewDependent 0 -orthoRefl 1 -backgroundColor 0 0 0 -frame 1 -bakeLayer TurtleDefaultBakeLayer -width 512 -height 512 -saveToRenderView 0 -saveToFile 1 -directory "%s/turtle/bakedTextures/" -fileName "baked_$p_$s.$e" -fileFormat 9 -visualize 0 -uvRange 0 -uMin 0 -uMax 1 -vMin 0 -vMax 1 -uvSet "" -tangentUvSet "" -edgeDilation 5 -bilinearFilter 1 -merge 0 -conservative 0 -windingOrder 1 -fullShading 1 -useRenderView 1 -layer defaultRenderLayer' % (
            shapes, MayaProjectDir)
        pm.mel.eval(bakeAO)

        cmds.select(meshName)
        aoMapAdjust(os.path.join(direcotory, 'T_%s_s.png' % name),
                    os.path.join(MayaProjectDir, r"turtle\bakedTextures\baked_beauty_%s.png" % shapes))

        createShadow(name)
    return meshName


def exportFBX(path, selection=True):
    if selection is True:
        cmds.FBXExport('-file', path, '-s')
    if selection is False:
        cmds.FBXExport('-file', path)


def saveScreenshot(name, directory=TexturesDir):
    # 图片保存路径
    cmds.displayRGBColor('backgroundTop', 1, 1, 1)
    cmds.displayRGBColor('backgroundBottom', 1, 1, 1)
    cmds.displayRGBColor('background', 1, 1, 1)
    cmds.setAttr("perspShape.focalLength", 50)
    path = os.path.join(directory, '%s.jpg' % name)
    cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', 1)
    cmds.viewFit(f=1)  # 聚焦物体
    cmds.setAttr('defaultRenderGlobals.imageFormat', 8)  # 设置默认渲染器图片格式 8位jpg
    # 使用playblast 的方式保存截图
    cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=2048, height=2048,
                   showOrnaments=False, startTime=1, endTime=1, viewer=False)
    cmds.displayRGBColor(rs=True)

    return path


def upTextures(name, directory, goodsImage=False):
    textureDir = os.path.join(MayaProjectDir, 'sourceimages')

    if goodsImage:
        try:
            shutil.copy(os.path.join(TexturesDir, '%s.jpg' % name), directory)
        except:
            cmds.warning(u'缺少商品图片')
            return
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
    for i in os.listdir(MayaProjectDir):
        if i.endswith('Diffuse.png'):
            diffuseImage = os.path.join(MayaProjectDir, i)
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

    im2.save(os.path.join(MayaProjectDir, 'sourceimages\T_%s_m.png' % name))
    im0.save(os.path.join(MayaProjectDir, 'Diffuse.png'))


def exportTo(name, simplygon=False, unity=False, marmoset=False):
    if simplygon:
        simplygonInfo = readJson(SimplyGonJson)
        simplygonInfo['Execute'].append(name)
        fbxName = os.path.join(r'F:\Share\simplygon\standby', '%s.fbx' % name)
        cmds.FBXExportEmbeddedTextures('-v', True)
        cmds.FBXExport('-file', fbxName, '-s')
        writeJson(SimplyGonJson, simplygonInfo)

    elif unity:
        unityInfo = readJson(UnityJson)
        unityDirPath = createDirectory(os.path.join(UnityProjectDir, name))
        try:
            cmds.select('s' + name)
        except:
            cmds.warning(u'未找到', 's' + name)
            return name

        if cmds.objExists('shadow'):
            try:
                cmds.parent('shadow', 's' + name)
            except:
                cmds.warning(u'未知原因')
                return name

        else:
            cmds.warning(u'缺少阴影')
            return name

        fbxName = os.path.join(unityDirPath, 's%s.fbx' % name)
        cmds.FBXExport('-file', fbxName, '-s')
        cmds.parent('shadow', world=True)

        upTextures(name, unityDirPath)
        unityInfo['Execute'].append(name)
        writeJson(UnityJson, unityInfo)
    elif marmoset:
        fbxDir = createDirectory(os.path.join(MarmosetDir, 'fbx'))
        fbxName = os.path.join(fbxDir, name + '.fbx')
        try:
            cmds.select('s' + name)
            cmds.FBXExport('-file', fbxName, '-s')
            upTextures(name, fbxDir)
            if name in MayaInfo['Marmoset']:
                MayaInfo['Marmoset'].remove(name)
            if name not in MarmosetInfo['Execute']:
                MarmosetInfo['Execute'].append(name)
        except:
            MayaInfo['Error']['Marmoset'].append(name)
        writeJson(MarmosetJson, MarmosetInfo)
        writeJson(MayaJson, MayaInfo)


def importSimplyGon(name):
    simplygonOutDir = r'F:\Share\simplygon\outputDir\lowPix'
    fbxPath = os.path.join(simplygonOutDir, '%s/LOD1/%s_lowPix_LOD1.fbx' % (name, name))
    ao = r"F:\Share\simplygon\outputDir\lowPix\%s\LOD1\Textures\AmbientOcclusion.png" % name
    d = r"F:\Share\simplygon\outputDir\lowPix\%s\LOD1\Textures\Diffuse.png" % name
    n = r"F:\Share\simplygon\outputDir\lowPix\%s\LOD1\Textures\Normals.png" % name

    try:
        shutil.copy(ao, MayaProjectDir)
        shutil.copy(d, MayaProjectDir)
        shutil.copy(n, MayaProjectDir)
        importMeshFile(fbxPath)

    except:
        cmds.warning('导入失败')
        return


def createNewScene(name):
    newScene()
    sceneDir = os.path.join(MayaProjectDir, 'scenes')
    sceneFile = os.path.join(sceneDir, name)
    cmds.file(rename=sceneFile)
    cmds.file(save=True, force=True, type='mayaAscii')


def removeShadow():
    try:
        cmds.polySeparate(cmds.ls(g=1)[0], ch=0)
    except:
        pass

    for shape in cmds.ls(g=True):
        bbox = cmds.exactWorldBoundingBox(shape)
        if abs(bbox[4] - bbox[1]) <= 1:
            cmds.delete(cmds.listRelatives(shape, p=1)[0])
        else:
            for i in cmds.ls(assemblies=True):
                g = cmds.listRelatives(i, type='transform')
                if g:
                    cmds.select(i)
                    cmds.ungroup()
                    try:
                        cmds.sets(g, e=True, fe='initialShadingGroup')
                    except:
                        pass


def deleteUnused():
    try:
        mel.eval('MLdeleteUnused')
    except:
        cmds.warning('未清理')


def temp1():
    startTime = time.time()
    goodsInfo = readJson(r"F:\Share\goods\rongdingxuanhongmu\rongdingxuanhongmu.json")
    rdxDir = r'F:\Share\2018\rdx'
    rdxInfo = readJson(r"F:\Share\goods\rongdingxuanhongmu\rdx.json")

    goodsList = goodsInfo['goodsList']

    scenesDir = os.path.join(MayaProjectDir, 'scenes')
    sourceImagesDir = os.path.join(MayaProjectDir, 'sourceimages')
    texturesDir = os.path.join(MayaProjectDir, 'Textures')
    errorList = []

    for i in goodsList:

        maFile = os.path.join(scenesDir, i + '.ma')
        contrastSKU = rdxInfo[goodsList.index(i)][1]

        contrastDir = os.path.join(rdxDir, contrastSKU)
        print contrastDir
        images = findSpecifiedFile(contrastDir, 'png')
        goodsImage = findSpecifiedFile(contrastDir, '.jpg')[0]

        shutil.copyfile(goodsImage, os.path.join(texturesDir, i + '.jpg'))

        for img in images:
            if img.endswith('_s.png'):
                shadowTex = img
                shutil.copyfile(shadowTex, os.path.join(sourceImagesDir, 'T_%s_s.png' % i))
            elif img.endswith('AmbientOcclusion.png') or img.endswith('ao.png'):
                aoTex = img
                shutil.copyfile(aoTex, os.path.join(sourceImagesDir, 'T_%s_ao.png' % i))

            elif img.endswith('Diffuse.png') or img.endswith('b.png'):
                diffuseTex = img
                shutil.copyfile(diffuseTex, os.path.join(sourceImagesDir, 'T_%s_b.png' % i))

            elif img.endswith('Normals.png') or img.endswith('n.png'):
                normalTex = img
                shutil.copyfile(normalTex, os.path.join(sourceImagesDir, 'T_%s_n.png' % i))

            elif img.endswith('m.png') or img.endswith('m.png'):
                metallicTex = img
                shutil.copyfile(metallicTex, os.path.join(sourceImagesDir, 'T_%s_m.png' % i))
            elif img.endswith('r.png'):
                roughnessTex = img
                shutil.copyfile(roughnessTex, os.path.join(sourceImagesDir, 'T_%s_r.png' % i))

        try:
            openMeshFile(maFile)
            cmds.select(cmds.ls(g=True))
            createPBS(i)
            createShadow(i)
            deleteUnused()
            cmds.file(save=True)

        except:
            errorList.append(contrastSKU)

        print i

    print errorList
    print changeTime(time.time() - startTime)


def temp2():
    startTime = time.time()
    goodsInfo = readJson(r"F:\Share\goods\rongdingxuanhongmu\rongdingxuanhongmu.json")
    rdxDir = r'F:\Share\2018\rdx'
    rdxInfo = readJson(r"F:\Share\goods\rongdingxuanhongmu\rdx.json")

    goodsList = goodsInfo['goodsList']

    scenesDir = os.path.join(MayaProjectDir, 'scenes')
    sourceImagesDir = os.path.join(MayaProjectDir, 'sourceimages')
    texturesDir = os.path.join(MayaProjectDir, 'Textures')
    errorList = []

    for i in goodsList:

        maFile = os.path.join(scenesDir, i + '.ma')
        contrastSKU = rdxInfo[goodsList.index(i)][1]

        openMeshFile(maFile)
        mesh = cmds.listRelatives(cmds.ls(g=True)[0], p=True)[0]
        cmds.select(mesh)
        createPBS(i)
        createShadow(i)
        deleteUnused()
        e = exportTo(i, unity=True)
        if e:
            errorList.append(e)

        cmds.file(save=True)

        print i

    print changeTime(time.time() - startTime)
    print errorList


def toUnityPackage():
    errorList = readJson(os.path.join(MayaProjectDir, 'errorList.json'))
    scenesDir = os.path.join(MayaProjectDir, 'scenes')

    for i in errorList:
        maFile = os.path.join(scenesDir, i + '.ma')
        openMeshFile(maFile)

        cmds.select('s' + i)

        createPBS(i)
        createShadow(i)
        deleteUnused()
        e = exportTo(i, unity=True)
        if e is None:
            errorList.remove(i)

        cmds.file(save=True)
        print i
    writeJson(os.path.join(MayaProjectDir, 'errorList.json'), errorList)
    if errorList == []:
        print u'修改完成'
    else:
        print errorList, u'需要修改'


def autoManage(marmoset=False):
    startTime = time.time()
    marmosetList = MayaInfo['Marmoset'][:]
    if marmoset:
        for sku in marmosetList:
            maFile = os.path.join(ScenesDir, sku + '.ma')
            openMeshFile(maFile)
            exportTo(sku, marmoset=True)
    print changeTime(time.time() - startTime)


def revision(name, marmoset=False):
    if marmoset:
        try:
            exportTo(name, marmoset=True)
            MarmosetInfo['Error'].remove(name)
        except:
            print 'Error'
        writeJson(MarmosetJson, MarmosetInfo)


def getUvShelList(name):
    selList = om.MSelectionList()
    selList.add(name)
    selListIter = om.MItSelectionList(selList, om.MFn.kMesh)
    pathToShape = om.MDagPath()
    selListIter.getDagPath(pathToShape)
    meshNode = pathToShape.fullPathName()
    uvSets = cmds.polyUVSet(meshNode, query=True, allUVSets=True)
    allSets = []
    for uvset in uvSets:
        shapeFn = om.MFnMesh(pathToShape)
        shells = om.MScriptUtil()
        shells.createFromInt(0)
        # shellsPtr = shells.asUintPtr()
        nbUvShells = shells.asUintPtr()

        uArray = om.MFloatArray()  # array for U coords
        vArray = om.MFloatArray()  # array for V coords
        uvShellIds = om.MIntArray()  # The container for the uv shell Ids

        shapeFn.getUVs(uArray, vArray)
        shapeFn.getUvShellsIds(uvShellIds, nbUvShells, uvset)

        # shellCount = shells.getUint(shellsPtr)
        shells = {}
        for i, n in enumerate(uvShellIds):
            if n in shells:
                # shells[n].append([uArray[i],vArray[i]])
                shells[n].append('%s.map[%i]' % (name, i))
            else:
                # shells[n] = [[uArray[i],vArray[i]]]
                shells[n] = ['%s.map[%i]' % (name, i)]
        allSets.append({uvset: shells})
    return allSets


def createMoc(size, name):
    name = 'moc_' + name
    a = cmds.polyCube(w=size[0], d=size[1], h=size[2], n=name)
    cmds.select(a)
    returnZero()


def saveMa(name, dir=ScenesDir):
    name = os.path.join(dir, name)
    cmds.file(rename=name)
    cmds.file(save=True, type='mayaAscii', force=True)


def returnZero():
    curSel = cmds.ls(long=True, selection=True, type='dagNode')
    cmds.makeIdentity(a=True)
    for n in curSel:
        bbox = cmds.exactWorldBoundingBox(n)
        bottom = [(bbox[0] + bbox[3]) / 2, bbox[1], (bbox[2] + bbox[5]) / 2]
        cmds.xform(n, piv=bottom, ws=True)

    cmds.xform(n, translation=[-bottom[0], -bottom[1], -bottom[2]])
    cmds.makeIdentity(a=True)
    cmds.DeleteAllHistory()


def temp3():
    startTime = time.time()
    errorList = []
    try:
        for sku in GoodsList:
            goodsDir = os.path.join(MerchantDir, sku)
            goodsJson = os.path.join(goodsDir, sku + '.json')
            goodsInfo = readJson(goodsJson)

            size = goodsInfo['size']
            createNewScene(sku)
            createMoc(size, sku)
            saveMa(sku, goodsDir)
    except:
        errorList.append(sku)

    print changeTime(time.time() - startTime)
    print errorList


def load(sku):
    goodsDir = os.path.join(MerchantDir, sku)
    maFile = os.path.join(goodsDir, sku + '.ma')
    if os.path.exists(maFile):
        shutil.copy(maFile, ScenesDir)
        openMeshFile(os.path.join(ScenesDir, sku + '.ma'))
