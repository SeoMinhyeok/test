# -*- coding: utf-8 -*-

"""
CODE 설명

Pytorch 에서 custom 으로 생성한 데이터와 모델을 이용해서 실험을 돌림,
DataLoader 에서 batch_size 만큼 Data 가 제공된다.
"""
from torch.utils.data.dataset import Dataset
import torch
from fc_model import NkModel
from my_dataset import NkDataSet

#Data_Load
csv_path = "./file/Hangul.csv"

custom_dataset = NkDataSet(csv_path)

my_dataset_loader = torch.utils.data.DataLoader(dataset=custom_dataset, batch_size=5,
                                                shuffle=False, num_workers=1)
#Model_Load
#input, hidden, output_size
D_in = 30000 #(100 * 100 * 3)
H = 1000
D_out = 5

model = NkModel(D_in, H, D_out)

#CrossEntropyLoss 를 사용
criterion = torch.nn.CrossEntropyLoss(reduction="sum")
optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)

for t in range(500):
    for i, data in enumerate(my_dataset_loader, 0):

        # Forward pass: Compute predicted y by passing x to the model

        #fc 구조 이기 때문에 일렬로 쫙피는 작업이 필요하다.

        images, label = data

        #그냥 images 를 하면 에러가 난다. 데이터 shape 이 일치하지 않아서
        images = images.view(5,30000)
        print(images.size())
        y_pred = model(images)

        print(label)
        #Compute and print loss
        loss = criterion(y_pred, label)

        print(t, loss.item())

        # Zero gradients, perform a backward pass, and update the weights.
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()