# Feed_Forward_Neural_Network

import numpy as np
from src.config import NN, NN_S, valur_NN

for i in range(1, len(NN)):
    NN_S.append((NN[i], NN[i-1]))
    valur_NN += NN[i] * NN[i-1]

def calculate_limits(NN_S):
    """คำนวณลิมิตของข้อมูลที่แบ่งเป็นช่วงข้อมูล."""
    limits = []
    cumulative_sum = 0
    for i, (n_out, n_in) in enumerate(NN_S):
        cumulative_sum += n_out * n_in
        limits.append(cumulative_sum)
    return limits

def extract_weights(individual, NN_S):
    """ดึงค่า weights จาก encoded individual."""
    limits = calculate_limits(NN_S)
    weights = []
    start = 0
    for limit in limits:
        weights.append(individual[start:limit])
        start = limit
    reshaped_weights = [w.reshape(n_out, n_in) for w, (n_out, n_in) in zip(weights, NN_S)]
    return reshaped_weights

def softmax(z):
    exp_z = np.exp(z.T)
    return exp_z / np.sum(exp_z, axis=1).reshape(-1, 1)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def relu(x):
    return np.maximum(0, x)

def tanh(x):
    return np.tanh(x)

def leaky_relu(x):
    return np.where(x > 0, x, x * 0.01)

def forward_propagation(X, individual, NN_S):
    """กระบวนการ forward propagation สำหรับ neural network."""
    weights = extract_weights(individual, NN_S)
    A = X.T
    for i, W in enumerate(weights):
        Z = np.matmul(W, A)
        if i == len(weights) - 1:
            A = softmax(Z)
        else:
            A = tanh(Z)
    return A

