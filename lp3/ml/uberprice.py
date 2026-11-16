# Practical ML-1: Uber fare prediction (Linear Regression & Random Forest)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# ---------- 1. Load and pre-process ----------
df = pd.read_csv("uber.csv")
df = df.drop(["Unnamed: 0", "key"], axis=1)          # remove unused columns
print(df.isnull().sum())                              # check missing values
df = df.dropna()                                      # drop rows with missing values

df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])   # text -> datetime
df["hour"] = df["pickup_datetime"].dt.hour
df["day"] = df["pickup_datetime"].dt.day
df["month"] = df["pickup_datetime"].dt.month
df["year"] = df["pickup_datetime"].dt.year
df["weekday"] = df["pickup_datetime"].dt.weekday
df = df.drop("pickup_datetime", axis=1)

# Haversine formula: distance (km) between pickup and dropoff points
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * np.arcsin(np.sqrt(a))           # 6371 = Earth radius in km

df["distance"] = haversine(df.pickup_latitude, df.pickup_longitude,
                           df.dropoff_latitude, df.dropoff_longitude)

# ---------- 2. Outliers ----------
df.boxplot(column=["fare_amount", "distance"])        # boxplot shows outliers
plt.show()

# remove wrong values, then use IQR rule on fare and distance
df = df[(df.fare_amount > 0) & (df.distance > 0) & (df.passenger_count > 0)]
for col in ["fare_amount", "distance"]:
    q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    iqr = q3 - q1
    df = df[(df[col] >= q1 - 1.5 * iqr) & (df[col] <= q3 + 1.5 * iqr)]

# ---------- 3. Correlation ----------
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.show()

# ---------- 4. Train/test split ----------
X = df.drop("fare_amount", axis=1)                    # features
y = df["fare_amount"]                                 # target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------- 5. Models ----------
lr = LinearRegression().fit(X_train, y_train)
rf = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)

# ---------- 6. Evaluation ----------
for name, model in [("Linear Regression", lr), ("Random Forest", rf)]:
    pred = model.predict(X_test)
    print(name)
    print("  R2   :", r2_score(y_test, pred))
    print("  RMSE :", np.sqrt(mean_squared_error(y_test, pred)))