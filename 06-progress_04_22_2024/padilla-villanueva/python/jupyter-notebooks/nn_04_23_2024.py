# -*- coding: utf-8 -*-
"""NN_04_23_2024.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ub34rpKIpz6ttx8lo9RCUy2b2qDDsBjp

# Import libraries
"""

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from IPython.display import Image

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam

"""#Load Data

"""

file_path = '/content/drive/MyDrive/AI-LINX/csv/comms_decisionFactor.csv'
data = pd.read_csv(file_path)

# Assume the following columns based on your previous mentions
features = data[['duration', 'power', 'voltage', 'priority_t', 'priority_e']]
target = data['execute']

"""#Split Data
Split the data into training and test sets:
"""

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

"""#Define the Neural Network"""

model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print model summary
def print_model_summary(model):
    model.summary()
    print("\nModel architecture is now printed above. Training will start next...\n")

# Save the model architecture as an image
def save_model_diagram(model, filename='model_architecture.png'):
    tf.keras.utils.plot_model(model, to_file=filename, show_shapes=True, show_layer_names=True)
    print(f"Model architecture diagram is saved as {filename}.")

"""# Train the model"""

# Enhanced training function with elegant print statements
def train_model(model, X_train, y_train, epochs, batch_size):
    optimizer = Adam(learning_rate=0.001)
    print("Starting training...\n")
    for epoch in range(epochs):
        # Shuffle the training data
        indices = np.arange(len(X_train))
        np.random.shuffle(indices)
        X_train_shuffled = X_train.iloc[indices]
        y_train_shuffled = y_train.iloc[indices]

        # Batch training
        for i in range(0, len(X_train), batch_size):
            X_batch = X_train_shuffled[i:i + batch_size].to_numpy()  # Convert DataFrame to NumPy array
            y_batch = y_train_shuffled[i:i + batch_size].to_numpy()  # Convert Series to NumPy array
            y_batch = y_batch.reshape(-1, 1)  # Reshape labels to match output shape of the model

            with tf.GradientTape() as tape:
                # Make predictions
                predictions = model(X_batch, training=True)
                # Compute losses
                loss = tf.keras.losses.binary_crossentropy(y_batch, predictions)
                # Apply reward function adjustments
                rewards = np.array([xi_j(x[1], x[2], 0, 0, 1, 0, 0, 0) for x in X_batch])  # Example placeholder
                loss *= rewards  # Modifying loss based on rewards

            # Compute gradients and update model weights
            gradients = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        # Evaluate the model's performance periodically
        val_loss, val_accuracy = model.evaluate(X_test.to_numpy(), y_test.to_numpy().reshape(-1, 1))
        print(f"Epoch {epoch + 1}/{epochs}: Val Loss = {val_loss:.4f}, Val Accuracy = {val_accuracy:.4f}")

"""# Generate predictions for the test set


"""

predictions = model.predict(X_test.to_numpy())

"""# Print the first few predictions

"""

print("Sample Predictions:")
for i in range(5):
    print(f"Input: {X_test.iloc[i].tolist()}, Predicted Execution Probability: {predictions[i][0]:.4f}")

"""# Define and implement the reward function

\begin{equation*}
    \xi _j = S_jP_je^{\left(\frac{(t_{j}^{E})-t_{j}^{R}}{\sigma}\right)^2}+(P_j^D)(d_j)({g(k))}
  \end{equation*}
"""

# Define the reward function with placeholder parameters
def xi_j(S_j, P_j, t_j_E, t_j_R, sigma, P_j_D, d_j, g_k):
    return S_j * P_j * np.exp(((t_j_E - t_j_R) / sigma) ** 2) + (P_j_D * d_j * g_k)

"""#Visualizing the Effect of the Reward **Function**

To visualize what the reward function is doing, we plot the modifications it makes to the loss during training.
todo:
- For a more straightforward visualization, we can plot how the reward values change with respect to some variables in your data.
- Our reward function depends on variables such as power and duration, and we can plot how this reward function changes as these variables vary
"""

import matplotlib.pyplot as plt

# Simulate some data for visualization
power_values = np.linspace(min(data['power']), max(data['power']), 100)
duration_values = np.linspace(min(data['duration']), max(data['duration']), 100)
reward_values = [xi_j(1, p, 0, 0, 1, 0, d, 0) for p, d in zip(power_values, duration_values)]

# Plot
plt.figure(figsize=(10, 5))
plt.plot(power_values, reward_values, label='Reward vs Power')
plt.xlabel('Power')
plt.ylabel('Reward')
plt.title('Reward Function Behavior')
plt.legend()
plt.grid(True)
plt.show()

"""# Train the model with custom loop

"""

# Use functions
print_model_summary(model)
save_model_diagram(model)
train_model(model, X_train, y_train, epochs=10, batch_size=32)

# Provide the path to your image file
image_path = '/content/model_architecture.png'

# Display the image
display(Image(filename=image_path))