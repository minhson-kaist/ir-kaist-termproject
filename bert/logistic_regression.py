# Logistic regression.py

import torch
import torch.nn.functional as F
from torch.autograd import Variable

num_inputs = 2
num_outputs = 1
input_size = 784
num_classes = 2
num_epochs = 5
batch_size = 100
learning_rate = 0.001

class Model(torch.nn.Module):
	"""
		Linear regresion model
	"""
	def __init__(self):
		super(Model, self).__init__()
		self.linear = torch.nn.Linear(num_inputs, num_outputs)

	def forward(self, x):
		y_pred = F.sigmoid(self.Linear(x))

		return y_pred

# prepare data
x_data = Variable(torch.Tensor())
y_data = Variable(torch.Tensor())

# defining model
model = Model()
# binary cross entropy loss
criterion = torch.nn.BCELoss(size_average=True)
# SGD optimizer
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# training
for epoch in range(num_epochs):
	y_pred = model(x_data)

	# compute loss
	loss = criterion(y_pred, y_data)
	print("Epoch: %i, Loss: %f" %(epoch+1, round(loss.item(), 4)))

	# back-propagation
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()