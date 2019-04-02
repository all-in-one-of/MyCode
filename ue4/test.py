import os
from unreal_engine.classes import PyFbxFactory, MaterialFactoryNew, TextureFactory
import json


# instantiate a new factory


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


def fbxImport(fbx, scale=1):
    fbx_factory = PyFbxFactory()
    # build the path for the fbx file

    # configure the factory
    fbx_factory.ImportUI.bCreatePhysicsAsset = False
    fbx_factory.ImportUI.bImportMaterials = False
    fbx_factory.ImportUI.bImportTextures = False
    fbx_factory.ImportUI.bImportAnimations = False
    # scale the mesh (the Kaiju is 30 meters high !)
    fbx_factory.ImportUI.SkeletalMeshImportData.ImportUniformScale = scale

    # import the mesh
    slicer_mesh = fbx_factory.factory_import_object(
        fbx, '/Game/Kaiju/Slicer')


def createMaterial():
    material_factory = MaterialFactoryNew()

    material_blades = material_factory.factory_create_new('/Game/Kaiju/Slicer/Blades_Material')

    material_body = material_factory.factory_create_new('/Game/Kaiju/Slicer/Body_Material')


def textureImport():
    # instantiate a factory for importing textures
    texture_factory = TextureFactory()
    # ensures textures are overwritten (2 means, YesAll, defined in Engine/Source/Runtime/Core/Public/GenericPlatform/GenericPlatformMisc.h, EAppReturnType::YesAll)
    texture_factory.OverwriteYesOrNoToAllState = 2

    slicer_blade_texture_base_color_tga = os.path.join(kaiju_assets_dir, 'Textures/slicer_blade_BaseColor.tga')
    slicer_blade_texture_base_color = texture_factory.factory_import_object(slicer_blade_texture_base_color_tga,
                                                                            '/Game/Kaiju/Slicer/Textures')

    slicer_blade_texture_normal_tga = os.path.join(kaiju_assets_dir, 'Textures/slicer_blade_Normal.tga')
    slicer_blade_texture_normal = texture_factory.factory_import_object(slicer_blade_texture_normal_tga,
                                                                        '/Game/Kaiju/Slicer/Textures')

    slicer_blade_texture_emissive_tga = os.path.join(kaiju_assets_dir, 'Textures/slicer_blade_Emissive.tga')
    slicer_blade_texture_emissive = texture_factory.factory_import_object(slicer_blade_texture_emissive_tga,
                                                                          '/Game/Kaiju/Slicer/Textures')

    # orm stands for OcclusionRoughnessMetallic
    slicer_blade_texture_orm_tga = os.path.join(kaiju_assets_dir,
                                                'Textures/slicer_blade_OcclusionRoughnessMetallic.tga')
    slicer_blade_texture_orm = texture_factory.factory_import_object(slicer_blade_texture_orm_tga,
                                                                     '/Game/Kaiju/Slicer/Textures')

    slicer_texture_base_color_tga = os.path.join(kaiju_assets_dir, 'Textures/slicer_BaseColor.tga')
    slicer_texture_base_color = texture_factory.factory_import_object(slicer_texture_base_color_tga,
                                                                      '/Game/Kaiju/Slicer/Textures')

    slicer_texture_normal_tga = os.path.join(kaiju_assets_dir, 'Textures/slicer_Normal.tga')
    slicer_texture_normal = texture_factory.factory_import_object(slicer_texture_normal_tga,
                                                                  '/Game/Kaiju/Slicer/Textures')

    slicer_texture_emissive_tga = os.path.join(kaiju_assets_dir, 'Textures/slicer_Emissive.tga')
    slicer_texture_emissive = texture_factory.factory_import_object(slicer_texture_emissive_tga,
                                                                    '/Game/Kaiju/Slicer/Textures')

    # orm stands for OcclusionRoughnessMetallic
    slicer_texture_orm_tga = os.path.join(kaiju_assets_dir, 'Textures/slicer_OcclusionRoughnessMetallic.tga')
    slicer_texture_orm = texture_factory.factory_import_object(slicer_texture_orm_tga, '/Game/Kaiju/Slicer/Textures')


kaiju_assets_dir = os.path.join(os.path.expanduser('~/Desktop'), 'Kaiju_Assets/Slicer')

slicer_fbx = os.path.join(kaiju_assets_dir, 'slicer.fbx')
# fbxImport(slicer_fbx, 0.1)
createMaterial()
textureImport()