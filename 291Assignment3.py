import sqlite3
import time
import sys

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def createTables():
    global connection, cursor
    query = open('tables.sql', 'r').read()
    cursor.executescript(query)
    connection.commit()

    return

def InsertValues():
    global connection, cursor
    query = open('queries.txt', 'r').read()
    cursor.executescript(query)
    connection.commit()
    
    
def SelectFunction():
    global connection, cursor
    
    print("Please choose a task to preform type e/exit to exit: \n 1. Task 1 \n 2. Task 2 \n 3. Task 3 \n 4. Task 4 \n 5. Task 5 \n 6. Task 6")

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
    elif choice == 5:
        Task5function()
    elif choice == 6:
        Task6function()

    return
    

def Task1function():
    global connection, cursor

    return


def Task2function():
    global connection, cursor

    return

def Task3function():
    global connection, cursor
    
    string = input("Please enter a range by typing the lower bound number, a - and a higher bound number (Ex: 2-4))\n")
    lower_bound = int(string[0])
    upper_bound = int(string[2])
    cursor.execute("SELECT COUNT(*), r.reviewer FROM users u, reviews r WHERE r.reviewer = u.email GROUP BY r.reviewer HAVING COUNT(*) >= :lb AND COUNT(*) <= :ub",
              {"lb":lower_bound, "ub":upper_bound})
    rows = cursor.fetchall()
    print(rows)

    return

def Task4function():
    global connection, cursor

    return

def Task5function():
    global connection, cursor

    return

def Task6function():
    global connection, cursor

    return




def main():
    global connection, cursor

    path = "./a3.db"
    #path = str(sys.argv[1])
    connect(path)
    #createTables()    // Only needs to be run once to create Tables
    #InsertValues()    // Only needs to be run once to insert values
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
