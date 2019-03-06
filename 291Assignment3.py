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
    

    connection.commit()
    connection.close()
    return


if __name__ == "__main__":
    main()
