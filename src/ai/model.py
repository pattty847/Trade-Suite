import sys
import numpy as np
import torch
import torch.nn as nn
import pandas as pd
import torch.optim as optim
import plotly.graph_objs as go
import logging
import preprocessing as process
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

np.random.seed(42)
torch.manual_seed(42)

# Set up logging
logging.basicConfig(filename='model_logs.log', level=logging.DEBUG)

# Create a LSTMModel class
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size) -> None:
        super(LSTMModel, self).__init__()
        logging.info("Initializing LSTM model.")
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """
        The forward function is the main function of a neural network. It takes in an input and passes it through the layers
        of the network to produce an output. The forward function is called when you call model(input) or model.forward(input).
        The forward function should be defined as:
        
        :param self: Access variables that belong to the class
        :param x: Pass in the input data
        :return: The output of the linear layer, which is a tensor with shape (batch_size, 10)
        :doc-author: Trelent
        """
        # Initialize hidden state and cell state with zeros
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        # Forward propagate the LSTM
        out, _ = self.lstm(x, (h0, c0))

        # Get the output from the last time step
        out = out[:, -1, :]

        # Pass the output through the linear layer
        out = self.fc(out)

        return out

# Train the model
def train(model, train_loader, criterion, optimizer, device):
    """
    The train function trains the model for one epoch.
        Args:
            model (torch.nn.Module): The PyTorch module that holds the neural network
            train_loader (DataLoader): A DataLoader with labeled training samples
            criterion (torch.nn): The loss function specified for the task, e.g., nn.MSELoss() or nn.L2Loss(reduction='sum').  See https://pytorch-cn-beginner-guidebook/chapter3/3_6_lossfunciton/#id4 and https://pytorch-
    
    :param model: Pass the model to be trained
    :param train_loader: Load the training data
    :param criterion: Define the loss function
    :param optimizer: Update the weights of the model
    :param device: Tell the train function to run on the gpu if available
    :return: The average loss over all batches
    :doc-author: Trelent
    """
    model.train()
    train_loss = 0
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        y_pred = model(X_batch)
        loss = criterion(y_pred.squeeze(), y_batch)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
    return train_loss / len(train_loader)

def validate(model, val_loader, criterion, device):
    """
    The validate function takes in a model, validation loader, criterion and device.
    It sets the model to eval mode and initializes val_loss to 0. It then iterates through the validation loader
    and calculates loss using the criterion function on each batch of data. The loss is added to val_loss for each iteration.
    
    :param model: Pass the model to the function
    :param val_loader: Pass the validation data to the function
    :param criterion: Calculate the loss of the model
    :param device: Tell the model which device to use for training
    :return: The average loss over the validation set
    :doc-author: Trelent
    """
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for X_batch, y_batch in val_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            y_pred = model(X_batch)
            loss = criterion(y_pred.squeeze(), y_batch)
            val_loss += loss.item()
    return val_loss / len(val_loader)

def load_data(file):
    """
    The load_data function loads the data from a CSV file and returns it as a NumPy array.
    The function also normalizes the data using Scikit-Learn's MinMaxScaler, which is returned along with the normalized data.
    
    :param file: Specify the file to be loaded
    :return: A tuple of three numpy arrays:
    :doc-author: Trelent
    """
    original_data = pd.read_csv(file)
    data = original_data.drop(columns=['dates'])  # Drop the 'dates' column
    data.dropna(inplace=True)
    data = data.values  # Convert DataFrame to NumPy array
    # Normalize the data
    scaled_data, scaler = process.normalize(data)
    return original_data, scaled_data, scaler

def convert_to_tensors(X_train, y_train, X_val, y_val, X_test, y_test):
    """
    The convert_to_tensors function converts the numpy arrays into torch tensors.
    
    :param X_train: Store the training data
    :param y_train: Convert the labels to tensors
    :param X_val: Create a validation set
    :param y_val: Validate the model
    :param X_test: Create the test dataset
    :param y_test: Calculate the accuracy of the model
    :return: A tuple of 6 tensors
    :doc-author: Trelent
    """
    return (
        torch.tensor(X_train, dtype=torch.float32),
        torch.tensor(y_train, dtype=torch.float32),
        torch.tensor(X_val, dtype=torch.float32),
        torch.tensor(y_val, dtype=torch.float32),
        torch.tensor(X_test, dtype=torch.float32),
        torch.tensor(y_test, dtype=torch.float32),
    )

def create_data_loaders(X_train_t, y_train_t, X_val_t, y_val_t, X_test_t, y_test_t, batch_size=32):
    """
    The create_data_loaders function takes in the training, validation and test data as numpy arrays.
    It then converts them into torch tensors and creates a TensorDataset for each of the three sets.
    The function then returns a DataLoader object for each of these datasets.
    
    :param X_train_t: Create the train_dataset, which is then used to create the train_loader
    :param y_train_t: Create the train_dataset
    :param X_val_t: Create a validation dataset
    :param y_val_t: Create a tensordataset for the validation data
    :param X_test_t: Create a tensordataset object for the test data
    :param y_test_t: Create the test dataset
    :param batch_size: Specify the number of samples to be used in each batch
    :return: A tuple of 3 dataloader objects, one for each dataset
    :doc-author: Trelent
    """
    train_dataset = TensorDataset(X_train_t, y_train_t)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)

    val_dataset = TensorDataset(X_val_t, y_val_t)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    test_dataset = TensorDataset(X_test_t, y_test_t)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, test_loader

def prepare_training(model, learning_rate=0.001):
    """
    The prepare_training function takes in a model and returns the criterion, optimizer, device, and model.
    The criterion is set to mean squared error loss. The optimizer is set to Adam with a learning rate of 0.001.
    The device is either cuda or cpu depending on availability.
    
    :param model: Pass the model to the function
    :param learning_rate: Set the learning rate for the optimizer
    :return: The criterion, optimizer, device and model
    :doc-author: Trelent
    """
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    logging.info(f"Using: {device}")
    return criterion, optimizer, device, model

def train_model(model, train_loader, val_loader, criterion, optimizer, device, num_epochs, early_stopping_patience):
    """
    The train_model function trains the model on the training data and validates it on the validation data.
    It also saves a checkpoint of the best model (in terms of validation loss) to disk.
    
    
    :param model: Pass the model to train
    :param train_loader: Pass the training data to the model
    :param val_loader: Validate the model
    :param criterion: Specify the loss function
    :param optimizer: Update the weights of the model
    :param device: Specify on which device the model is trained
    :param num_epochs: Specify the number of epochs to train for
    :param early_stopping_patience: Determine when to stop training
    :return: The model with the best validation loss
    :doc-author: Trelent
    """
    best_val_loss = float("inf")
    epochs_without_improvement = 0

    for epoch in range(num_epochs):
        train_loss = train(model, train_loader, criterion, optimizer, device)
        val_loss = validate(model, val_loader, criterion, device)
        print(f"Epoch: {epoch+1}/{num_epochs}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
        
        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_without_improvement = 0
            torch.save(model.state_dict(), "best_model.pt")
        else:
            epochs_without_improvement += 1
            
        if epochs_without_improvement == early_stopping_patience:
            print("Early stopping...")
            break

def main():
    """
    The main function is the entry point of the program.
    It loads data, splits it into training and test sets, creates a model, trains it on the training set and evaluates its performance on the test set.
    
    
    :return: The value of the last expression evaluated
    :doc-author: Trelent
    """
    original_data, scaled_data, scaler = load_data("data/exchange/coinbasepro/BTC_USD_1d.csv")

    window_size = 30
    X, y = process.create_sliding_window_dataset(scaled_data, window_size)
    X_train, y_train, X_val, y_val, X_test, y_test = process.split(X, y)

    input_size = X_train.shape[2]
    hidden_size = 64
    num_layers = 2
    output_size = 1

    model = LSTMModel(input_size, hidden_size, num_layers, output_size)

    X_train_t, y_train_t, X_val_t, y_val_t, X_test_t, y_test_t = convert_to_tensors(X_train, y_train, X_val, y_val, X_test, y_test)
    train_loader, val_loader, test_loader = create_data_loaders(X_train_t, y_train_t, X_val_t, y_val_t, X_test_t, y_test_t)
    criterion, optimizer, device, model = prepare_training(model)

    # Train the model
    num_epochs = 100
    early_stopping_patience = 10

    train_model(model, train_loader, val_loader, criterion, optimizer, device, num_epochs, early_stopping_patience)

    # Load the best model
    best_model = LSTMModel(input_size, hidden_size, num_layers, output_size)
    best_model.load_state_dict(torch.load("best_model.pt"))
    best_model = best_model.to(device)

    # Evaluate the model on the test set
    test_loss = validate(best_model, test_loader, criterion, device)
    print(f"Test Loss: {test_loss:.4f}")

    # Make predictions on the test set
    y_pred_list = []
    with torch.no_grad():
        for X_batch in test_loader:
            X_batch = X_batch[0].to(device)
            y_pred = best_model(X_batch)
            y_pred_list.extend(y_pred.squeeze().cpu().numpy())

    # Calculate evaluation metrics
    mse = mean_squared_error(y_test, y_pred_list)
    mae = mean_absolute_error(y_test, y_pred_list)
    r2 = r2_score(y_test, y_pred_list)

    print(f"MSE: {mse:.4f}, MAE: {mae:.4f}, R-squared: {r2:.4f}")

    # Denormalize the test data and predicted data
    y_test_denorm = process.denormalize(y_test, scaler)
    y_pred_denorm = process.denormalize(np.array(y_pred_list), scaler)

    # Plot the original and predicted close prices
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(len(y_test_denorm)), y=y_test_denorm, name='Original Close Price'))
    fig.add_trace(go.Scatter(x=np.arange(len(y_pred_denorm)), y=y_pred_denorm, name='Predicted Close Price'))
    fig.update_layout(title='Original vs. Predicted Close Prices', xaxis_title='Time', yaxis_title='Price')
    fig.show()

if __name__ == "__main__":
    main()