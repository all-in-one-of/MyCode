import os
from unreal_engine.classes import PyFbxFactory
import json
# instantiate a new factory
fbx_factory = PyFbxFactory()


def fbx_import(slicer_fbx):
    # build the path for the fbx file
    # kaiju_assets_dir = os.path.join(os.path.expanduser('~/Desktop'), 'Kaiju_Assets/Slicer')
    #
    # slicer_fbx = os.path.join(kaiju_assets_dir, 'slicer.fbx')

    # configure the factory
    fbx_factory.ImportUI.bCreatePhysicsAsset = False
    fbx_factory.ImportUI.bImportMaterials = True
    fbx_factory.ImportUI.bImportTextures = True
    fbx_factory.ImportUI.bImportAnimations = False
    # scale the mesh (the Kaiju is 30 meters high !)
    # fbx_factory.ImportUI.SkeletalMeshImportData.ImportUniformScale = 0.1

    # import the mesh
    slicer_mesh = fbx_factory.factory_import_object(
        slicer_fbx, '/Game/Kaiju/Slicer')


def findSpecifiedFile(path, suffix=''):
    '''
    查找指定文件
    :param path: 根目录
    :param suffix: 格式，默认是空
    :return: 文件地址列表
    '''
    _file = []
    for root, dirs, fils in os.walk(path):
        for file in fils:
            if file.endswith(suffix):
                _file.append(os.path.join(root, file))
    return _file


# for i in findSpecifiedFile(r'D:\test','.fbx'):
#     fbx_import(i)
fbx = r"F:\Share\simplygon\inputDir\00000000.fbx"
fbx_import(fbx)
aaa