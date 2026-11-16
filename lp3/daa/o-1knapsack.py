# Practical 4: 0/1 Knapsack using Dynamic Programming

n = int(input("Enter number of items: "))
W = int(input("Enter knapsack capacity: "))
val, wt = [], []
for i in range(n):
    val.append(int(input("Value of item " + str(i + 1) + ": ")))
    wt.append(int(input("Weight of item " + str(i + 1) + ": ")))

# Table T: (n+1) rows x (W+1) columns, row 0 and column 0 are all 0
T = [[0] * (W + 1) for _ in range(n + 1)]

# Fill table: T[i][j] = best value using first i items with capacity j
for i in range(1, n + 1):
    for j in range(1, W + 1):
        if wt[i - 1] <= j:                       # item i fits: take it or leave it
            T[i][j] = max(T[i - 1][j], val[i - 1] + T[i - 1][j - wt[i - 1]])
        else:                                    # item i too heavy: leave it
            T[i][j] = T[i - 1][j]

print("Maximum value =", T[n][W])               # last box = answer

# Trace back to find which items were picked
j, chosen = W, []
for i in range(n, 0, -1):
    if T[i][j] != T[i - 1][j]:                  # value changed -> item i taken
        chosen.append(i)
        j -= wt[i - 1]
print("Items selected:", chosen[::-1])