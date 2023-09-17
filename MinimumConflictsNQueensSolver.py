import random
import time
from datetime import datetime
from collections import Counter
import pandas as pd


class MinimumConflictsNQueensSolver:
    def __init__(self, N, growth_interval, number_of_iterations, max_attempts=100, max_time=5):
        self.N = N
        self.growth_interval = growth_interval
        self.number_of_iterations = number_of_iterations
        self.board = list(range(self.N))
        self.expanded_nodes = 0
        self.data = []
        self.max_attempts = max_attempts
        self.max_time = max_time

    def calculate_conflicts_reparations(self):
        conflicts_reparations = []
        for row in range(self.N):
            if not self.is_valid_queen(row, self.board[row]):
                for col in range(self.N):
                    if col != self.board[row] and self.is_valid_queen(row, col):
                        conflicts_reparations.append((row, col))

        if not conflicts_reparations:
            return None  # No conflicts to repair

        counter_conflicts_reparations = Counter(key for key, _ in conflicts_reparations)
        queen_with_less_conflict = min(counter_conflicts_reparations, key=counter_conflicts_reparations.get)
        conflicts_reparations = list(filter(lambda x: x[0] == queen_with_less_conflict, conflicts_reparations))
        return random.choice(conflicts_reparations)

    def is_valid_queen(self, row, col):
        # Check if it's safe to place a queen at position (row, col)
        for i in range(row):
            if self.board[i] == col or abs(self.board[i] - col) == abs(i - row):
                return False
        return True

    def is_valid_board(self):
        # Check if the board is valid (no conflicts)
        for row in range(self.N):
            for col in range(row + 1, self.N):
                if (
                        self.board[row] == self.board[col] or
                        abs(self.board[row] - self.board[col]) == abs(row - col)
                ):
                    return False
        return True

    def random_board(self):
        # Create a random initial board configuration with distinct values
        random.shuffle(self.board)

    def solve(self):
        self.board = list(range(self.N))
        while not self.is_valid_board():
            self.random_board()
            attempts = 0
            start_time = time.time()
            while attempts < self.max_attempts or time.time() - start_time <= self.max_time:
                self.expanded_nodes += 1
                conflicts_reparations = self.calculate_conflicts_reparations()
                if conflicts_reparations is None:
                    return  # No conflicts to repair
                row, col = conflicts_reparations
                self.board[row] = col
                if self.is_valid_board():
                    return
                attempts += 1

    def test(self):
        for _ in range(self.number_of_iterations):
            self.expanded_nodes = 0
            start_time = time.time()
            self.solve()
            end_time = time.time()
            # Convert timestamps to datetime objects
            start_time_datetime = datetime.fromtimestamp(start_time)
            end_time_datetime = datetime.fromtimestamp(end_time)
            iteration_data = {
                "N": self.N,
                "start_time": start_time_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": end_time_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                "duration(s)": end_time - start_time,
                "expanded_nodes": self.expanded_nodes
            }
            self.data.append(iteration_data)
            self.N += self.growth_interval

        self.print_table()

    def print_board(self):
        if self.board is None:
            print("No solution found.")
            return
        for row in range(self.N):
            print(" ".join("Q" if self.board[row] == col else "." for col in range(self.N)))

    def print_table(self):
        df = pd.DataFrame(self.data)

        # Print DataFrame
        print(df)


if __name__ == "__main__":
    N = 8  # Change N according to the desired board size
    growth_interval = 16
    number_of_iterations = 5
    solver = MinimumConflictsNQueensSolver(N, growth_interval, number_of_iterations)
    solver.test()
