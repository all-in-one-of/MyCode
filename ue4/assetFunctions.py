#!/usr/bin/env python
# coding=utf-8
# Author = 'HYC'
# Time   = '2019/4/2 23:37'
import unreal


def buildImportTask(fileName,destination_path):
    task = unreal.AssetImportTask()
    # 避免对话框
    task.set_editor_property('automated',True)

    # 导入之后的路径
    task.set_editor_property('destination_path',destination_path)

    # 导入的文件
    task.set_editor_property('filename',fileName)

    # 覆盖
    task.set_editor_property('replace_existing',True)
    # 保存
    task.set_editor_property('save',True)

    return task

def executeImportTask(tasks):
    '''
    执行导入
    :param tasks: list
    :return:
    '''
    if isinstance(tasks,list) is False:
        return
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)