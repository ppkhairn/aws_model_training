import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
import os

# SageMaker automatically sets these paths
TRAIN_DIR = os.environ.get('SM_CHANNEL_TRAINING', '/opt/ml/input/data/training')
MODEL_DIR = os.environ.get('SM_MODEL_DIR', '/opt/ml/model')

def train():
    # 1. Setup Data
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
    dataset = datasets.ImageFolder(TRAIN_DIR, transform=transform)
    loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

    # 2. Setup Model (Transfer Learning)
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, 2) # Cat vs Dog
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 3. Training Loop
    model.train()
    for epoch in range(1): # Keep epochs low for testing
        for images, labels in loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    
    # 4. Save Model
    torch.save(model.state_dict(), os.path.join(MODEL_DIR, "model.pth"))

if __name__ == "__main__":
    train()