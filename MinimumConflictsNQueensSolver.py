import random
import time


class MinimumConflictsNQueensSolver:
    def __init__(self, N, max_time=30):
        self.N = N
        self.board = [-1] * N
        self.max_attempts = N + 1
        self.max_time = max_time

    def is_valid(self, row, col):
        # Check if it's safe to place a queen at position (row, col)
        for i in range(row):
            if self.board[i] == col or abs(self.board[i] - col) == abs(i - row):
                return False
        return True

    def find_min_conflict(self, row):
        # Find the column that minimizes the number of conflicts and satisfies diagonal constraints
        conflicts = []
        for col in range(self.N):
            if self.is_valid(row, col):
                conflicts.append(self.count_conflicts(row, col))
            else:
                conflicts.append(float('inf'))  # Mark as infinite conflict if not valid
        min_conflicts = min(conflicts)
        min_conflict_cols = [i for i, c in enumerate(conflicts) if c == min_conflicts]
        return random.choice(min_conflict_cols)

    def count_conflicts(self, row, col):
        # Count the number of queens that can attack the queen at position (row, col)
        conflict = 0
        for i in range(row):
            if self.board[i] == col or abs(self.board[i] - col) == abs(i - row):
                conflict += 1
        return conflict

    def solve(self):
        row = 0
        attempts = 0
        start_time = time.time()

        while row < self.N:
            attempts += 1
            col = self.find_min_conflict(row)

            if self.is_valid(row, col):
                self.board[row] = col
                row += 1
            else:
                # Backtrack if unable to place the queen in the current row
                row -= 1

            # Check if the maximum number of attempts has been reached
            if attempts >= self.max_attempts:
                self.board = [-1] * N
                row = 0
                attempts = 0
                start_time = time.time()

            # Check if the maximum time has been exceeded
            if time.time() - start_time >= self.max_time:
                self.board = [-1] * N
                row = 0
                attempts = 0
                start_time = time.time()

        return self.board

    def print_board(self):
        if self.board is None:
            print("No solution found.")
            return
        for row in range(self.N):
            print(" ".join("Q" if self.board[row] == col else "." for col in range(self.N)))


if __name__ == "__main__":
    N = 8  # Change N according to the desired board size
    max_attempts = N  # Maximum number of attempts before resetting
    solver = MinimumConflictsNQueensSolver(N, max_attempts)
    solution_board = solver.solve()
    solver.print_board()
