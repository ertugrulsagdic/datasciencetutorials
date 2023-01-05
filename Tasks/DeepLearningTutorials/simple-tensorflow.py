# Example of TensorFlow library
import tensorflow as tf
tf.compat.v1.disable_eager_execution()

# declare two symbolic floating-point scalars
a = tf.compat.v1.placeholder(tf.float32)
b = tf.compat.v1.placeholder(tf.float32)
# create a simple symbolic expression using the add function add = tf.add(a, b)
add = tf.add(a, b)
#bind1.5to a,2.5to b,andevaluate c
sess = tf.compat.v1.Session()
binding = {a: 1.5, b: 2.5}
c = sess.run(add, feed_dict=binding)
print(c)