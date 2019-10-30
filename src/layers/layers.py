import numpy as np

from src.layers.module import Module


class LinearLayer(Module):
    def __init__(self, in_shape, out_shape):
        super().__init__()
        self.weights = np.random.normal(scale=1, size=[in_shape, out_shape])
        self.bias = np.random.normal(scale=1, size=out_shape)

        self.prev_activation = None
        self.z = None

        self.dW = None
        self.db = None
        self.da_prev = None

    def forward(self, x):
        self.prev_activation = x
        self.z = np.dot(self.prev_activation, self.weights) + self.bias
        return self.z

    def backward(self, upstream_gradient):
        self.dW = np.dot(upstream_gradient.T, self.prev_activation).T
        self.db = np.sum(upstream_gradient, axis=0, keepdims=True)

        self.da_prev = np.dot(upstream_gradient, self.weights.T)

        # auto update
        self.weights = self.weights - 1 * self.dW
        self.bias = self.bias - 1 * self.db
        return self.da_prev

    def _init_weights(self, method):
        pass


class FullyConnected(Module):
    def __init__(self, in_shape, out_shape, activation):
        super().__init__()
        self.linear = LinearLayer(in_shape, out_shape)
        self.activation = activation

    def forward(self, x):
        z = self.linear.forward(x)
        a = self.activation.forward(z)
        return a

    def backward(self, upstream_gradients):
        dZ = self.activation.backward(upstream_gradients)
        dA = self.linear.backward(dZ)
        return dA
