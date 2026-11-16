# Practical 1: Fibonacci - recursive and non-recursive

# Non-recursive: loop, Time O(n), Space O(1)
def fib_iter(n):
    a, b = 0, 1              # F(0), F(1)
    for i in range(n):
        a, b = b, a + b      # shift: next = sum of previous two
    return a

# Recursive: function calls itself, Time O(2^n), Space O(n) (call stack)
def fib_rec(n):
    if n <= 1:               # base case: F(0)=0, F(1)=1
        return n
    return fib_rec(n - 1) + fib_rec(n - 2)

n = int(input("Enter number of terms: "))

print("Non-recursive:", end=" ")
for i in range(n):
    print(fib_iter(i), end=" ")

print("\nRecursive:    ", end=" ")
for i in range(n):
    print(fib_rec(i), end=" ")
print()