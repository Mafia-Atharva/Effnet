import tensorflow as tf

@tf.keras.utils.register_keras_serializable()
class GeMPoolingLayer(tf.keras.layers.Layer):
    def __init__(self, p=3.0, epsilon=1e-6, **kwargs):
        super(GeMPoolingLayer, self).__init__(**kwargs)
        self.p = p
        self.epsilon = epsilon

    def call(self, inputs):
        return tf.reduce_mean(tf.pow(tf.abs(inputs) + self.epsilon, self.p), axis=[1, 2])

    def get_config(self):
        config = super(GeMPoolingLayer, self).get_config()
        config.update({"p": self.p, "epsilon": self.epsilon})
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)
