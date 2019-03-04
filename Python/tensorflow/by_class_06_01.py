#!/usr/bin/env python

# -*- coding:utf-8 -*-
# Author = 'HYC'
# Time   = '2019/3/2 23:25'

import getpass
import os
import shutil

import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib.tensorboard.plugins import projector
from tensorflow.python import VariableV1

DIR = 'C:/Users/' + getpass.getuser() + '/Documents/MyCode/Python/tensorflow/'
mnist = input_data.read_data_sets(DIR + 'MNIST_data/', one_hot=True)

# 每个批次的大小
batch_size = 100

# 计算一共有多少个批次
n_batch = mnist.train.num_examples // batch_size


# 初始化权值
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=.1)  # 生成一个截断的正太分布
    return tf.Variable(initial)


# 初始化偏置
def bias_variable(shape):
    initial = tf.constant(.1, shape=shape)
    return tf.Variable(initial)


# 卷积层
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


# 定义两个placeholder
x = tf.placeholder(tf.float32, [None, 784])  # 28*28
y = tf.placeholder(tf.float32, [None, 10])

# 改变x的格式转为4D的向量
x_image = tf.reshape(x, [-1, 28, 28, 1])

# 初始化第一个卷基层的权值和偏置

W_convl = weight_variable([5, 5, 1, 32])  # 5x5的采样窗口，32个卷积核从1个平面抽取特征
b_convl = bias_variable([32])  # 每个卷积核有一个偏置值

# 把x_image 和权值向量进行卷积，再加上偏置值，然后应用于relu激活函数
h_convl = tf.nn.relu(conv2d(x_image, W_convl) + b_convl)
h_pool1 = max_pool_2x2(h_convl)  # 进行max-pooling

# 初始化第二个卷基层的权值和偏置
W_conv2 = weight_variable([5, 5, 32, 64])  # 5x5的采样窗口，64个卷积内核从32个平面抽取特征
b_conv2 = bias_variable([64])

# 把h_pool1和权值向量进行卷积，再加上偏置值，然后应用于relu激活函数
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fcl = weight_variable([7 * 7 * 64, 1024])
b_fcl = bias_variable([1024])

h_pool2_falt = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
h_fcl = tf.nn.relu(tf.matmul(h_pool2_falt, W_fcl) + b_fcl)

keep_prob = tf.placeholder(tf.float32)
h_fcl_drop = tf.nn.dropout(h_fcl, keep_prob)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

prediction = tf.nn.softmax(tf.matmul(h_fcl_drop, W_fc2) + b_fc2)

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=prediction))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session()as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(21):
        for batch in range(n_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step, feed_dict={x: batch_xs, y: batch_ys, keep_prob: .7})
        acc = sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels, keep_prob: 1.})
        print('Iter' + str(epoch) + ', Testing Accuracy= ' + str(acc))
