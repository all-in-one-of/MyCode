# coding=utf-8
"""

1.产品信息结构
2.UI结构
3.代码重构
4.接口性能优化
5.多平台，多机型（原生系统）
6.样板间
7.3d交互
8.工具链

"""

# #####################################
# 会议美术部分主要内容
##############################
# 1.模型制作报告
# 全部完成
# 对方希望以什么方式提交模型源文件
#
# 2.美术工具开发报告
# （1）商品信息录入工具。
#     ① 商品需要包含的信息补全
#     ② 录入工具的具体流程
#     ③ 商品信息的具体格式
# （2）maya工具
#     ① 打开，保存，上传，导入，（商品库）（ma,fbx,textures,max,obj,）
#     ② 商品当前制作状态
#     ③ maya内部操作的脚本

# !/usr/bin/python
# -*- coding: utf-8 -*-
# {
#     "s01": "桑扈·桌",
#     "s02": "须臾·茶桌"
# }
# 收藏级
# 优等级
# 实用级
# 一等级
import os
import shutil

from CommonTools import tools

a = {
    "a001": "参文椅",
    "a002": "参文茶几",
    "a003": "古典卷书搭脑茶几",  # 有金属
    "a004": "江檐椅",
    "a005": "桑扈·椅",
    "a006": "古典卷书搭脑边几",
    "a007": "雀悦长沙发椅",
    "a008": "雀悦短沙发椅",
    "a009": "雀悦平几",  # 有金属
    "a010": "桑扈·案",
    "a011": "雀悦茶几",  # 有金属
    "a012": "雀悦角几",  # 有金属
    "a013": "若水长沙发椅",
    "a014": "江缘短沙发椅",
    "a015": "若水短沙发椅",
    "a016": "若水平几",  # 有金属
    "a017": "若水茶几",  # 有金属
    "a018": "若水角几",
    "a019": "江缘长沙发椅",
    "a020": "明式餐椅",
    "a021": "简明式餐椅",
    "a022": "清式餐椅",
    "a023": "言炎边柜",  # 有金属
    "a024": "明式圆台（1.76米",
    "a025": "明式圆角画案",  # 有金属
    "a026": "明式书架",  # 有金属
    "a027": "桑扈柜",  # 材质球命名 #有金属
    "a028": "明式茶桌1.55",
    "a029": "虚舟茶桌",
    "a030": "虚舟茶凳",
    "a031": "知闲茶桌",
    "a032": "素官帽椅（42",
    "a033": "传统流霞南宫椅(38",  # 法线有问题
    "a034": "流霞明几南宫椅",
    "a035": "禅椅(大",
    "a036": "禅椅(小",
    "a037": "明式圆台1.48米",
    "a038": "明式圆台1.38米",
}

# 收藏级
# 优等级
# 实用级
# 一等级
b = {
    "b001": "古典卷书搭脑长沙发椅",
    "b002": "古典卷书搭脑短沙发椅",
    "b003": "古典卷书搭脑平几",  # 有金属
    # "b004": "古典卷书搭脑茶几",
    # "b005": "古典卷书搭脑角几",
    "b006": "江缘平几",
    "b007": "江檐茶几",
    "b008": "明式餐桌1.55米",
    "b009": "清式餐桌1.55米",
    "b010": "无尘书柜",  # 有金属
    "b011": "无尘画案（2.18米二抽",  # 有金属
    "b012": "无尘画案（2.38米二抽",  # 有金属
    "b013": "无尘画案（1.78米四抽",  # 有金属
    "b014": "无尘画案（1.98米四抽",  # 有金属
    "b015": "逸兴办公桌（2.18米二抽",  # 有金属
    "b016": "逸兴办公桌（2.38米二抽",  # 有金属
    "b017": "逸兴办公桌（1.78米四抽",  # 有金属
    "b018": "逸兴办公桌（1.98米四抽",  # 有金属
    "b019": "秦韵大办台(3.4米",
    "b020": "秦韵大办台(3.2米",
    "b021": "圈椅茶桌",
    "b022": "疏香茶桌",
    "b023": "疏香长茶凳",
    "b024": "疏香短茶凳",
    "b025": "言炎茶台（3米",
    "b026": "言炎茶台（3.2米",
    "b027": "言炎茶台（5.2米",
    "b028": "圈椅茶几",
    "b029": "圈椅(38",
    "b030": "圈椅(48",
    "b031": "明式茶几",
    "b032": "素官帽椅（48",
    "b033": "四出头官帽椅茶几",
    "b034": "四出头官帽椅",
    "b035": "博古架式茶边柜（右）",
    "b036": "明式三叶博古架1.86米（左）",  # 有金属
    "b037": "明式三叶博古架2米（左）",  # 有金属
    "b038": "明式双抽双门博古架",  # 有金属
    "b039": "明式翘头三联柜",  # 有金属
    "b040": "五抹圆角柜",  # 有金属
    "b041": "无尘（2.6米电视柜）",
    "b042": "无尘（2.2米电视柜）",
    "b043": "听园·柜",  # 有金属
    "b044": "无为·茶柜",  # 有金属
    "B045": "瑾瑜·条案",
    "b046": "纤月·条案",
    # "b047": "桑扈·案",
    "b048": "九格柜",  # 有金属
    "b049": "听园备餐柜",  # 有金属
    "b050": "五斗柜",  # 有金属
    "b051": "明式三叶博古架1.86米(右)",  # 有金属
    "b052": "明式三叶博古架2米（右）",  # 有金属
    "b053": "博古架式茶边柜（左）",
    "b054": "简衣架"
}
# 收藏级
# 优等级
# 实用级
# 一等级
c = {
    "c001": "江缘炕几",

    "c002": "明式四仙桌",  # 88 78
    "c003": "明式茶水架",
    "c004": "清式茶边架",
    "c005": "明式茶边架",
}

