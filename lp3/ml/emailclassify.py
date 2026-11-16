# Practical ML-2: Email spam detection using KNN and SVM
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix, classification_report

# ---------- 1. Load and pre-process ----------
df = pd.read_csv("emails.csv")
print(df.shape)
print(df.isnull().sum().sum())                       # total missing values
df = df.drop("Email No.", axis=1)                    # email name is not a feature

X = df.drop("Prediction", axis=1)                    # word counts (features)
y = df["Prediction"]                                 # 1 = spam, 0 = not spam
print(y.value_counts())                              # how many spam / not spam

# ---------- 2. Split and scale ----------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
sc = StandardScaler()                                # KNN uses distance, so scale features
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# ---------- 3. Models ----------
knn = KNeighborsClassifier(n_neighbors=5).fit(X_train, y_train)
svm = SVC(kernel="linear").fit(X_train, y_train)

# ---------- 4. Evaluation ----------
for name, model in [("KNN", knn), ("SVM", svm)]:
    pred = model.predict(X_test)
    print("=====", name, "=====")
    print("Accuracy :", accuracy_score(y_test, pred))
    print("Precision:", precision_score(y_test, pred))
    print("Recall   :", recall_score(y_test, pred))
    print("F1 score :", f1_score(y_test, pred))
    print(confusion_matrix(y_test, pred))
    sns.heatmap(confusion_matrix(y_test, pred), annot=True, fmt="d", cmap="Blues")
    plt.title(name + " confusion matrix")
    plt.show()