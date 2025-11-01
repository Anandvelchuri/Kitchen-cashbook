# train_model.py
# Script to train and save a fraud detection model

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    X = np.random.rand(n_samples, 5)
    y = (X[:, 0] + X[:, 1] * 2 + np.random.rand(n_samples) > 1.5).astype(int)
    return X, y

def train_and_save_model():
    X, y = generate_synthetic_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"Model accuracy: {score:.2f}")
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Model saved as model.pkl")

if __name__ == "__main__":
    train_and_save_model()
