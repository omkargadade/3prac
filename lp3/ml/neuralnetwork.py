# Practical ML-3: Bank customer churn prediction using Neural Network (Keras)
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
from tensorflow import keras
from tensorflow.keras import layers

# ---------- 1. Read dataset ----------
df = pd.read_csv("Churn_Modelling.csv")
df = df.drop(["RowNumber", "CustomerId", "Surname"], axis=1)   # useless columns

# text columns -> numbers (one-hot encoding)
df = pd.get_dummies(df, columns=["Geography", "Gender"], drop_first=True)

# ---------- 2. Features / target and split ----------
X = df.drop("Exited", axis=1).astype("float32")        # Exited: 1 = left, 0 = stayed
y = df["Exited"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------- 3. Normalize ----------
sc = StandardScaler()
X_train = sc.fit_transform(X_train)                    # learn mean/std from train only
X_test = sc.transform(X_test)

# ---------- 4. Build model ----------
model = keras.Sequential([
    keras.Input(shape=(X_train.shape[1],)),
    layers.Dense(16, activation="relu"),               # hidden layer 1
    layers.Dense(8, activation="relu"),                # hidden layer 2
    layers.Dropout(0.1),                               # improvement: reduces overfitting
    layers.Dense(1, activation="sigmoid"),             # output: probability of leaving
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1)

# ---------- 5. Accuracy and confusion matrix ----------
y_pred = (model.predict(X_test) > 0.5).astype(int)     # probability > 0.5 -> leaves
print("Accuracy:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))