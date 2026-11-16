# ============================================================
# ML Practical: KNN on diabetes.csv
# Compute: Confusion Matrix, Accuracy, Error Rate, Precision, Recall
# ============================================================

# ---------- STEP 1: Import libraries ----------
import pandas as pd                      # pandas = read/handle CSV data (like Excel in Python)
import numpy as np                       # numpy = maths on arrays
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler          # for feature scaling
from sklearn.neighbors import KNeighborsClassifier        # the KNN algorithm
from sklearn.metrics import (confusion_matrix, accuracy_score,
                             precision_score, recall_score)

# ---------- STEP 2: Load the dataset ----------
df = pd.read_csv("diabetes.csv")         # keep diabetes.csv in the same folder as this file
print("Shape (rows, columns):", df.shape)   # Pima dataset -> (768, 9)
print(df.head())                         # first 5 rows, just to check data loaded properly

# ---------- STEP 3: Preprocessing ----------
# In these columns a value of 0 is impossible (BP, BMI etc. can't be 0),
# so 0 really means "missing value". We replace 0 with NaN, then fill with median.
cols_with_fake_zero = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
df[cols_with_fake_zero] = df[cols_with_fake_zero].replace(0, np.nan)
df[cols_with_fake_zero] = df[cols_with_fake_zero].fillna(df[cols_with_fake_zero].median())
# median is used (not mean) because it isn't affected by outliers

# ---------- STEP 4: Split into inputs (X) and target (y) ----------
X = df.drop(columns=["Outcome"])         # X = all features (Glucose, BMI, Age ...)
y = df["Outcome"]                        # y = target: 1 = has diabetes, 0 = no diabetes

# ---------- STEP 5: Train-test split ----------
# 80% data for training, 20% for testing.
# random_state=1 -> same split every run (reproducible)
# stratify=y     -> keeps same ratio of diabetic / non-diabetic in train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1, stratify=y)

# ---------- STEP 6: Feature scaling ----------
# KNN works on DISTANCE. Insulin (0-846) is huge vs Pregnancies (0-17),
# so Insulin would dominate. Scaling puts every feature on the same scale.
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # learn mean/std from TRAIN data and apply
X_test = scaler.transform(X_test)        # apply the same mean/std on TEST (no peeking!)

# ---------- STEP 7: Build and train KNN ----------
knn = KNeighborsClassifier(n_neighbors=5)   # k=5 -> look at 5 nearest neighbours, majority vote
knn.fit(X_train, y_train)                   # "training" = KNN just stores the training data

# ---------- STEP 8: Predict on test data ----------
y_pred = knn.predict(X_test)

# ---------- STEP 9: Evaluation ----------
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:\n", cm)
# Layout of cm:
#              Predicted 0 | Predicted 1
# Actual 0  [      TN      |     FP      ]
# Actual 1  [      FN      |     TP      ]
TN, FP, FN, TP = cm.ravel()              # unpack the 4 values
print("TN =", TN, " FP =", FP, " FN =", FN, " TP =", TP)

accuracy = accuracy_score(y_test, y_pred)     # (TP + TN) / total   -> how many predictions were right
error_rate = 1 - accuracy                     # (FP + FN) / total   -> how many were wrong
precision = precision_score(y_test, y_pred)   # TP / (TP + FP)      -> of predicted diabetic, how many truly were
recall = recall_score(y_test, y_pred)         # TP / (TP + FN)      -> of actual diabetic, how many we caught

print("Accuracy   :", round(accuracy, 4))
print("Error Rate :", round(error_rate, 4))
print("Precision  :", round(precision, 4))
print("Recall     :", round(recall, 4))

# ============================================================
# OPTIONAL (bonus, from the manual): choose best k
# Do this only if sir/examiner asks "how did you choose k?"
# ============================================================

# K-Fold Cross Validation: data split in 5 parts, each part used once as test set.
# Gives a more reliable accuracy than a single train-test split.
cv_scores = cross_val_score(KNeighborsClassifier(n_neighbors=5), X_train, y_train, cv=5)
print("\nCV scores:", cv_scores)
print("CV mean accuracy:", round(cv_scores.mean(), 4))

# GridSearchCV: tries k = 1 to 24 automatically and picks the best one
param_grid = {"n_neighbors": np.arange(1, 25)}
grid = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5)
grid.fit(X_train, y_train)
print("Best k:", grid.best_params_)
print("Best CV accuracy:", round(grid.best_score_, 4))