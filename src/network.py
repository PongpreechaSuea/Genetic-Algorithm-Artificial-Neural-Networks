# Feed_Forward_Neural_Network

import numpy as np
from src.config import NN, NN_S, valur_NN, W

for position_value in range(1,len(NN)):
  data = (NN[position_value],NN[position_value-1])
  valur_NN = valur_NN+ (NN[position_value]*NN[position_value-1])
  NN_S.append(data)

# for i in range(1, len(NN)):
#     NN_S.append((NN[i], NN[i-1]))
#     valur_NN += NN[i] * NN[i-1]

def Limit_Neural_Network(NN_S):   #แบ่งข้อมูลที่ได้มาทำเป็นลิมิตหาช่วงข้อมูล เพื่อนำมาใช้ในการคำนวณในส่วนของ weights
  Data_Limit_Neural_Network = []
  for i , data in enumerate(NN_S):
    if data == NN_S[0]: 
      Data_Limit_Neural_Network.append(data[0]*data[1])
    elif data == NN_S[-1]:
      Data_Limit_Neural_Network.append(data[0]*data[1]+Data_Limit_Neural_Network[i-1])
    else:
      Valur = (NN_S[i][0]*NN_S[i][1])
      Data_Limit_Neural_Network.append(Valur+Data_Limit_Neural_Network[i-1])

  return Data_Limit_Neural_Network

def get_weights_from_encoded(individual,NN_S):
    Return_value = []
    Weight_NN = []
    Limit = Limit_Neural_Network(NN_S)
    for i , data in enumerate(NN_S):
      if data == NN_S[0]: 
        Weight_NN.append(individual[:Limit[i]])
      elif data == NN_S[-1]:
        Weight_NN.append(individual[Limit[-2]:])        
      else:
        Valur = (NN_S[i][0]*NN_S[i][1])
        Weight_NN.append(individual[Limit[i-1]:Limit[i]])
        
    for ValueInW_NN in zip(Weight_NN,NN_S):
      Return_value.append(ValueInW_NN[0].reshape(ValueInW_NN[1][0],ValueInW_NN[1][1]))
    return Return_value

def calculate_limits(NN_S):
    """คำนวณลิมิตของข้อมูลที่แบ่งเป็นช่วงข้อมูล."""
    limits = []
    cumulative_sum = 0
    for i, (n_out, n_in) in enumerate(NN_S):
        cumulative_sum += n_out * n_in
        limits.append(cumulative_sum)
    return limits

def extract_weights(individual, NN_S):
    """Extract weights from encoded individual."""
    limits = calculate_limits(NN_S)
    weights = []
    start = 0
    for limit in limits:
        weights.append(individual[start:limit])
        start = limit

    # Debugging: print the size and shape of each weight array
    for i, (w, (n_out, n_in)) in enumerate(zip(weights, NN_S)):
        print(f"Weight {i}: size {w.size}, expected shape ({n_out}, {n_in})")
        if w.size != n_out * n_in:
            print(f"Error: Weight size {w.size} does not match expected size {n_out * n_in}")
            # Optionally, you could raise an error or handle the mismatch
            raise ValueError(f"Weight size mismatch for weight {i}")

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


