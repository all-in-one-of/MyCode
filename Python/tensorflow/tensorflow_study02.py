import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf


a = tf.constant([[1.],[2.]])  # 定义张量a，为常数constant,1.0,2.0
b = tf.constant([[3., 4.]])  
x = tf.constant([[1.,2.]])
y = tf.constant([[3.],[4.]])
# a = x+y # 搭建网路，不参与运算
c = tf.matmul(a,b)
# Tensor("add:0", shape=(2,), dtype=float32) add:0 节点名称、第0个输出，shape=（2，）维度、一维数组，dtype=float32 数据类型
# shape=(2,) 第一个维度里有两个元素

# w = tf.Variable(tf.random_normal([2,3], stddev=2, mean=0, seed=1))

# tf.random_normal() 正态分布
# tf.truncated_normal() 去掉过大偏离点的正态分布
# tf.random_uniform() 平均分布




with tf.Session()as sess:
    # print(sess.run(a))
    print(sess.run(c))
