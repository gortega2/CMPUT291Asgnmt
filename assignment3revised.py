import sqlite3
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

    
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
    cursor.execute(" SELECT papers.Id, papers.title FROM papers") # select all papers 
    rows = cursor.fetchall()
    num_rows = len(rows)
    i = 0                   # i is the i-th paper to be printed
    page = 0
    while i < num_rows and i < 5:   # print the first 5 papers
        print(rows[i][0], rows[i][1])
        i = i + 1
    while True:
        instruction = input("Enter 'N' to go to next page, 'P' to go to previous page, or select a paper's ID ")
        if instruction == 'N' or instruction == 'n':    # go to next page
            if i < (num_rows):
                j = 0                                   # j is a counter
                while i < num_rows and j < 5:
                    print(rows[i][0], rows[i][1])
                    i = i + 1
                    j = j + 1
                page += 1
            else:
                print("This is the last page please try again")
            continue
        elif instruction == 'P' or instruction == 'p':  # go to previous page
            if page == 0:
                print("This is the first page please try again")
            else:
                page -= 1
                i = 5 * page
                j = 0                                   # j is a counter
                while i < num_rows and j < 5:
                    print(rows[i][0], rows[i][1])
                    j += 1
                    i = i + 1
            continue
        else:
            # select all the reviewers who have reviewed the paper
            cursor.execute(" SELECT reviews.reviewer FROM papers, reviews WHERE papers.Id = '%s' AND papers.Id = reviews.paper;" % instruction) 
            print("Reviewers:")
            reviewers = cursor.fetchall()
            for reviewer in reviewers:
                print(reviewer[0])
            break
    return


def Task2function():
    global connection, cursor
    cursor.execute(" SELECT papers.Id, papers.title FROM papers")   # select all papers 
    rows = cursor.fetchall()
    num_rows = len(rows)
    i = 0                   # i is the i-th paper to be printed
    page = 0
    while i < num_rows and i < 5:      # print the first 5 papers
        print(rows[i][0], rows[i][1])
        i = i + 1
    while True:
        instruction = input("Enter 'N' to go to next page, 'P' to go to previous page, or select a paper's ID to review the paper ")
        if instruction == 'N' or instruction == 'n':    # go to next page
            if i < (num_rows):
                j = 0                                   # j is a counter
                while i < num_rows and j < 5:
                    print(rows[i][0], rows[i][1])
                    i = i + 1
                    j = j + 1
                page += 1
            else:
                print("This is the last page please try again")
            continue
        elif instruction == 'P' or instruction == 'p':  # go to previous page
            if page == 0:
                print("This is the first page please try again")
            else:
                page -= 1
                i = 5 * page
                j = 0                                   # j is a counter
                while i < num_rows and j < 5:
                    print(rows[i][0], rows[i][1])
                    j += 1
                    i = i + 1
            continue
        else:
            p_id = int(instruction)
            # select all the potential reviewers author excluded
            cursor.execute(" SELECT expertise.reviewer FROM papers p1, expertise WHERE expertise.area = p1.area AND p1.Id = '%s' AND p1.author <> expertise.reviewer EXCEPT SELECT r1.reviewer FROM papers p2, reviews r1 WHERE p2.Id = r1.paper AND p2.Id = '%s' ;" % (instruction, instruction))  
            print("Potential reviewers:")
            reviewers = cursor.fetchall()
            p_reviewers = []
            for reviewer in reviewers:
                print(reviewer[0])
                p_reviewers.append(reviewer[0])
            reviewer = input("Select a potential reviewer to enter reviews ")
            if reviewer not in p_reviewers:                                         # check if it is a potential reviewer
                print("This is not a potential reviewer, review denied")
            else:                                                                   # ask for inputs
                originality = input("Please enter the score for originality ")
                importance = input("Please enter the score for importance ")
                soundness = input("Please enter the score for soundness ")
                overall = input("Please enter the score for overall ")
                # insert review into database
                cursor.execute(" INSERT INTO reviews VALUES (?,?,?,?,?,?)", (p_id, reviewer, int(originality), int(importance), int(soundness), int(overall))) 
                connection.commit()
                print("Reviews added")
            break
    return

# No error checking implemented yet
def Task3function():
    global connection, cursor
    
    string = input("Please enter a range by typing the lower bound number, a - and a higher bound number (Ex: 2-4))\n") # ask for range
    lower_bound = int(string[0])
    upper_bound = int(string[2])
    
    # select all reviewers in expertise and the number of paper they've reviewed
    cursor.execute("SELECT COUNT(DISTINCT reviews.paper), expertise.reviewer FROM expertise LEFT JOIN reviews USING (reviewer) GROUP BY expertise.reviewer HAVING COUNT(DISTINCT reviews.paper) >= :lb AND COUNT(DISTINCT reviews.paper) <= :ub", {"lb":lower_bound, "ub":upper_bound}) 
    rows = cursor.fetchall()
    print(rows)
    return
# No error checking implemented yet
def Task4function():
    global connection, cursor
    choice = int(input("Please select a task by inputting the corresponding number: \n 1. A bar plot of all individual authors \n 2. Select an individual author \n"))

    if choice == 1:     
        
        # select author with accepted papers and the number of papers accepted
        df = pd.read_sql_query("SELECT p.author, COUNT(*) FROM papers p, sessions s WHERE p.csession = s.name AND p.decision = 'A' GROUP BY p.author", connection)     
        plot = df.plot.bar(x="author") # plot the diagram
        plt.plot()
        plt.show()
    elif choice == 2:
        
        # select authors with papers accepted
        cursor.execute("SELECT p.author FROM papers p, sessions s WHERE p.csession = s.name AND p.decision = 'A' GROUP BY p.author")
        rows = cursor.fetchall()
        for i in range(len(rows)):
            print(str(i) + ". " + str(rows[i][0]))
        author = int(input("Please select an author by selecting the corresponding number: \n"))
        author = rows[author][0]
        # select the author's name and count the number of papers accepted
        cursor.execute("SELECT p.author, COUNT(*) FROM papers p, sessions s WHERE p.csession = s.name AND p.decision = 'A' AND p.author = :athr",
                       {"athr":author})
        print(cursor.fetchall())
        
        
    else:
        print("Invalid choice")

    return

def Task5function():
    global connection, cursor
    # select area's name and count the number of papers under that area
    df = pd.read_sql_query('''
                               SELECT areas.name AS area, COUNT(papers.id) AS count
                               FROM areas LEFT JOIN papers ON (areas.name = papers.area)
                               GROUP BY areas.name
                               ORDER BY COUNT(papers.id) DESC;''', connection)
    
    index = 1
    while index < len(df.index) and (index < 5 or df.iloc[index,1] == df.iloc[index-1,1]):
        index +=1
    # plot the graph
    if not df.empty:
        df.iloc[:index].plot.pie(labels=df.area,y="count")
        plt.plot()
        plt.show()
    return

def Task6function():
    global connection, cursor
    # select reviewer and calculate the average for each category
    df = pd.read_sql_query('''
                               SELECT reviewer, 
                                   AVG(originality) AS Average_originality,
                                   AVG(importance) AS Average_importance,
                                   AVG(soundness) AS Average_soundness
                               FROM reviews
                               GROUP BY reviewer;''', connection)
    # plot the graph
    if not df.empty:
        plot = df.plot.bar(x= 'reviewer')
        plt.plot()
        plt.show()
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
