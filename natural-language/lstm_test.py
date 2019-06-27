import numpy as np
from keras.models import Model
from keras.layers import Input
from keras.layers import LSTM

inputs = Input(shape=(3, 1))
lstm = LSTM(units=1, return_sequences=True, return_state=True)
lstm, state_h, state_c = lstm(inputs)
model = Model(inputs=inputs, outputs=[lstm, state_h, state_c])

# return_state=True
#  |-> state_h is the hidden state output for the last time step
#  |-> state_c is the cell state for the last time step
# return_sequences=True
#  |-> lstm is the sequence of hidden state outputs for each input time step*

data = np.array([0.1, 0.2, 0.3]).reshape((1,3,1))
prediction = model.predict(data) # * -> prediction[0][:, -1] == prediction[1]
print(model.predict(data))