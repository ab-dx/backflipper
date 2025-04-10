import frame_from_csv
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

f = frame_from_csv.FRAME_FROM_CSV()
data = np.array(f.get_all_frames())
window_size = 8  # Number of past steps to use

# Create sequences and targets
X, y = [], []
for i in range(len(data) - window_size):
    X.append(data[i:i+window_size])
    y.append(data[i+window_size])
X = np.array(X)  # (samples, window_size, 39)
y = np.array(y)  # (samples, 39)

# Normalize
scaler = StandardScaler()
X = scaler.fit_transform(X.reshape(-1, 39)).reshape(X.shape)
y = scaler.transform(y)

# 2. Build Model
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(256, return_sequences=False, input_shape=(window_size, 39)),
    tf.keras.layers.Dense(39)
])

model.compile(optimizer='adam', loss='mse')

# 3. Train
model.fit(X, y, epochs=200, batch_size=1, validation_split=0.0)

# 4. Predict Next Sequence
def predict_future(model, initial_sequence, steps=1):
    predictions = []
    current_seq = initial_sequence.copy()
    
    for _ in range(steps):
        pred = model.predict(current_seq[np.newaxis, ...])[0]
        predictions.append(pred)
        current_seq = np.vstack([current_seq[1:], pred])
    
    return scaler.inverse_transform(np.array(predictions))

# Usage example
initial_seq = X[0]  # Get first window from training data
predictions = predict_future(model, initial_seq, steps=400)
print("Predictions:")
predictions = predictions.flatten()
print(predictions)
print(len(predictions))
df_output = pd.DataFrame(predictions)
df_output.to_csv("./output.csv")
