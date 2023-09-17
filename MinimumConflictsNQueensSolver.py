import random
import time
from datetime import datetime
from collections import Counter
import pandas as pd


class MinimumConflictsNQueensSolver:
    def __init__(self, N, growth_interval, number_of_iterations, max_attempts=1000, max_time=100):
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
            if not self.is_valid_queen(row, self.board[row], self.board):
                for col in range(self.N):
                    board_copy = list(self.board)
                    board_copy[row] = col
                    if col != self.board[row] and self.is_valid_queen(row, col, board_copy):
                        conflicts_reparations.append((row, col))

        if not conflicts_reparations:
            return None  # No conflicts to repair

        counter_conflicts_reparations = Counter(key for key, _ in conflicts_reparations)
        queen_with_less_conflict = min(counter_conflicts_reparations, key=counter_conflicts_reparations.get)
        conflicts_reparations = list(filter(lambda x: x[0] == queen_with_less_conflict, conflicts_reparations))
        return random.choice(conflicts_reparations)

    @staticmethod
    def is_valid_queen(row, col, board):
        # Check if it's safe to place a queen at position (row, col)
        for i in range(len(board)):
            if i != row:
                if board[i] == col or abs(board[i] - col) == abs(i - row):
                    return False
        return True

    def is_valid_board(self):
        # Check if the board is valid (no conflicts)
        for row in range(self.N):
            if not self.is_valid_queen(row, self.board[row], self.board):
                return False
        return True

    def random_board(self):
        # Create a random initial board configuration with distinct values
        random.shuffle(self.board)

    def solve(self):
        self.board = list(range(self.N))
        while not self.is_valid_board():
            self.random_board()
            print("\nTablero Aleatorio")
            self.print_board()
            attempts = 0
            start_time = time.time()
            while attempts < self.max_attempts or time.time() - start_time <= self.max_time:
                self.expanded_nodes += 1
                conflicts_reparations = self.calculate_conflicts_reparations()
                if conflicts_reparations is not None:
                    row, col = conflicts_reparations
                    self.board[row] = col
                else:
                    if not self.is_valid_board():
                        self.random_board()

                if self.is_valid_board():
                    return
                attempts += 1

    def test(self):
        for _ in range(self.number_of_iterations):
            self.expanded_nodes = 0
            start_time = time.time()
            self.solve()
            print("Tablero Solución")
            self.print_board()
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
    growth_interval = 4
    number_of_iterations = 5
    solver = MinimumConflictsNQueensSolver(N, growth_interval, number_of_iterations)
    solver.test()