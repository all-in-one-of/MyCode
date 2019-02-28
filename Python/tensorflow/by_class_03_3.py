#!/usr/bin/env python

# -*- coding:utf-8 -*-
# Author = 'HYC'
# Time   = '2019/2/28 21:14'

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow .examples.tutorials.mnist import input_data
import numpy as np

# 载入数据
mnist = input_data.read_data_sets('MNIST_data',one_hot=True)