import time
from art import *
from tabulate import tabulate
import os
from colorama import Fore, Back, Style

def is_safe(table, row, col, N):
    # Check the current column and row
    for i in range(N):
        if table[row][i] == 1 or table[i][col] == 1:
            return False

    # Check diagonal
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if table[i][j] == 1:
            return False

    for i, j in zip(range(row, N, 1), range(col, N, 1)):
        if table[i][j] == 1:
            return False
    
    
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if table[i][j] == 1:
            return False
    
    for i, j in zip(range(row, -1, -1), range(col, N, 1)):
        if table[i][j] == 1:
            return False
        
    return True


def backtraking(table, col, N):
    global totalExpandedNodes,findTotalSolutions 
    if col >= N:
        return True

    for row in range(N):
        if is_safe(table, row, col, N):
            totalExpandedNodes += 1
            table[row][col] = 1
            if backtraking(table, col + 1, N):
                # show just the first solution
                if(not findTotalSolutions):
                    print_table(table)
                    return True    
        
                # show all solutions
                print_table(table)

            table[row][col] = 0

    return False

def print_table(table):
    print(tabulate(table,[],tablefmt="rounded_grid"))

def main():
    # Clear the console and show the title of the algorithm
    os.system('clear')
    print(Fore.YELLOW,text2art("Welcome to N-Queens")) 

    # Ask about how many queens we want to use in the table
    print(Fore.GREEN,'Please insert the number of queens')
    n = int(input())

    while(n<1):
        print("Please insert a number greater than 0")
        n = int(input())

    print("How many solutions do you want to find?")
    print("0 : First Solution \n1: All solutions")
    option = int(input())
    while(option != 0 and option != 1):
        print("Please select a valid option")
        option = int(input())
    
    print(Fore.WHITE,"Running Backtracking :\')")
    initMainVariables(n, option)

def initMainVariables(queenNumber, solutions):
    #  define all vars
    global table,startTime,endTime,findTotalSolutions,totalExpandedNodes,n
    n = queenNumber

    # init table
    table = [[0 for i in range(n)] for j in range(n)]
    
    # second index in the menu was all solutions 
    findTotalSolutions = int(solutions) == 1
     
    startTime = time.time()
    totalExpandedNodes = 0
    

    # start at the position 0
    backtraking(table,0,n)

    endTime = time.time()

    print(Fore.GREEN,'The total number of expanded nodes is ' + str(totalExpandedNodes))

    print(Fore.GREEN,'Total time ', endTime - startTime)

main()