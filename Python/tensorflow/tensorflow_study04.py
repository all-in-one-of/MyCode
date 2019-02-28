import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

# 定义输入和参数
x = tf.placeholder(tf.float32, shape=(None, 2))
w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))

# 定义向前传播过程
a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

# 运行
with tf.Session()as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    print("y in tf05前向传播 is:\n", sess.run(y, feed_dict={x: [[.7, .5],
                                                            [.2, .3],
                                                            [.3, .4],
                                                            [.4, .5]]}))
    print('w1:', sess.run(w1))
    print('w2:', sess.run(w2))
