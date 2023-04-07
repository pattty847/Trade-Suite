# Set up logging
import logging
import numpy as np

from sklearn.preprocessing import MinMaxScaler


logging.basicConfig(filename='model_logs.log', level=logging.DEBUG)

# Normalize the data
def normalize(data):
    """
    The normalize function takes in a numpy array of data and returns the normalized data.
        The normalize function uses the MinMaxScaler from sklearn to scale all values between -0.5 and 0.5.
    
    :param data: Pass in the data to be normalized
    :return: The normalized data and the scaler object
    :doc-author: Trelent
    """
    logging.info("Normalizing data.")
    scaler = MinMaxScaler(feature_range=(-1, 1))
    return scaler.fit_transform(data), scaler

def denormalize(data, scaler):
    """
    The denormalize function takes in a dataset that has been normalized and the scaler object that was used
    to normalize it. The function denormalizes the data using the scaler object and returns the denormalized data.
    
    :param data: Pass in the data that we want to denormalize
    :param scaler: Pass in the scaler object that was used to normalize the data
    :return: A numpy array of denormalized data
    :doc-author: Trelent
    """
    logging.info("Denormalizing data.")
    new_scaler = MinMaxScaler(feature_range=(0, 1))
    new_scaler.min_, new_scaler.scale_ = scaler.min_[3], scaler.scale_[3]
    return new_scaler.inverse_transform(data.reshape(-1, 1)).flatten()

# Create sliding window dataset
def create_sliding_window_dataset(data, window_size):
    """
    The create_sliding_window_dataset function takes in a dataset and a window size.
    It then creates sliding windows of the specified size, where each window is an array of shape (window_size, num_features).
    The function returns two arrays: X and y. X contains all the sliding windows, while y contains their corresponding targets.
    
    :param data: Pass in the dataframe that we want to use for training
    :param window_size: Determine the size of the sliding window
    :return: A tuple of two numpy arrays
    :doc-author: Trelent
    """
    logging.info("Creating sliding window dataset.")
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i - window_size:i, :])
        y.append(data[i, 3])  # Use the "close" price as target
    return np.array(X), np.array(y)

# Split the dataset into training and validation sets
def split(X, y):
    """
    The split function takes in a dataset and a window size, and returns the training, validation,
    and test sets. The function first creates the sliding window dataset using create_sliding_window_dataset.
    Then it splits the data into 60% training data (X_train), 20% validation data (X_val), and 20% testing 
    data (X_test). It also splits up y values accordingly.
    
    :param data: Pass the data to be split
    :param window_size: Determine the window size of each sliding window
    :return: The following:
    :doc-author: Trelent
    """
    logging.info("Splitting dataset.")
    train_size = int(len(X) * 0.6)
    val_size = int(len(X) * 0.2)
    X_train, y_train = X[:train_size], y[:train_size]
    X_val, y_val = X[train_size:train_size + val_size], y[train_size:train_size + val_size]
    X_test, y_test = X[train_size + val_size:], y[train_size + val_size:]
    return X_train, y_train, X_val, y_val, X_test, y_test