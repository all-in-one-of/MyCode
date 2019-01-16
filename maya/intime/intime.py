# coding=utf-8
import datetime
import json
import pprint
import shutil

import ast
from maya import cmds
import logging
import os
from PySide2 import QtWidgets, QtCore, QtGui
from CommonTools import tools

JSONFILESPATH = r"D:\jsons"
PROJECTPATH = r'D:\testProject'
MAYAPROJECT = cmds.workspace(fn=True)


class IntmeCommodity(dict):
    def createPBS(self, name, direcotory, ismetallic=None, isemissive=None, isroughness=None):
        imges = os.listdir(direcotory)
        for img in imges:
            if img.endswith('%s_b.png' % name):
                baseTex = os.path.join(direcotory, img)
            if img.endswith('%s_n.png' % name):
                noramlTex = os.path.join(direcotory, img)
            if img.endswith('%s_ao.png' % name):
                aoTex = os.path.join(direcotory, img)
            if img.endswith('%s_r.png' % name):
                roughnessTex = os.path.join(direcotory, img)
            if img.endswith('%s_m.png' % name):
                metallicTex = os.path.join(direcotory, img)
            if img.endswith('%s_e.png' % name):
                emissiveTex = os.path.join(direcotory, img)

        shaderName = 'M_' + name + '_w'
        shader = cmds.shadingNode('StingrayPBS', asShader=True, name=shaderName)
        cmds.shaderfx(sfxnode=shader, initShaderAttributes=True)

        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shaderName + 'SG')
        cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader')

        baseColor = cmds.shadingNode('file', at=True, name='T_' + name + '_b')
        cmds.setAttr(shader + '.use_color_map', 1)
        cmds.connectAttr(baseColor + '.outColor', shader + '.TEX_color_map')

        normal = cmds.shadingNode('file', at=True, name='T_' + name + '_n')
        cmds.setAttr(shader + '.use_normal_map', 1)
        cmds.connectAttr(normal + '.outColor', shader + '.TEX_normal_map')

        ambientOcclusion = cmds.shadingNode('file', at=True, name='T_' + name + '_ao')
        cmds.setAttr(shader + '.use_ao_map', 1)
        cmds.connectAttr(ambientOcclusion + '.outColor', shader + '.TEX_ao_map')

        if isroughness:
            roughness = cmds.shadingNode('file', at=True, name='T_' + name + '_r')
            cmds.setAttr(shader + '.use_roughness_map', 1)
            cmds.connectAttr(roughness + '.outColor', shader + '.TEX_roughness_map')

        if ismetallic:
            metallic = cmds.shadingNode('file', at=True, name='T_' + name + '_m')
            cmds.setAttr(shader + '.use_metallic_map', 1)
            cmds.connectAttr(metallic + '.outColor', shader + '.TEX_metallic_map')

        if isemissive:
            emissive = cmds.shadingNode('file', at=True, name='T_' + name + '_e')
            cmds.setAttr(shader + '.use_emissive_map', 1)
            cmds.connectAttr(emissive + '.outColor', shader + '.TEX_emissive_map')

        # cmds.setAttr(ao + '.fileTextureName', i[0], type='string')

    def findCommodity(self, directory=JSONFILESPATH):
        """
        找到文件夹下所有json，存入字典
        :param directory: json文件夹地址
        :return:
        """
        self.clear()
        files = os.listdir(directory)
        for file in files:
            name, ext = os.path.splitext(file)
            commodityInfo = os.path.join(directory, file)
            with open(commodityInfo, 'r') as f:
                info = json.load(f)

            self[name] = eval(json.dumps(info, encoding="utf-8", ensure_ascii=False))

    def loadMayaFile(self, name, versions):
        """
        从服务器上打开maya文件
        :param name: 文件名
        :param versions: 版本
        :return:
        """
        a = self[name][versions]['maya文件地址']['path']
        shutil.copy(a, os.path.join(MAYAPROJECT, 'scenes'))

        cmds.file(os.path.join(MAYAPROJECT, 'scenes/%s.ma' % name), o=True, force=True)

    def saveMayaFile(self, name):
        """
        保存本地maya
        :param name: 文件名
        :return:
        """
        maName = os.path.join(MAYAPROJECT, 'scenes//%s.ma' % name)
        cmds.file(rename=maName)
        cmds.file(save=True, type='mayaAscii', force=True)
        return maName

    def openMayaFile(self, name):
        '''
        打开maya文件
        :param name: 文件名
        :return:
        '''
        maName = os.path.join(cmds.workspace(fn=True), 'scenes//%s.ma' % name)
        cmds.file(maName, o=True, force=True)

    def updateMayaFile(self, name, directory=PROJECTPATH, note=''):
        """
        上传maya文件
        :param name: 名字
        :param directory: 项目地址
        :param note: 摘要
        :return:
        """
        date = datetime.date.today()
        nameDirectory = os.path.join(directory, name)
        tools.createDirectory(nameDirectory)
        dateDirectory = os.path.join(nameDirectory, '%s' % date)
        tools.createDirectory(dateDirectory)
        mayaDirectory = os.path.join(dateDirectory, 'maya')

        tools.createDirectory(mayaDirectory)
        shutil.copy(self.saveMayaFile(name), mayaDirectory)
        self[name]['%s' % date]['note'] = note
        self[name]['%s' % date]['maya文件地址'] = os.path.join(dateDirectory, '%s.ma' % name)
        with open(os.path.join(JSONFILESPATH, '%s.json' % name), 'w') as f:
            json.dump(self[name], f, ensure_ascii=False)


def run():
    name = []
    a = IntmeCommodity()
    a.findCommodity()
    for n, info in a.items():
        name.append(n)

    a.createPBS(name[0])
    # a.loadMayaFile(name=name[0], versions='2019-01-12')
