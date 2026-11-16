# ============================================================
# ML Practical: K-Means / Hierarchical Clustering + Elbow Method
# Output you get: data preview, elbow graph, K-Means cluster plot,
#                 dendrogram, hierarchical cluster plot
# ============================================================

# ---------- STEP 1: Import libraries ----------
import pandas as pd                          # read and handle the data
import numpy as np                           # maths on arrays
import matplotlib.pyplot as plt              # draw graphs
from sklearn.preprocessing import StandardScaler       # bring features to same scale
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage  # for dendrogram (hierarchical)

# ---------- STEP 2: Choose file + the 2 features to cluster on ----------
# >>> OPTION A: Mall_Customers (the one used in the lab manual code)
FILE = "Mall_Customers.csv"                  # if your file is .xlsx, write "Mall_Customers.xlsx"
FEATURES = ["Annual Income (k$)", "Spending Score (1-100)"]

# >>> OPTION B: sales_data_sample.csv (the one in the title)
# Comment out OPTION A above and uncomment these 2 lines:
# FILE = "sales_data_sample.csv"
# FEATURES = ["QUANTITYORDERED", "SALES"]

# ---------- STEP 3: Load the dataset ----------
if FILE.endswith(".xlsx"):
    data = pd.read_excel(FILE)               # Excel file
else:
    data = pd.read_csv(FILE, encoding="latin-1")   # latin-1 avoids decoding error in sales_data_sample.csv

print("Shape (rows, columns):", data.shape)
print(data.head())                           # first 5 rows, to confirm data loaded
print("\nMissing values:\n", data[FEATURES].isnull().sum())   # should be all 0

# ---------- STEP 4: Select features ----------
# Clustering is UNSUPERVISED -> there is no target/label column (no y).
X = data[FEATURES].dropna()                  # keep only the 2 columns (drop empty rows if any)

# Scaling: K-Means uses distance, so a big-range column would dominate the small one.
X_scaled = StandardScaler().fit_transform(X)

# ---------- STEP 5: ELBOW METHOD (find the best K) ----------
# WCSS = Within-Cluster Sum of Squares = sum of squared distance of each point to its own centroid.
# More clusters -> WCSS always goes down. We pick K where the drop suddenly slows (the "elbow").
wcss = []                                    # empty list to store WCSS for each K
for k in range(1, 11):                       # try K = 1 to 10
    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    km.fit(X_scaled)                         # run K-Means for this K
    wcss.append(km.inertia_)                 # inertia_ = WCSS of this model

plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss, marker="o", color="red", linewidth=2)
plt.title("Elbow Method")
plt.xlabel("Number of clusters (K)")
plt.ylabel("WCSS")
plt.xticks(range(1, 11))
plt.grid(True)
plt.show()                                   # look at the graph: bend point = best K

# Pick K from the elbow graph. For Mall_Customers (income vs spending) the elbow is at 5.
# If your graph bends at a different number, change this value.
K = 5

# ---------- STEP 6: Final K-Means with the chosen K ----------
kmeans = KMeans(n_clusters=K, init="k-means++", n_init=10, random_state=42)
labels = kmeans.fit_predict(X_scaled)        # cluster number (0..K-1) for every row
data.loc[X.index, "Cluster"] = labels        # add the cluster number as a new column
print("\nData with cluster labels:\n", data.head())
print("\nCustomers per cluster:\n", data["Cluster"].value_counts().sort_index())

# ---------- STEP 7: Plot K-Means clusters ----------
plt.figure(figsize=(8, 6))
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=labels, cmap="viridis", s=50)   # colour by cluster
# centroids were learned on scaled data -> convert back to original units for plotting
centroids = StandardScaler().fit(X).inverse_transform(kmeans.cluster_centers_)
plt.scatter(centroids[:, 0], centroids[:, 1], c="red", marker="X", s=250, label="Centroids")
plt.title(f"K-Means Clusters (K = {K})")
plt.xlabel(FEATURES[0])
plt.ylabel(FEATURES[1])
plt.legend()
plt.show()

# ============================================================
# HIERARCHICAL CLUSTERING (Agglomerative = bottom-up)
# Every point starts as its own cluster; closest clusters keep merging.
# ============================================================

# ---------- STEP 8: Dendrogram ----------
# Dendrogram = tree diagram of the merges.
# ward linkage = merge the pair of clusters that increases variance the least.
plt.figure(figsize=(10, 6))
dendrogram(linkage(X_scaled, method="ward"))
plt.title("Dendrogram")
plt.xlabel("Data points")
plt.ylabel("Euclidean distance")
plt.show()
# How to read it: cut the tree with a horizontal line across the LONGEST vertical lines;
# the number of lines it crosses = number of clusters.

# ---------- STEP 9: Fit Agglomerative clustering ----------
hc = AgglomerativeClustering(n_clusters=K, linkage="ward")   # same K as K-Means
hc_labels = hc.fit_predict(X_scaled)

plt.figure(figsize=(8, 6))
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=hc_labels, cmap="viridis", s=50)
plt.title(f"Hierarchical Clusters (K = {K})")
plt.xlabel(FEATURES[0])
plt.ylabel(FEATURES[1])
plt.show()