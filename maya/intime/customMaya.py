# coding=utf-8
import json
import os
# from PIL import Image

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

#
# def createPBS(name, direcotory=os.path.join(MAYAPROJECT, 'sourceimages')):
#     '''
#     创建pbs
#     :param name: 名字
#     :param direcotory: 贴图文件夹，默认项目文件夹sourceimages
#     :return:
#     '''
#     if cmds.ls(sl=True, type='dagNode'):
#         meshName = cmds.ls(sl=True, type='dagNode')[0]
#     else:
#         cmds.warning(u'未选择模型')
#         return
#     for i in os.listdir(MAYAPROJECT):
#         # 使用simplygon减面
#         if i.endswith('AmbientOcclusion.png'):
#             im = Image.open(os.path.join(MAYAPROJECT, i))
#             im = im.resize((512, 512), Image.ANTIALIAS)
#             im.save(os.path.join(direcotory, 'T_%s_ao.png' % name))
#             os.remove(os.path.join(MAYAPROJECT, i))
#         if i.endswith('Diffuse.png'):
#             im = Image.open(os.path.join(MAYAPROJECT, i))
#             im = im.resize((2048, 2048), Image.ANTIALIAS)
#             im.save(os.path.join(direcotory, 'T_%s_b.png' % name))
#
#             os.remove(os.path.join(MAYAPROJECT, i))
#
#         if i.endswith('Normals.png'):
#             im = Image.open(os.path.join(MAYAPROJECT, i))
#             im = im.resize((2048, 2048), Image.ANTIALIAS)
#             im.save(os.path.join(direcotory, 'T_%s_n.png' % name))
#
#             os.remove(os.path.join(MAYAPROJECT, i))
#
#     shaderName = 'M_' + name + '_w'
#     shader = cmds.shadingNode('StingrayPBS', asShader=True, name=shaderName)
#     cmds.shaderfx(sfxnode=shader, initShaderAttributes=True)  # 初始化pbs
#
#     shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shaderName + 'SG')
#     cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader')
#
#     imges = os.listdir(direcotory)
#     for img in imges:
#         if img.endswith('%s_b.png' % name):
#             baseTex = os.path.join(direcotory, img)
#             baseColor = cmds.shadingNode('file', at=True, name='T_' + name + '_b')
#             cmds.setAttr(shader + '.use_color_map', 1)
#             cmds.connectAttr(baseColor + '.outColor', shader + '.TEX_color_map')
#             cmds.setAttr(baseColor + '.fileTextureName', baseTex, type='string')
#
#         if img.endswith('%s_n.png' % name):
#             noramlTex = os.path.join(direcotory, img)
#             normal = cmds.shadingNode('file', at=True, name='T_' + name + '_n')
#             cmds.setAttr(shader + '.use_normal_map', 1)
#             cmds.connectAttr(normal + '.outColor', shader + '.TEX_normal_map')
#             cmds.setAttr(normal + '.fileTextureName', noramlTex, type='string')
#
#         if img.endswith('%s_ao.png' % name):
#             aoTex = os.path.join(direcotory, img)
#             ambientOcclusion = cmds.shadingNode('file', at=True, name='T_' + name + '_ao')
#             cmds.setAttr(shader + '.use_ao_map', 1)
#             cmds.connectAttr(ambientOcclusion + '.outColor', shader + '.TEX_ao_map')
#             cmds.setAttr(ambientOcclusion + '.fileTextureName', aoTex, type='string')
#
#         if img.endswith('%s_r.png' % name):
#             roughnessTex = os.path.join(direcotory, img)
#             roughness = cmds.shadingNode('file', at=True, name='T_' + name + '_r')
#             cmds.setAttr(shader + '.use_roughness_map', 1)
#             cmds.connectAttr(roughness + '.outColor', shader + '.TEX_roughness_map')
#             cmds.setAttr(roughness + '.fileTextureName', roughnessTex, type='string')
#
#         if img.endswith('%s_m.png' % name):
#             metallicTex = os.path.join(direcotory, img)
#             metallic = cmds.shadingNode('file', at=True, name='T_' + name + '_m')
#             cmds.setAttr(shader + '.use_metallic_map', 1)
#             cmds.connectAttr(metallic + '.outColor', shader + '.TEX_metallic_map')
#             cmds.setAttr(metallic + '.fileTextureName', metallicTex, type='string')
#
#         if img.endswith('%s_e.png' % name):
#             emissiveTex = os.path.join(direcotory, img)
#             emissive = cmds.shadingNode('file', at=True, name='T_' + name + '_e')
#             cmds.setAttr(shader + '.use_emissive_map', 1)
#             cmds.connectAttr(emissive + '.outColor', shader + '.TEX_emissive_map')
#             cmds.setAttr(emissive + '.fileTextureName', emissiveTex, type='string')
#
#     # cmds.setAttr(ao + '.fileTextureName', i[0], type='string')
#     cmds.sets(meshName, e=True, fe=shading_group)
