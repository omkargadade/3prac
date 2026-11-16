# Practical ML-4: Gradient Descent to find local minimum of y = (x+3)^2
import matplotlib.pyplot as plt
import numpy as np

def f(x):                       # function to minimise
    return (x + 3) ** 2

def gradient(x):                # derivative: dy/dx = 2(x+3)
    return 2 * (x + 3)

x = 2                           # starting point
lr = 0.1                        # learning rate (step size)
epochs = 100                    # max iterations
tol = 1e-6                      # stop when change becomes very small
path = [x]                      # store every x to plot later

for i in range(epochs):
    new_x = x - lr * gradient(x)        # move opposite to the gradient
    path.append(new_x)
    if abs(new_x - x) < tol:            # converged
        x = new_x
        break
    x = new_x
    print("Iteration", i + 1, ": x =", round(x, 5), " y =", round(f(x), 5))

print("Local minimum at x =", round(x, 4), ", y =", round(f(x), 6))

# Plot the function and the steps taken
xs = np.linspace(-6, 4, 100)
plt.plot(xs, f(xs))
plt.plot(path, [f(p) for p in path], "ro-")
plt.title("Gradient Descent on y = (x+3)^2")
plt.xlabel("x"); plt.ylabel("y")
plt.show()