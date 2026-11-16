# Practical 3: Fractional Knapsack using Greedy method

n = int(input("Enter number of items: "))
W = float(input("Enter knapsack capacity: "))

items = []                                   # each item = (value, weight)
for i in range(n):
    v = float(input("Value of item " + str(i + 1) + ": "))
    w = float(input("Weight of item " + str(i + 1) + ": "))
    items.append((v, w))

# Step 1 + 2: sort by value/weight ratio, highest first (greedy choice)
items.sort(key=lambda x: x[0] / x[1], reverse=True)

total = 0.0                                  # total profit
for v, w in items:
    if w <= W:                               # whole item fits
        W -= w
        total += v
    else:                                    # take only a fraction and stop
        total += v * W / w
        break

print("Maximum value in knapsack =", total)