import tensorflow as tf

print(tf.test.gpu_device_name())

def cpu():
  with tf.device('/cpu:0'):
    random_image_cpu = tf.random.normal((100, 100, 100, 3))
    net_cpu = tf.keras.layers.Conv2D(32, 7)(random_image_cpu)
    return tf.math.reduce_sum(net_cpu)

def gpu():
  with tf.device('/device:GPU:0'):
    random_image_gpu = tf.random.normal((100, 100, 100, 3))
    net_gpu = tf.keras.layers.Conv2D(32, 7)(random_image_gpu)
    return tf.math.reduce_sum(net_gpu)
  
import timeit

cpu_time = timeit.timeit('cpu()', number=10, setup="from __main__ import cpu")
print('CPU (s):', cpu_time)
gpu_time = timeit.timeit('gpu()', number=10, setup="from __main__ import gpu")
print('GPU (s):', gpu_time)
print('GPU speedup over CPU: {}x'.format(int(cpu_time/gpu_time)))

cpu_time = timeit.timeit('cpu()', number=10, setup="from __main__ import cpu")
print('CPU (s):', cpu_time)
gpu_time = timeit.timeit('gpu()', number=10, setup="from __main__ import gpu")
print('GPU (s):', gpu_time)
print('GPU speedup over CPU: {}x'.format(int(cpu_time/gpu_time)))
