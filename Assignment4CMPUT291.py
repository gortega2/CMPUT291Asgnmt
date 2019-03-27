import sqlite3
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt
import folium

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    connection.commit()
    return


def Task1function():
    global connection, cursor

    return

def Task2function():
    global connection, cursor

    return

def Task3function():
    global connection, cursor

    return

def Task4function():
    global connection, cursor

    return

def SelectFunction():
    global connection, cursor
    
    print("Please choose a task to preform type e/exit to exit: \n 1. Task 1 \n 2. Task 2 \n 3. Task 3 \n 4. Task 4 \n")

    return input()

def ExecuteFunction(choice):

    if choice == 1:
        Task1function()
    elif choice == 2:
        Task2function()
    elif choice == 3:
        Task3function()
    elif choice == 4:
        Task4function()

    return
    

def main():
    global connection, cursor

    path = input("Enter database name: ")
    connect(path)
    
    while True:
        choice = SelectFunction()
        if choice == 'e' or choice == 'exit':
            break
        ExecuteFunction(int(choice))
    

    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()

    
    
