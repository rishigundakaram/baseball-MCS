import torch
from model import NCF
from dataloader import PlaysDataset
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import numpy as np
from sklearn.preprocessing import LabelEncoder

LEARNING_RATE = .001
EPOCHS = 20
EMBED_DIM = 50
NUM_LAYERS = 3

df = pd.read_csv('plays.csv')
df = df[df.outcome != 'unknown']
pitcher_encoder = LabelEncoder().fit(df['pitcher'])
batter_encoder = LabelEncoder().fit(df['batter'])
outcome_encoder = LabelEncoder().fit(df['outcome'])

# Split the data into training and testing sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Create separate datasets and dataloaders for training and testing
train_dataset = PlaysDataset(train_df, pitcher_encoder, batter_encoder, outcome_encoder)
train_dataloader = DataLoader(train_dataset, batch_size=512, shuffle=True)

test_dataset = PlaysDataset(test_df, pitcher_encoder, batter_encoder, outcome_encoder)
test_dataloader = DataLoader(test_dataset, batch_size=512, shuffle=False)

# Initialize the model, loss, and optimizer
num_pitchers = len(train_dataset.pitcher_encoder.classes_)
num_batters = len(train_dataset.batter_encoder.classes_)
num_outcomes = len(train_dataset.outcome_encoder.classes_)

model = NCF(num_pitchers, num_batters, num_outcomes, embed_dim=EMBED_DIM, num_layers=NUM_LAYERS)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
model.to(device)

# Training loop
num_epochs = EPOCHS
for epoch in range(num_epochs):
    model.train()
    train_loss = 0.0
    for i, (pitchers, batters, outcomes) in enumerate(train_dataloader):
        optimizer.zero_grad()
        pitchers, batters, outcomes = pitchers.to(device), batters.to(device), outcomes.to(device)
        outputs = model(pitchers, batters)
        loss = criterion(outputs, outcomes)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()
    train_loss /= len(train_dataloader)
    
    # Testing
    model.eval()
    test_loss = 0.0
    with torch.no_grad():
        for pitchers, batters, outcomes in test_dataloader:
            pitchers, batters, outcomes = pitchers.to(device), batters.to(device), outcomes.to(device)
            outputs = model(pitchers, batters)
            loss = criterion(outputs, outcomes)
            test_loss += loss.item()
    test_loss /= len(test_dataloader)
    
    print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}')
        
# Save the model
torch.save(model.state_dict(), 'ncf_model.pth')

# Assuming test_loader is your DataLoader object for the test set
# and model is your trained model
def evaluate_model(test_loader, model):
    all_preds = []
    all_labels = []
    all_probabilities = []

    with torch.no_grad():
        for batch in test_loader:
            pitcher_ids, batter_ids, labels = batch
            outputs = model(pitcher_ids, batter_ids)
            _, preds = torch.max(outputs, dim=1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            
    # # Generate the confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    
    # # Plotting the confusion matrix
    # plt.figure(figsize=(10, 10))
    # sns.heatmap(cm, annot=True, fmt="d")
    # plt.title("Confusion Matrix")
    # plt.xlabel("Predicted Label")
    # plt.ylabel("True Label")
    # plt.show()
    
    # Generate classification report for precision, recall, f1-score, and accuracy
    print(classification_report(all_labels, all_preds, target_names=['strikeout', 'single', 'double', 'triple', 'homerun','walk','groundout', 'flyout','lineout','popout']))  # Replace target_names with your actual classes
    
    # Calculate class-wise accuracy
    class_wise_accuracy = np.diag(cm) / np.sum(cm, axis=1)
    print("Class-wise Accuracy:", class_wise_accuracy)

    with torch.no_grad():
        for pitcher, batter, outcome in test_loader:
            output = model(pitcher, batter)
            
            # Apply Softmax to get probabilities
            probabilities = F.softmax(output, dim=1)
            
            # Store the probabilities for later analysis
            all_probabilities.append(probabilities)
    
    all_probabilities = torch.cat(all_probabilities, dim=0)
    
    # Calculate the mean probability for each class
    mean_probabilities = all_probabilities.mean(dim=0)
    
    # You can print or plot the mean probabilities here to see if they are close to your expectation
    print(f"Mean probabilities: {mean_probabilities}")

# Assume model is your trained model and you have test_loader for the test set
model.eval()  # Set the model to evaluation mode
model.to('cpu')
evaluate_model(test_dataloader, model)
print(outcome_encoder.classes_)