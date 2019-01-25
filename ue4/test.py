import os.path
from unreal_engine.classes import PyFbxFactory

# instantiate a new factory
fbx_factory = PyFbxFactory()

# build the path for the fbx file
kaiju_assets_dir = os.path.join(os.path.expanduser('~/Desktop'), 'Kaiju_Assets/Slicer')

slicer_fbx = os.path.join(kaiju_assets_dir, 'slicer.fbx')

# configure the factory
fbx_factory.ImportUI.bCreatePhysicsAsset = False
fbx_factory.ImportUI.bImportMaterials = False
fbx_factory.ImportUI.bImportTextures = False
fbx_factory.ImportUI.bImportAnimations = False
# scale the mesh (the Kaiju is 30 meters high !)
fbx_factory.ImportUI.SkeletalMeshImportData.ImportUniformScale = 0.1

# import the mesh
slicer_mesh = fbx_factory.factory_import_object(slicer_fbx, '/Game/Kaiju/Slicer')