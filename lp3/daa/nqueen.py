# Practical 5: N-Queens using Backtracking (first queen placed by user)

N = int(input("Enter N: "))
col0 = int(input("Column of first queen in row 1 (1 to N): ")) - 1

board = [[0] * N for _ in range(N)]
board[0][col0] = 1                       # place the first queen

# Is it safe to put a queen at (row, col)? Only check above (rows are filled top to bottom)
def is_safe(row, col):
    for k in range(row):                 # same column above
        if board[k][col] == 1:
            return False
    k, l = row - 1, col - 1              # upper-left diagonal
    while k >= 0 and l >= 0:
        if board[k][l] == 1:
            return False
        k, l = k - 1, l - 1
    k, l = row - 1, col + 1              # upper-right diagonal
    while k >= 0 and l < N:
        if board[k][l] == 1:
            return False
        k, l = k - 1, l + 1
    return True

# Place queens row by row starting from row 1 (row 0 already has the first queen)
def solve(row):
    if row == N:                         # all queens placed
        return True
    for col in range(N):
        if is_safe(row, col):
            board[row][col] = 1          # place queen
            if solve(row + 1):           # try to place the rest
                return True
            board[row][col] = 0          # backtrack: remove queen, try next column
    return False                         # no column worked -> go back to previous row

if solve(1):
    for r in board:
        print(*r)
else:
    print("No solution with first queen at this position")