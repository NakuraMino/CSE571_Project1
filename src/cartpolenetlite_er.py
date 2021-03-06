# -*- coding: utf-8 -*-
"""CartpoleNetLite_er.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E6ZY2qJeFhed0sUPYvToYDlSAWnljjhf
"""

# !unzip dataset.zip

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class CartpoleNetLite_er(nn.Module):

  def __init__(self):
    super(CartpoleNetLite_er, self).__init__()
    # 6 output channels, 3x3 square convolution
    self.conv1 = nn.Conv3d(1, 6, 3, padding=1)
    self.conv2 = nn.Conv3d(6, 10, 3, padding=1)
    self.conv3 = nn.Conv3d(10, 20, 3, padding=1)
    self.fc1 = nn.Linear(5120, 200)
    self.fc2 = nn.Linear(200, 100)
    self.fc3 = nn.Linear(100, 4)
    self.JHist = []

  def forward(self, x):
    # Max pooling over a (1, 2, 2) window
    x = F.max_pool3d(F.relu(self.conv1(x)), (1, 2, 2))
    x = F.max_pool3d(F.relu(self.conv2(x)), (1, 2, 2))
    x = F.max_pool3d(F.relu(self.conv3(x)), (1, 2, 2))
    # print(x.shape)
    x = torch.sum(x, axis=2)
    x = x.view(-1, self.num_flat_features(x))
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = self.fc3(x)
    return x

  def num_flat_features(self, x):
    size = x.size()[1:]  # all dimensions except the batch dimension
    num_features = 1
    for s in size:
      num_features *= s
    return num_features

# images_per_set = 5
# num_samples = 10
# num_channels = 1

# net = CartpoleNetLite_er()
# print(net)
# input = torch.randn(num_samples, num_channels, images_per_set, 128, 128)
# out = net(input)
# print(out)

def create_batch(dataset, batch_size=32, epoch=0, index=0):
  '''
  retrieves a batch of training data to work on. given the specified
  starting epoch and starting index. 
  '''
  index %= 50
  assert(epoch < 220 and epoch >= 0)
  assert(index >= 3 and index <= 48)

  train_x = dataset[epoch * 50 + index][0].unsqueeze(0) # gets first training point 
  train_y = torch.tensor(dataset[epoch * 50 + index][1][-2, :]).unsqueeze(0) # gets second to last delta state 

  # epoch * 50 + index


  for i in range(batch_size - 1):
    index += 1
    if (index > 48):
      # resetting indices so we are in the right area
      epoch += 1
      index = 3 
    if epoch >= 218:
      epoch = 0
    x = dataset[epoch * 50 + index][0].unsqueeze(0)
    y = torch.tensor(dataset[epoch * 50 + index][1][-2, :]).unsqueeze(0)
    train_x = torch.cat((train_x, x), axis=0)
    train_y = torch.cat((train_y, y), axis=0)

  return (train_x.double(), train_y, epoch, index)

if __name__ == '__main__':
  from dataloader import CartpoleDataset
  import numpy as np
  torch.autograd.set_detect_anomaly(True)

  NUM_ITRS = 10  # Number of times to go over the full dataset
  NUM_EPOCHS = 220
  LEARNING_RATE = 0.01
  BATCH_SIZE = 100
  E = 50  # epoch length
  n = 5  # images per set
  W = 128  # image width
  H = 128  # image height
  grayscale = True

  if not grayscale:
    num_channels = 3
  else:
    num_channels = 1

  net = CartpoleNetLite_er().float().to("cuda")
  # net = CartpoleNetLite_er().float()
  criterion = nn.MSELoss()
  optimizer = optim.Adam(net.parameters(), lr=LEARNING_RATE)
  dataset = CartpoleDataset('data.csv', './image_dataset/', n, grayscale=grayscale)

  epoch = 0; index = 3
  for i in range(4500 ):
    train_x, train_y, epoch, index = create_batch(dataset, BATCH_SIZE, epoch, index)
    train_x = train_x.float().to("cuda")
    train_y = train_y.float().to("cuda")

    optimizer.zero_grad()
    y_pred = net(train_x)
    loss = criterion(y_pred, train_y)
    loss.backward()
    optimizer.step()

    epoch_loss = loss.item()
    net.JHist.append(epoch_loss)
    print(i, epoch_loss)

# import matplotlib.pyplot as plt
# 
# plt.plot(net.JHist[230:])
# # print(net.JHist)
# plt.ylabel("Mean Squared error")
# plt.xlabel("epoch")
# plt.grid()
# plt.show()
# 
# JHist_avg = []
# ii = 0
# sum = 0
# for J in net.JHist:
  # if ii % 100 == 99:
    # JHist_avg.append(sum / 100)
    # sum = 0
  # else:
    # sum += J
  # ii += 1
# 
# plt.clf()
# plt.xlabel("epoch")
# plt.ylabel("mean-squared error")
# plt.title("average MSE per 100 iterations")
# plt.plot(JHist_avg[2:])
# plt.show()
# 
# PATH = './models/CartpoleNetLite-er.pth'
# torch.save(net.state_dict(), PATH)

