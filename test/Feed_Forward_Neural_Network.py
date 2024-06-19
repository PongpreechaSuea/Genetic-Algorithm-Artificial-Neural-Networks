import numpy as np

# NN = [ 7,30,100,70,10,3 ]
NN = [ 7 ,18,18, 4 ] #ความซ้อนซับของ Neural Networks
NN_S = []   #ค่าลิมิตของข้อมูลที่แบ่งเป็นช่วงข้อมูล
W = []
valur_NN = 0 #num_weights ที่คำนวนได้จะนำมาเก็บไว้ในตัวแปลงนี้

for position_value in range(1,len(NN)):
  data = (NN[position_value],NN[position_value-1])
  valur_NN = valur_NN+ (NN[position_value]*NN[position_value-1])  #num_weights ที่คำนวนได้จะนำมาเก็บไว้ในตัวแปลงนี้
  NN_S.append(data)  #ค่าลิมิตของข้อมูลที่แบ่งเป็นช่วงข้อมูล

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
        Valur=(NN_S[i][0]*NN_S[i][1])
        Weight_NN.append(individual[Limit[i-1]:Limit[i]])
        
    for ValueInW_NN in zip(Weight_NN,NN_S):
      Return_value.append(ValueInW_NN[0].reshape(ValueInW_NN[1][0],ValueInW_NN[1][1]))
    return Return_value

def softmax(z):
    s = np.exp(z.T) / np.sum(np.exp(z.T), axis=1).reshape(-1, 1)
    return s

def sigmoid(z):
    s = 1 / (1 + np.exp(-z))
    return s

def ReLu(x):
    return max(0.0,x)

def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

def Leaky_ReLU(x):
    if x < 0 :
        return 0.01 * x
    else:
        return x 

def forward_propagation(X, individual,NN_S):
    Z = 0
    A = 0
    Weight  = get_weights_from_encoded(individual, NN_S)
    for i,calculate_model in enumerate(Weight):
      if len(calculate_model) == len(Weight[0]):
        Z = np.matmul(Weight[0], X.T)
        A = np.tanh(Z)
      elif len(calculate_model) == len(Weight[-1]):
        Z = np.matmul(Weight[i],A)
        A = softmax(Z)
        return A
      else:
        Z = np.matmul(Weight[i],A)
        A = np.tanh(Z)
